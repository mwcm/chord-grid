from madmom.audio.chroma import DeepChromaProcessor
from madmom.features.chords import (
    CNNChordFeatureProcessor, CRFChordRecognitionProcessor,
    DeepChromaChordRecognitionProcessor 
)

# NOTE ON CHORDS fps
# ------------------
# from docs:
# > fps : float
# > Frames per second. Must correspond to the fps of the incoming
# > activations and the model.

# - beats are set to 100 so shouldn't this also be fps=100?
#    seems like it's 10 in the docs mostly, while beats are 100
# - results seemed the same with fps 100 as 10? retest

class Chords:

    def __init__(self, fps=10, crf_model=None, deep_chroma_model=None):
        """ if models are None, madmom defaults will be used """
        self.fps = fps
        self.deep_chroma_model = deep_chroma_model
        self.crf_model = crf_model

        self.chord_feature_extractor = CNNChordFeatureProcessor()

        # https://madmom.readthedocs.io/en/v0.16.1/modules/audio/chroma.html#madmom.audio.chroma.DeepChromaProcessor
        # fmin=65, fmax=2100, unique_filters=True, models=None
        self.chord_deep_chroma_vector_extractor  = DeepChromaProcessor()

        self.chord_crf_processor = CRFChordRecognitionProcessor(model=crf_model, fps=fps)
        self.chord_deep_chroma_processor = DeepChromaChordRecognitionProcessor(mode=deep_chroma_model, fps=fps)

        self.processors = [self.chord_crf_processor, self.chord_deep_chroma_processor]
        return


    def extract_features(self, audio_file_path):
        features = self.chord_feature_extractor(audio_file_path)
        return features


    def extract_chroma_vectors(self, audio_file_path):
        chroma_vectors = self.chord_deep_chroma_vector_extractor(audio_file_path)
        return chroma_vectors
    

    def process_chord_features(self, chord_features):
        # recognize chords from features
        decoded_chords = self.chord_crf_processor(chord_features)
        return decoded_chords


    def process_chroma_vectors(self, chroma_vectors):
        # decode chord sequence from chroma vectors
        decoded_chords = self.chord_deep_chroma_processor(chroma_vectors)
        return decoded_chords