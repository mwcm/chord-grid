from chord_extractor.extractors import Chordino
from pydub import AudioSegment

from madmom.features.beats import DBNBeatTrackingProcessor, RNNBeatProcessor
from madmom.features.downbeats import DBNBarTrackingProcessor, RNNBarProcessor

chordino = Chordino()

# TODO: i think we should probably analyze and provide sample rate here?
# From madmom Docs:
# Create a DBNBeatTrackingProcessor. The returned array represents the
# positions of the beats in seconds, thus the expected sampling rate has to
# be given.
btp = DBNBeatTrackingProcessor(fps=100)

# it seems like this actually gets each beat?
# i would have expected these settings to get only the 1st of each bar
dbtp = DBNBarTrackingProcessor(beats_per_bar=[1, 4])

# use click to get file path properly
file_path = '/Users/mwcmitchell/projects/chord-grid/mase.mp3'
print(f'file_path: {file_path}')

audio = AudioSegment.from_mp3(file_path)


def extract_and_export_downbeats():

    act = RNNBeatProcessor()(file_path)
    beats = btp(act)
    # TODO: is this the best way to do this?
    bars = RNNBarProcessor()((file_path, beats))

    # TODO: this seems like it returns each beat in the bar properly
    #       I was expecting the first beat in each bar
    downbeats = dbtp(act)

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
        audio_chunk.export(f'./output/downbeats/{idx} - {str(start)} - {end}.mp3', format="mp3")
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
    beats = btp(act)

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


def extract_and_export_chords():
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
