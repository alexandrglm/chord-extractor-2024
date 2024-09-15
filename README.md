# Chord-yzer v0.3 - Musical analyzer
## Chord Extraction & Database & Analysis Tool

A python and HTML/CSS/JS based tool to **extract chords from any song**, 
which  **creates a database to analyze and show** chord-key data by  different criteria as *title*, *artist*, by *chord type*, *number of times* a chord appears; by song, by a group of songs or globally.


## INCLUDES

 - Chord extracting from any MP3, WAV, MIDI file.
 - Chord Visualizer with GUITAR diagrams, HTML5-webkit compatible.
 - Chord carts transposing with live changing diagrams.
 - Bar/Time Signatures counting, Tempo/BPM analyzer tool & live rhythm change.
 - Keynote analysis on each bar, A4 referencial frequency identifier.
 - A database generation for analysing purposses capable of sorting chords, how many times used, the most and least used chords; by song, globally, ....


## REQUIREMENTS

 - Python 3.9.x
 - pip install numpy librosa chord-extractor (and it requirements)

## USAGE
```
$ python cho.py
```

The program generates:
1. _Artist_Title.html_ file. The visualizer of each song.
2. _chord_database.html_ and _chord_db.json_ files. A full database of all the song's with data analysis tools. Both files are updated automatically.

**In order to generatethe files both,  you are told to provide some info as:**
 *- ARTIST NAME*
 *- SONG TITLE*

(Development in progress)

2024 September, 15th.
