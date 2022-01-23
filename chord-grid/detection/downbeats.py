from madmom.features.downbeats import (RNNDownBeatProcessor, RNNBarProcessor,
    DBNDownBeatTrackingProcessor, DBNBarTrackingProcessor, SyncronizeFeaturesProcessor)

# RNNDownBeat
# Takes audio Returns
# Returns Downbeat probabilities

# RNNBar
# Takes Beat POSITIONS + audio
# Returns Downbeat probabilities

# DBNDownBeatTracking
# Takes Activation function with probabilities corresponding to beats and downbeats given in the first and second column, respectively. 
# Returns decoded Downbeat positions & beat #'s

# DBNBarTracking
# Array containing beat positions (first column) and corresponding downbeat activations (second column).
# returns decoded Downbeat positions & beat #'s

class DownBeats:

    def __init__(self):
        return
