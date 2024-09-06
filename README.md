Fork from the Chord Visualizer code made by AdielBm @ https://github.com/adielBm/chord-extractor

### GOALS
- Add functional chord diagrams.
- Fix the generation of chord-diagrams from the original code, which prevents any sharp chords from being displayed.
- Implement some changes/improvements to the original project:
-   [x]  Removed "open HTML in browser".
-   [x]  Spaces and symbols in path without using "quotations".
-   [x]  General code fixed.
-   [ ]  (Pending) Include Audio Pitch (+) (-) feature, and others ...

  
### REQUIREMENTS

- Python (The same version as 'ohollo/chord-extractor' needs).
Please note that chord-extractor currently requires python 3.9.x, 'pyenv' and 'direnv' may be used for this purpose.
- Ohollo's chord-extractor and all of its dependences (See https://github.com/ohollo/chord-extractor)


### USAGE

* No need of using "quotation marks" in the input path.

LINUX:
```
$ python cho.py song.mp3
```

An HTML with the same name of the audio input file will be generated.


_2024, September. 6th._
