from chordgrid.detection.chords import Chords
from chordgrid.detection.beats import Beats
from chordgrid.detection.downbeats import DownBeats

def run():
    print('starting inits')
    beats = Beats()
    downbeats = DownBeats()
    chords = Chords()
    print('done inits')
    return