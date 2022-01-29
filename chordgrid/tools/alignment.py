from madmom.features.downbeats import SyncronizeFeaturesProcessor


def madmom_syncronize_features(features, downbeats, beat_subdivisions=4, fps=100):
    '''
    First, divide a beat interval into beat_subdivision divisions.
    Then summarise all features that fall into one subdivision.
    If no feature value for a subdivision is found, it is set to 0.

    beat_subdivisions : int
        Number of subdivisions a beat interval is divided into. 
    '''
    sfp = SyncronizeFeaturesProcessor(beat_subdivisions=beat_subdivisions, fps=fps)
    beat_synchronized_features = sfp.process((features, downbeats))
    return beat_synchronized_features