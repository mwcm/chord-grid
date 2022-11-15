import re
import numpy as np
from datetime import timedelta

from pydub import AudioSegment, silence
from pydub.utils import mediainfo


from madmom.features.beats import DBNBeatTrackingProcessor, RNNBeatProcessor, MultiModelSelectionProcessor, CRFBeatDetectionProcessor
from madmom.features.downbeats import DBNBarTrackingProcessor, RNNBarProcessor, RNNDownBeatProcessor, DBNDownBeatTrackingProcessor
from madmom.features.chords import CNNChordFeatureProcessor, CRFChordRecognitionProcessor, DeepChromaChordRecognitionProcessor


chord_processor = CNNChordFeatureProcessor(fps=100)
chord_decoder = CRFChordRecognitionProcessor(fps=100)
# DeepChromaChordRecognitionProcessor

#note: was this used earlier?
beat_processor = DBNBeatTrackingProcessor(fps=100)

# TODO:
# Notate expected chord position in audacity

# - Use it to compare against
#   - start with comparing against current results
#   - then without removing leading silence, remove_N, combine_sequential

# - Adjust audio segments manually as little as possible
# - Use model params effectively


# TODO: seems like these @ 10 do same as at 100, for test song at least
#       test more

# 10 is aligned with chordprocessor
downbeat_processor = RNNDownBeatProcessor(fps=100)
# https://github.com/CPJKU/madmom/blob/3bc8334099feb310acfce884ebdb76a28e01670d/madmom/features/downbeats.py#L122
downbeat_decoder = DBNDownBeatTrackingProcessor(beats_per_bar=[4], fps=100)

# https://github.com/CPJKU/madmom/blob/3bc8334099feb310acfce884ebdb76a28e01670d/madmom/features/downbeats.py#L1038
# DBNBarTrackingProcessor

# use click to get file path properly
file_path = 'C:/Users/mwcm/Documents/GitHub/chord-grid/mase.mp3'
print(f'file_path: {file_path}')

# TODO: pass this through instead of using it as a global
rudio = AudioSegment.from_mp3(file_path)

# It seems like leading silence effects outputs:
#   - removing leading silence before processing the file results
#     in dramatically different results from the downbeat and chord processors
#
#   - accounting for leading slice in-loop like below in the
#     extrac_and_export_chords fn seems to help a ton

# leading_silence = silence.detect_leading_silence(audio, chunk_size=1)

def main():
    extract_and_export_chords()
    return


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
    return str(number_shaver(str(timedelta(milliseconds=ms)))).replace(':','-').replace('.', '-')


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

    beats = downbeat_decoder(downbeat_processor(file_path))
    chords = chord_decoder(chord_processor(file_path))

    chords = remove_N(chords)
    chords = combine_sequential(chords)

    start = 0
    end = 0
    for idx, c in enumerate(chords):
        if idx == len(chords):
            break

        chord_name = c[2]

        # if start == 0:
        start = (c[0] * 1000) #+ leading_silence
        #else:
        #    start = (c[0] * 1000)

        end = (c[1] * 1000)

        audio_chunk = audio[start:end]

        start = display_ms(start)
        end = display_ms(end)
        print(f'split at [{start} - {end}]')
        audio_chunk.export(f'./output/chords/{idx}_{chord_name.replace(":","-")}_{start}_{end}.mp3', format="mp3")

    print('done exporting chords')


# it seems like this is returning the same thing as extract_and_export_beats?
def extract_and_export_downbeats():

    print('initializing RNNBeatProcessor...')
    act = RNNBeatProcessor()(file_path)

    print('getting beats...')
    beats = downbeat_processor(act)
    # TODO: is this the best way to do this?

    print('initializing RNNBarProcessor...')
    bars = RNNBarProcessor()((file_path, beats))

    # TODO: this seems like it returns each beat in the bar properly
    #       I was expecting the first beat in each bar
    print('getting downbeats...')
    downbeats = downbeat_decoder(bars)

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


#def extract_and_export_chords_chordify():
    #chords = chordino.extract(audio)
    #print(f'extracted {len(chords)}')

    #start = 0
    #for  idx, c in enumerate(chords):
        ##break loop if at last element of list
        #if idx == len(chords):
            #break

        #end = c.timestamp * 1000 #pydub works in millisec
        #print(f"split at [{start}:{end}] ms")
        #audio_chunk=audio[start:end]

        ## do os.mkdirs
        #audio_chunk.export(f"./output/chords/{idx}_{str(c.chord).replace('/','slash')}_{end}.mp3", format="mp3")

        #start = end
    #print('done extracting chords')
    #return


if __name__ == '__main__':
    main()
