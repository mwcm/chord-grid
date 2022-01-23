chord-grid
----------

chordipy?

TODDO next:
 - check audacity comparison, try removing any chords not in the song's key as pulled from spotify api
 - look into how to better align chords/beats, use the model params  or try to modify  the script from the madmom repo issue

requires ffmpeg and ffprobe built on py3.7.9

numpy needs to be installed before madmom

The goal is to generate a playable grid of samples broken down by beat grid
and ready to be imported to Ableton Live drum rack.

Inspired by the chordify grid - which is already doing this very well for most
songs.

<img width="806" alt="Screen Shot 2022-01-11 at 11 13 19 AM" src="https://user-images.githubusercontent.com/2433319/148979518-16b0d8eb-d979-4256-b1c4-fa3abe1af7fc.png">
