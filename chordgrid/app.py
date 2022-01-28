from chordgrid.detection.chords import Chords
from chordgrid.detection.beats import Beats
from chordgrid.detection.downbeats import DownBeats

def run():
    print('init')
    beats = Beats()
    downbeats = DownBeats()
    chords = Chords()
    print('done init')
    return