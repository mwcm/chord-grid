from chord_extractor.extractors import Chordino
from pydub import AudioSegment

chordino = Chordino()
file_path = '/Users/mwcmitchell/projects/chord-grid/mase.mp3'
print(f'file_path: {file_path}')

audio = AudioSegment.from_mp3(file_path)
chords = chordino.extract(file_path)
# todo: cache this result, takes a while

print(f'extracted {len(chords)}')

start = 0
for  idx, c in enumerate(chords):
    #break loop if at last element of list
    if idx == len(chords):
        break

    end = c.timestamp * 1000 #pydub works in millisec
    print(f"split at [{start}:{end}] ms")
    audio_chunk=audio[start:end]
    audio_chunk.export(f"./{idx}_{str(c.chord).replace('/','slash')}_{end}.mp3", format="mp3")

    start = end
