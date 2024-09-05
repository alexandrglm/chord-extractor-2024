FORK of "chord-extractor HTML generator" code made by AdielBm @ https://github.com/adielBm/chord-extractor

### GOALS
- Add functional chord diagrams.
- Fix the generation of chord-diagrams from the original code, which prevents any sharp chords from being displayed.
- Implement some changes/improvements to the original project.

  

### REQUIREMENTS
- Python (The same version as 'ohollo/chord-extractor' needs).
Please note that chord-extractor currently requires python 3.9.x, 'pyenv' and 'direnv' may be used for this purpose.

- Ohollo's chord-extractor and all of its dependences (See https://github.com/ohollo/chord-extractor)


### USAGE

LINUX:
```
$ python cho.py song.mp3
```
WIN:
```
C:\...\Music> python "C:\...\chord_extractor\cho.py" "song.mp3"
```

An HTML with the same name of the .mp3 file will be generated.
Don't move their dependences (script.js, style.css, 'guitar' and 'ukelele' folders, ...).
