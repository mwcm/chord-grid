from madmom.features.tempo import TempoEstimationProcessor
from madmom.features.beats import (
    RNNBeatProcessor, MultiModelSelectionProcessor, BeatDetectionProcessor,
    CRFBeatDetectionProcessor, DBNBeatTrackingProcessor, BeatTrackingProcessor
)


class Beats:

    def __init__(self, fps=100, min_bpm=15.0, max_bpm=215.0, nn_files=None, tempo_estimator=None):
        self.fps = fps
        self.min_bpm = min_bpm
        self.max_bpm = max_bpm
        self.nn_files = nn_files
        self.tempo_estimator = TempoEstimationProcessor(min_bpm=self.min_bpm, max_bpm=self.max_bpm)
        self.tempo_estimator = tempo_estimator or self.tempo_estimator

        # use post_processor = None to get all nn predictions
        self.beat_predictor = RNNBeatProcessor(
            fps=self.fps, nn_files=self.nn_files, post_processor=None
        )

        # with None selected the MultiModelProcessor will averages all predictions
        # to obtain a reference prediction
        self.multi_model_prediction_processor = MultiModelSelectionProcessor(num_ref_predictions=None)

        self.beat_tracking_post_processor = BeatTrackingProcessor(fps=self.fps, tempo_estimator=tempo_estimator)
        self.beat_detection_post_processor = BeatDetectionProcessor(fps=self.fps)

        # NOTE: try to edit observation lambda and transition lambda here
        self.dbn_post_processor = DBNBeatTrackingProcessor(
            fps=self.fps, min_bpm=self.min_bpm, max_bpm=self.max_bpm
        )

        # NOTE: try some of the params on this one too?
        self.crf_post_processor = CRFBeatDetectionProcessor(fps=self.fps)

        self.post_processors = [
            self.beat_tracking_post_processor,
            self.beat_detection_post_processor,
            self.dbn_post_processor,
            self.crf_post_processor
        ]
        return


    def predict_beats(self, audio_file_path):
        predictions = self.beat_predictor(audio_file_path)
        return predictions


    def select_best_prediction(self, predictions):
        most_suitable_prediction = self.multi_model_prediction_processor(predictions)
        return most_suitable_prediction


    def post_process_prediction(self, prediction, post_processor=None):
        """ if post_processor is None we'll use all of them """

        beat_times = []

        if not post_processor:
            for idx, p in enumerate(self.post_processors):
                p_beat_times = p(prediction) 
                beat_times[idx] = p_beat_times
            return beat_times

        if post_processor not in self.post_processors:
            raise ValueError(f'Invalid post_processor {post_processor}'
                             f'valid post processors are {self.post_processors}.')

        beat_times = post_processor(prediction)
        return beat_times
    