import re
import numpy as np
from datetime import timedelta

from chord_extractor.extractors import Chordino
from pydub import AudioSegment

from madmom.features.beats import DBNBeatTrackingProcessor, RNNBeatProcessor
from madmom.features.downbeats import DBNBarTrackingProcessor, RNNBarProcessor, RNNDownBeatProcessor, DBNDownBeatTrackingProcessor
from madmom.features.chords import CNNChordFeatureProcessor, CRFChordRecognitionProcessor

chordino = Chordino()

# TODO: i think we should analyze and provide sample rate here?
# From madmom Docs:
# Create a DBNBeatTrackingProcessor. The returned array represents the
# positions of the beats in seconds, thus the expected sampling rate has to
# be given.

# TODO:
# seems like the main issues now are:
#       - the next chord often begins during the findal second of the
#         current chord, these need to be adjusted so that that time is included
#         in the next chord and disqualified from the current chord
#           - align by beat?
#           - graph the two against eachother next
#
#       - It often detects the min version or maj version incorrectly.
#         It may be correct to the model but incorrect based on the songs
#         notation. In these cases maybe try to find the key of the song?
#         Althought if we're trying to find key baesd on the chords it'll be
#         wrong if the chords are wrong.
#
#       - Having a db of song key would help
#       - Having a db of bpm might help too
#
#      - Once in a while it detects completely incorrect chords, F#m or D#
#
#      - inconsistent segment lengths, need to be able to normalize lengths
#
#      - guess chord names based on the other chords in the song & verifiable
#        key data?
#
#     - split chords by beats when chords are properly aligned

chord_processor = CNNChordFeatureProcessor()
chord_decoder = CRFChordRecognitionProcessor()

beat_processor = RNNDownBeatProcessor(fps=100)
beat_decoder = DBNDownBeatTrackingProcessor(beats_per_bar=[4], fps=100)

# use click to get file path properly
file_path = '/Users/mwcmitchell/projects/chord-grid/mase.mp3'
print(f'file_path: {file_path}')

audio = AudioSegment.from_mp3(file_path)

class Chord:
    def __init__ (self, chord_name, curr_beat_time, prev_beat_time, curr_beat, prev_chord):
        self.chord_name = chord_name
        self.prev_beat_time = prev_beat_time
        self.curr_beat_time = curr_beat_time
        self.curr_beat    = curr_beat
        self.prev_chord = prev_chord


regx = re.compile('(?<![\d.])0*(?:(\d+)\.?|\.(0)|(\.\d+?)|(\d+\.\d+?))0*(?![\d.])')
def number_shaver(ch, regx=regx, repl=lambda x: x.group(x.lastindex) if x.lastindex!=3 else '0' + x.group(3)):
    # https://stackoverflow.com/questions/5807952/removing-trailing-zeros-in-python
    return regx.sub(repl,ch)


def display_ms(ms):
    return number_shaver(str(timedelta(milliseconds=ms)))


def remove_N(chords):
    """
    Remove the 'N' chords representing segments where no chord is identified

    Combines the 'N' chord segment with the prev chord segment - unless it's
    the first segment in the list, in that case it's combined with the next.
    """
    idx_to_delete = []
    for idx,  c in enumerate(chords):
        if idx == len(chords):
            break

        # TODO: there's gotta be a better way to write this
        #       only targetting c rather than next_c and prev_c
        #       optimize later though
        if (c[2] == 'N') and (len(chords) >= idx + 1):
            if idx == 0:
                # first, have to combine w next
                next_c = chords[idx +1]
                next_c[0] = c[0]
                chords[idx + 1] = next_c
            else:
                prev_c = chords[idx - 1]
                prev_c[1] = c[1]
                chords[idx - 1] = prev_c
            idx_to_delete.append(idx)

    chords = np.delete(chords, idx_to_delete)
    return chords



# TODO combine this with remove_N so only one loop
def combine_sequential(chords):
    """
    combine sequential chords into one longer chord

    this currently ignores Maj/Min as it seems like the algorithm detetcts that
    very accurately, finding transitions where the notation indicates the same chord
    it's possible you could just adjust a variable for likelyhood of chord transition?
    """

    idx_to_delete = []
    for idx, c in enumerate(chords):
        if idx == len(chords):
            break

        if (idx - 1 >= 0):
            prev_c = chords[idx - 1]
            if prev_c[2][0] == c[2][0]:
                prev_c[1] = c[1]
                chords[idx - 1] = prev_c
                idx_to_delete.append(idx)
        pass

    chords = np.delete(chords, idx_to_delete)
    return chords



def extract_and_export_chords():

    beats = beat_decoder(beat_processor(file_path))
    chords = chord_decoder(chord_processor(file_path))


    chordsArray = []
    chord_idx = 0
    chord_name = 'N'

    chords = remove_N(chords)
    chords = combine_sequential(chords)

    start = 0
    end = 0
    for idx, c in enumerate(chords):
        if idx == len(chords):
            break

        chord_name = c[2]
        start = c[0] * 1000
        end = c[1] * 1000
        audio_chunk = audio[start:end]

        start = display_ms(start)
        end = display_ms(end)
        print(f'split at [{start} - {end}]')
        audio_chunk.export(f'./output/chords/{idx}-{chord_name}-{start}-{end}.mp3', format="mp3")

    print('done exporting chords')


# it seems like this is returning the same thing as extract_and_export_beats?
def extract_and_export_downbeats():

    print('initializing RNNBeatProcessor...')
    act = RNNBeatProcessor()(file_path)

    print('getting beats...')
    beats = beat_processor(act)
    # TODO: is this the best way to do this?

    print('initializing RNNBarProcessor...')
    bars = RNNBarProcessor()((file_path, beats))

    # TODO: this seems like it returns each beat in the bar properly
    #       I was expecting the first beat in each bar
    print('getting downbeats...')
    downbeats = beat_decoder(bars)

    print('splitting...')
    n = 1
    if n != 1:
        every_n_downbeats = [value for index, value in enumerate(downbeats) if index % n == 1]
        downbeats = every_n_downbeats

    start = 0
    for idx, b in enumerate(downbeats):
        if idx == len(downbeats):
            break
        end = b[0] * 1000
        print(f'split at [{start}:{end}] ms')
        audio_chunk = audio[start:end]
        audio_chunk.export(f'./output/downbeats/{idx}-{str(start)}-{end}.mp3', format="mp3")
        start = end

    print('done extracting and exporting downbeats')
    return


# it seems like this is returning the same thing as extract_and_export_downbeats?
def extract_and_export_beats():
    act = RNNBeatProcessor()(file_path)

    # TODO: maybe re-use the btp(act) results for downbeats if they run
    # sequentially
    beats = beat_processor(act)

    n = 1
    if n != 1:
        every_n_beats = [value for index, value in enumerate(beats) if index % n == 1]
        beats = every_n_beats

    start = 0
    for idx, b in enumerate(beats):
        if idx == len(beats):
            break
        end = b * 1000
        print(f'split at [{start}:{end}] ms')
        audio_chunk = audio[start:end]
        audio_chunk.export(f'./output/beats/{idx} - {str(start)} - {end}.mp3', format="mp3")
        start = end
    print('done extracting and exporting beats')
    return


def extract_and_export_chords_chordify():
    chords = chordino.extract(file_path)
    print(f'extracted {len(chords)}')

    start = 0
    for  idx, c in enumerate(chords):
        #break loop if at last element of list
        if idx == len(chords):
            break

        end = c.timestamp * 1000 #pydub works in millisec
        print(f"split at [{start}:{end}] ms")
        audio_chunk=audio[start:end]

        # do os.mkdirs
        audio_chunk.export(f"./output/chords/{idx}_{str(c.chord).replace('/','slash')}_{end}.mp3", format="mp3")

        start = end
    print('done extracting chords')
    return


if __name__ == '__main__':
    extract_and_export_chords()
