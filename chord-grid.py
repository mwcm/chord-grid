import numpy as np

from chord_extractor.extractors import Chordino
from pydub import AudioSegment

from madmom.features.beats import DBNBeatTrackingProcessor, RNNBeatProcessor
from madmom.features.downbeats import DBNBarTrackingProcessor, RNNBarProcessor, RNNDownBeatProcessor, DBNDownBeatTrackingProcessor
from madmom.features.chords import CNNChordFeatureProcessor, CRFChordRecognitionProcessor

chordino = Chordino()

# TODO: i think we should probably analyze and provide sample rate here?
# From madmom Docs:
# Create a DBNBeatTrackingProcessor. The returned array represents the
# positions of the beats in seconds, thus the expected sampling rate has to
# be given.

# TODO use madmom settings to get better chord/beat detection results

chord_processor = CNNChordFeatureProcessor()
chord_decoder = CRFChordRecognitionProcessor()

beat_processor = RNNDownBeatProcessor(fps=100)
beat_decoder = DBNDownBeatTrackingProcessor(beats_per_bar=[4], fps=100)

# use click to get file path properly
file_path = '/Users/mwcmitchell/projects/chord-grid/mase.mp3'
print(f'file_path: {file_path}')

audio = AudioSegment.from_mp3(file_path)

class Chord:
    def __init__ (self, chord_name, curr_beat_time, curr_beat, prev_chord):
        self.chord_name = chord_name
        self.curr_beat_time   = curr_beat_time
        self.curr_beat    = curr_beat
        self.prev_chord = prev_chord


def extract_and_export_chords():

    beats = beat_decoder(beat_processor(file_path))
    chords = chord_decoder(chord_processor(file_path))


    for idx,  c in enumerate(chords):
        if idx == len(chords):
            break


        # TODO: THIS ALMOST WORKS
        # working for the first item but then it's deleting the wrong index

        if (c[2] == 'N') and (len(chords) > idx + 1):
            if idx == 0:
                # first, have to combine w next
                next_c = chords[idx +1]
                next_c[0] = c[0]
                chords[idx + 1] = next_c
            else:
                prev_c = chords[idx - 1]
                prev_c[1] = c[1]
                chords[idx - 1] = prev_c
            chords = np.delete(chords, idx, 0)

    chordsArray = []
    chord_idx = 0
    chord_name = 'N'

    start = 0
    end = 0
    for idx, c in enumerate(chords):
        if idx == len(chords):
            break

        start = c[0] * 1000
        end = c[1] * 1000
        chord_name = c[2]

        print(f'split at [{start}:{end}] ms')
        audio_chunk = audio[start:end]

        audio_chunk.export(f'./output/chords/{idx}-{chord_name}-{start}-{end}.mp3', format="mp3")
        prev_chord = c


    # TODO: figure this out next
    # for beat_idx in range(len(beats) - 1):
    #     curr_beat_time, curr_beat = beats[beat_idx]
    #     # find the corresponding chord for this beat
    #     while chord_idx < len(chords):
    #         chord_time, _ , chord_name = chords[chord_idx]
    #         prev_beat_time, _ = (0, 0) if beat_idx == 0 else beats[beat_idx - 1]
    #         eps = (curr_beat_time - prev_beat_time) / 2
    #         if chord_time > curr_beat_time + eps:
    #             break
    #         chord_idx += 1
    # 
    #         # append to array
    #         # TODO: I know this is supposed to be @ the same level as the while
    #         # loop for the chord/beat alignment to work properly
    #         #
    #         # BUT the chords look correct when it's over here
    #         # and they look completely wrong with it over there
    #         # maybe I have something else wrong earlier?
    #     _, _, prev_chord = chords[chord_idx - 1]
    #     chord = Chord(chord_name, curr_beat_time, curr_beat, prev_chord)
    #     chordsArray.append(chord)

    # for c in chordsArray:
    #     print(c.chord_name)
    #     print(c.curr_beat_time)

    # chord_name = 'N'
    # start = 0
    # for idx, c in enumerate(chordsArray):
    #     if idx == len(chordsArray):
    #         break
    #     end = c.curr_beat_time * 1000
    #     print(f'split at [{start}:{end}] ms')
    #     audio_chunk = audio[start:end]
    #     audio_chunk.export(f'./output/chords/{idx}-{chord_name}-{str(start)}-{end}.mp3', format="mp3")
    #     # leave this, printing an 0-0 chord at the start pushes everything back one
    #     # TODO: adjust above so there is no 0-0 chord at the start
    #     chord_name = c.chord_name
    #     start = end

    print('done exporting chords')


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


# TODO: I'm not exactly sure what this is doing?
#       Maybe it is working properly and I'm just mishearing the results
#       Need to graph out the results visually too
def extract_and_export_beats():
    # TODO: is this the best way to do this?
    act = RNNBeatProcessor()(file_path)

    # TODO: maybe re-use the btp(act) results for downbeats?
    #       not sure if that's going to be useful or not?
    #       will they ever run one after another?
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