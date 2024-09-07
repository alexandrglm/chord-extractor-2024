import os
import json
import librosa
import numpy as np
from viewer import generate_html_with_chords
from db import generate_db_html
from chord_extractor.extractors import Chordino
from engine.scales import scales

DB_FILE = "chords_db.json"

def sanitize_filename(input_str):
    import unicodedata
    import re
    normalized = unicodedata.normalize('NFKD', input_str).encode('ASCII', 'ignore').decode('utf-8')
    sanitized = re.sub(r'[^\w\s-]', '', normalized)
    return sanitized.strip().replace(' ', '_')

def sanitize_url(url):
    from urllib.parse import quote
    return quote(url, safe='/:')

def extract_chords_from_audio(audio_file):
    chordino = Chordino(roll_on=1.0)
    chords = chordino.extract(audio_file)
    return chords

def get_bpm(audio_file):
    y, sr = librosa.load(audio_file)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    tempo, beat_frames = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    return tempo[0] if isinstance(tempo, np.ndarray) and tempo.size == 1 else tempo, beat_times

def get_reference_pitch_segment(audio_file, start_time, end_time):
    y, sr = librosa.load(audio_file, offset=start_time, duration=end_time - start_time)
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    magnitude_median = np.median(magnitudes)
    a4_range = (440.0 * np.power(2, -0.5), 440.0 * np.power(2, 0.5))
    a4_frequencies = [pitches[i, j] for i in range(pitches.shape[0]) for j in range(pitches.shape[1])
                      if magnitudes[i, j] > magnitude_median and a4_range[0] <= pitches[i, j] <= a4_range[1]]
    if a4_frequencies:
        a4_frequency = np.mean(a4_frequencies)
    else:
        a4_frequency = 440.0
    return a4_frequency

def get_tone_from_frequencies(frequencies, reference_freq):
    if len(frequencies) == 0:
        return None
    tones = librosa.hz_to_midi(frequencies)
    median_tone = np.median(tones)
    return librosa.midi_to_note(median_tone)

def get_tone_at_beats(audio_file, beat_times):
    tones_at_beats = []
    for i, beat_time in enumerate(beat_times[:-1]):
        start_time = beat_time
        end_time = beat_times[i + 1]
        reference_freq = get_reference_pitch_segment(audio_file, start_time, end_time)
        y, sr = librosa.load(audio_file, offset=start_time, duration=end_time - start_time)
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        magnitude_median = np.median(magnitudes)
        significant_pitches = pitches[magnitudes > magnitude_median]
        if significant_pitches.size > 0:
            tone = get_tone_from_frequencies(significant_pitches, reference_freq)
            tones_at_beats.append((beat_time, tone))
    return tones_at_beats

def convert_ndarray_to_list(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, (list, tuple)):
        return [convert_ndarray_to_list(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_ndarray_to_list(v) for k, v in obj.items()}
    else:
        return obj

def load_scales():
    return scales

def match_chords_to_scales(chords, scales):
    chord_names = set(chord for chord in chords)
    best_match = None
    best_match_score = 0
    for key, scale_types in scales.items():
        for scale_name, scale_notes in scale_types.items():
            scale_notes_set = set(scale_notes)
            match_score = len(chord_names.intersection(scale_notes_set))
            if match_score > best_match_score:
                best_match = (key, scale_name)
                best_match_score = match_score
    return best_match

def update_chords_db(artist, title, chords, bpm, tempo_changes, tones_at_beats, keynote):
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                chords_db = json.load(f)
        except json.JSONDecodeError:
            print("Error: Corrupted JSON...creating new json file")
            chords_db = []
    else:
        chords_db = []

    chord_counts = {}
    for chord in chords:
        chord_name = chord.chord
        if chord_name not in chord_counts:
            chord_counts[chord_name] = 1
        else:
            chord_counts[chord_name] += 1

    tempo_changes = convert_ndarray_to_list(tempo_changes)
    tones_at_beats_serializable = convert_ndarray_to_list(tones_at_beats)

    scales = load_scales()
    best_match = match_chords_to_scales(chord_counts.keys(), scales)

    song_entry = {
        "artist": artist,
        "title": title,
        "chords": chord_counts,
        "bpm": bpm,
        "tempo_changes": tempo_changes,
        "tones_at_beats": tones_at_beats_serializable,
        "keynote": best_match[0] if best_match else "Unknown"
    }

    chords_db.append(song_entry)

    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(chords_db, f, indent=4, ensure_ascii=False)

    return song_entry

def determine_key_from_chords(chords):
    chord_names = [chord.chord for chord in chords]

    scales = load_scales()
    for keynote, scale_variations in scales.items():
        for scale_name, scale_chords in scale_variations.items():
            if all(chord in scale_chords for chord in chord_names):
                return keynote

    return "Unknown"

def main():
    audio_file = input("Enter the path to the audio file: ")
    artist_name = input("ARTIST ?: ")
    song_title = input("SONG TITLE ?: ")

    if not os.path.exists(audio_file):
        print("Error: File does not exist.")
        return

    tempo, beat_times = get_bpm(audio_file)
    print(f"BPM: {tempo}")
    print(f"Beat times: {beat_times}")

    tones_at_beats = get_tone_at_beats(audio_file, beat_times)

    print("Tones at detected beats:")
    for beat_time, tone in tones_at_beats:
        print(f"Time: {beat_time:.2f}s - Tone: {tone}")

    chords = extract_chords_from_audio(audio_file)

    keynote = determine_key_from_chords(chords)
    print(f"Keynote: {keynote}")

    song_entry = update_chords_db(artist_name, song_title, chords, tempo, beat_times, tones_at_beats, keynote)

    html_file = generate_html_with_chords(audio_file, chords, artist_name, song_title, tempo, beat_times, tones_at_beats, keynote)
    print(f"Analysis complete. Results saved to {html_file}")

    generate_db_html()

if __name__ == "__main__":
    main()
