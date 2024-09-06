import os
import argparse
from chord_extractor.extractors import Chordino

def extract_chords_from_audio(audio_file):
    chordino = Chordino()
    chords = chordino.preprocess(audio_file)
    chords = chordino.extract(audio_file)
    return chords

def generate_html_with_chords(audio_file, chords):
    output_file_name = os.path.splitext(os.path.basename(audio_file))[0] + ".html"
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Chords from Audio</title>
        <script src="script.js"></script>
        <link rel="stylesheet" type="text/css" href="style.css" />
    </head>
    <body>
    <header>
      <div>
        <h4>File: {audio_file}</h4>
        <audio controls>
          <source src="{audio_file}" type="audio/mpeg" />
          Your browser does not support the audio element.
        </audio>
        <div>
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
        <img id="chord-diagram-current" src="empty.png" />
        <h1 id="chord-current"></h1>
        <div style=" width: 2px; height: 100%; display: block; background: #8d94b4; margin: 15px; "></div>
        <img id="chord-diagram-next" src="empty.png" />
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
    with open(html_file, "w") as f:
        f.write(html_content)

    return html_file

def main(audio_file):
    chords = extract_chords_from_audio(audio_file)
    html_file = generate_html_with_chords(audio_file, chords)
    print(f"\033[92m{html_file} has been generated\033[0m")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate HTML with chords from audio file")
    parser.add_argument("audio_file", nargs=argparse.REMAINDER, help="Path to the audio file")
    args = parser.parse_args()
    audio_file = ' '.join(args.audio_file)
    main(audio_file)
