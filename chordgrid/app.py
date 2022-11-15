from chordgrid.detection.chords import Chords
from chordgrid.detection.beats import Beats
from chordgrid.detection.downbeats import DownBeats

def run():
    print('init')
    beat_detection = Beats()
    downbeat_detection = DownBeats()
    chord_detection = Chords()
    print('done init')

    

    return