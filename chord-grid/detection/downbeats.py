from madmom.features.downbeats import (
    RNNDownBeatProcessor, RNNBarProcessor, DBNDownBeatTrackingProcessor,
    DBNBarTrackingProcessor, SyncronizeFeaturesProcessor
)

# DBNDownBeatTracking
# Takes Activation function with probabilities corresponding to beats and downbeats given in the first and second column, respectively. 
# Returns decoded Downbeat positions & beat #'s

# DBNBarTracking
# Array containing beat positions (first column) and corresponding downbeat activations (second column).
# returns decoded Downbeat positions & beat #'s

class DownBeats:

    def __init__(self, beat_subdivisions=(4,2), beats_per_bar=[4],
                 fps=100, min_bpm=55.0, max_bpm=215.0):
        ''' beat_subdivions - tuple with # of beat subdivisions
            for the percussive and harmonic feature. '''

        # number of subdivisions a beat is divided into
        self.beat_subdivisions = beat_subdivisions
        self.beats_per_bar = beats_per_bar
        self.fps = fps
        self.min_bpm = min_bpm
        self.max_bpm = max_bpm

        self.downbeat_predictor = RNNDownBeatProcessor()
        # downbeat_bar_predictor takes beat predictions as well as audio
        self.downbeat_bar_predictor = RNNBarProcessor(
            beat_subdivisions=self.beat_subdivisions, fps=self.fps
        )

        # maybe try experimenting with
        # num_tempi=60, transition_lambda=100, observation_lambda=16,
        self.downbeat_processor = DBNDownBeatTrackingProcessor(
            beats_per_bar=self.beats_per_bar, fps=self.fps,
            min_bpm = self.min_bpm, max_bpm=self.max_bpm
        )

        # maybe try experimenting with 
        # observation_weight=100, meter_change_prob=1e-07
        self.downbeat_bar_processor = DBNBarTrackingProcessor(
            beats_per_bar=self.beats_per_bar
        )

        self.processors = [self.downbeat_processor, self.downbeat_bar_processor]
        return


    def predict_downbeats(self, beats=None): 

        if beats:
            return
        
        return


    def process_downbeats(self, prediction, processor=None):
        """ if post_processor is None we'll use both of them """
        downbeat_times = []
        if not processor:
            for idx, p in enumerate(self.processors):
                p_beat_times = p(prediction) 
                downbeat_times[idx] = p_beat_times
            return downbeat_times

        if processor not in self.processors:
            raise ValueError(f'Invalid processor {processor}'
                             f'valid post processors are {self.processors}.')

        beat_times = processor(prediction)
        return beat_times