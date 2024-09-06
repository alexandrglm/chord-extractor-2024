import os
import argparse
import json
import re
import unicodedata
import numpy as np
import librosa
from chord_extractor.extractors import Chordino
from urllib.parse import quote

DB_FILE = "chords_db.json"

def sanitize_filename(input_str):
    normalized = unicodedata.normalize('NFKD', input_str).encode('ASCII', 'ignore').decode('utf-8')
    sanitized = re.sub(r'[^\w\s-]', '', normalized)
    return sanitized.strip().replace(' ', '_')

def sanitize_url(url):
    return quote(url, safe='/:')

def extract_chords_from_audio(audio_file):
    chordino = Chordino()
    chords = chordino.preprocess(audio_file)
    chords = chordino.extract(audio_file)
    return chords

def get_bpm(audio_file):
    y, sr = librosa.load(audio_file)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    return round(tempo[0]) if isinstance(tempo, (list, np.ndarray)) else round(tempo)

def update_chords_db(artist, title, chords, bpm):
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            chords_db = json.load(f)
    else:
        chords_db = []

    chord_counts = {}
    for chord in chords:
        chord_name = chord.chord
        if chord_name not in chord_counts:
            chord_counts[chord_name] = 1
        else:
            chord_counts[chord_name] += 1

    song_entry = {
        "artist": artist,
        "title": title,
        "chords": chord_counts,
        "bpm": bpm
    }

    chords_db.append(song_entry)

    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(chords_db, f, indent=4, ensure_ascii=False)

    return song_entry

def generate_html_with_chords(audio_file, chords, artist, title, bpm):
    sanitized_artist = sanitize_filename(artist)
    sanitized_title = sanitize_filename(title)
    output_file_name = f"{sanitized_artist}_{sanitized_title}.html"

    sanitized_audio_file = sanitize_url(audio_file)

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Chords from {artist} - {title}</title>
        <script src="./scripts/script.js"></script>
        <link rel="stylesheet" type="text/css" href="./scripts/style.css" />
    </head>
    <body>
    <header>
      <div>
        <h4>File: {sanitized_audio_file}</h4>
        <label for="bpm-input">BPM:</label>
        <input type="number" id="bpm-input" value="{bpm}" step="1" min="30" max="300" />
        <button id="update-bpm">Update BPM</button>
        <audio controls>
          <source src="{sanitized_audio_file}" type="audio/mpeg" />
          Your browser does not support the audio element.
        </audio>
        <div>
          <button id="vel-up">BPM(+)</button>
          <button id="vel-down">BPM(-)</button>
          <button id="transpose-up">Transpose Up (+)</button>
          <button id="transpose-down">Transpose Down (-)</button>
          Transpose: <span id="transpose-counter">0</span>, Capo:
          <span id="capo-counter">0</span>
          <input type="radio" id="guitar" name="instrument" value="guitar" checked />
          <label for="guitar">Guitar</label>
          <input type="radio" id="ukulele" name="instrument" value="ukulele" />
          <label for="ukulele">Ukulele</label>
        </div>
      </div>
      <div id="chord-diagram-bar">
        <img id="chord-diagram-current" src="./diagrams/empty.png" />
        <h1 id="chord-current"></h1>
        <div style=" width: 2px; height: 100%; display: block; background: #8d94b4; margin: 15px; "></div>
        <img id="chord-diagram-next" src="./diagrams/empty.png" />
        <h1 id="chord-next"></h1>
      </div>
    </header>
    <button id="zoom-in">zoom-in(+)</button>
    <button id="zoom-out">zoom-out(-)</button>
    <ul id="chords">
    """

    for chord in chords:
        seconds = chord.timestamp
        html_content += f"<li id='{seconds}'>{chord.chord}</li>"

    html_content += """
        </ul>
    </body>
    </html>
    """

    html_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), output_file_name)
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    return html_file

def generate_db_html():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            chords_db = json.load(f)
    else:
        chords_db = []

    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Chords Database</title>
        <script src="./scripts/jquery.min.js"></script>
        <script src="./scripts/jquery.dataTables.min.js"></script>
        <link rel="stylesheet" href="./scripts/jquery.dataTables.min.css">
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1 { text-align: center; margin-bottom: 40px; }
            table { width: 100%; margin-top: 20px; border-collapse: collapse; }
            table, th, td { border: 1px solid #ddd; }
            th, td { padding: 8px; text-align: center; }
            th { background-color: #f4f4f4; cursor: pointer; }
            tr:nth-child(even) { background-color: #f9f9f9; }
        </style>
    </head>
    <body>
    <h1>Chords Database</h1>
    <table id="chords-table">
        <thead>
            <tr>
                <th>Artist</th>
                <th>Title</th>
                <th>Chord</th>
                <th>Times Used</th>
                <th>BPM</th>  <!-- Añadir columna BPM -->
            </tr>
        </thead>
        <tbody>
    """

    for entry in chords_db:
        artist = entry["artist"]
        title = entry["title"]
        bpm = entry.get("bpm", "N/A")
        for chord, count in entry["chords"].items():
            html_content += f"<tr><td>{artist}</td><td>{title}</td><td>{chord}</td><td>{count}</td><td>{bpm}</td></tr>"

    html_content += """
        </tbody>
    </table>

    <script>
        $(document).ready(function() {
            $('#chords-table').DataTable({
                "paging": true,
                "searching": true,
                "order": [[3, "desc"]],
                "columns": [
                    { "orderable": true },
                    { "orderable": true },
                    { "orderable": true },
                    { "orderable": true },
                    { "orderable": false }  // Columna BPM no ordenable
                ]
            });
        });
    </script>
    </body>
    </html>
    """

    db_html_file = "chords_database.html"
    with open(db_html_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"\033[92m{db_html_file} has been generated\033[0m")
    return db_html_file

def main(audio_file, artist, title):
    chords = extract_chords_from_audio(audio_file)
    bpm = get_bpm(audio_file)  # Obtener BPM
    html_file = generate_html_with_chords(audio_file, chords, artist, title, bpm)
    print(f"\033[92m{html_file} has been generated\033[0m")

    update_chords_db(artist, title, chords, bpm)  # Actualizar base de datos con BPM

    generate_db_html()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate HTML with chords from audio file")
    parser.add_argument("audio_file", nargs=argparse.REMAINDER, help="Path to the audio file")
    args = parser.parse_args()
    audio_file = ' '.join(args.audio_file)

    artist = input("Artist: ")
    title = input("Title: ")

    main(audio_file, artist, title)
