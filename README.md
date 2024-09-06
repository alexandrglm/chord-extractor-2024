# Chord Extraction&Database Tool v.0.1
_The real alternative to Chordify, but free and offline._

A python and HTML/CSS/JS based tool to **extract chords from any song**, 
which  **creates a database to analyze and show** chord-key data by  different criteria as *title*, *artist*, by *chord type*, *number of times* a chord appears; by song, by a group of songs or globally.


# INCLUDES

 - Chord extracting from any MP3, WAV, MIDI file.
 - Chord Visualizer with GUITAR diagrams, HTML5-webkit compatible.
 - BPM analyzer tool & live rhythm change.
 - Chord transposing with live changing diagrams.
 - A database generation for analysing purposses capable of sorting chords, how many times used, the most and least used chords; by song, globally, ....


## REQUIREMENTS

 - Python.

Please note that chord-extractor currently requires python 3.9.x, so *'pyenv'* and *'direnv*' may be suitable for this purpose.

 
 - Ohollo's chord-extractor and **all** of its dependences 
 (Follow steps from   https://github.com/ohollo/chord-extractor)



## USAGE

LINUX:
```
$ python cho.py song.mp3
```
***No need of using "quotations" in file paths.***

WINDOWS:
```
C:\ python "C:\...\chord_extractor\cho.py" full_path_file.mp3
```

In order to generate *song_chords.html* and *chord_database.html* both,  you are told to provide some info as:

 - ARTIST NAME
 - SONG TITLE




# LICENSING

 1. This is a fork based on AdielBm's https://github.com/adielBm/chord-extractor script, which fixes, improves and adds many functions.
 2. JQuery is used to display data from the database under MIT License https://jquery.com/license/
 3. Chord-Extractor and its dependences are used under GNU General Public Licensing v2.0 
 https://github.com/ohollo/chord-extractor/blob/master/LICENSE


2024 September, 6th.
