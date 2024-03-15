from typing import List
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error

from climate_health.dataset import IsSpatioTemporalDataSet
from climate_health.datatypes import HealthData, ResultType
from climate_health.time_period import PeriodRange
from climate_health.time_period.date_util_wrapper import TimeStamp


class MultiLocationEvaluator:
    def __init__(self, model_names: List[str], truth: IsSpatioTemporalDataSet[HealthData]):
        self.model_names = model_names
        self.truth = truth
        self.predictions = {model_name: [] for model_name in model_names}

    def add_predictions(self, model_name: str, predictions: IsSpatioTemporalDataSet[HealthData]):
        self.predictions[model_name].append(predictions)
        return self

    def get_results(self) -> dict[str, ResultType]:
        truth_df = self.truth.to_pandas()
        results = {}

        for model_name, predictions in self.predictions.items():
            model_results = []
            for prediction in predictions:
                for location in prediction.locations():

                    pred = prediction.get_location(location).data()
                    prediction_time = self.time_to_string(pred.time_period._start_timestamp) # fix if multi-period pred

                    true = truth_df.loc[(truth_df['location'] == location) &
                                        (truth_df['time_period'] == prediction_time)]

                    if self.check_data(true.disease_cases, pred.disease_cases):
                        mae = mean_absolute_error(true.disease_cases, pred.disease_cases)
                        model_results.append([location, prediction_time, mae])

            results[model_name] = pd.DataFrame(model_results, columns=['location', 'period', 'mae'])

        return results

    def time_to_string(self, time_stamp: TimeStamp) -> str:
        return f"{time_stamp.year}-{str(time_stamp.month).zfill(2)}"

    def check_data(self, true, pred) -> bool:
        if np.isnan(true).any() or np.isnan(pred).any() or len(true) != len(pred):
            return False
        else:
            return True

