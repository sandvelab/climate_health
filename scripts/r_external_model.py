import logging
logging.basicConfig(level=logging.INFO)
import numpy as np
import pandas as pd

from climate_health.assessment.dataset_splitting import split_test_train_on_period, get_split_points_for_data_set
from climate_health.datatypes import tsdataclass, TimeSeriesData
from climate_health.external.external_model import ExternalCommandLineModel
from climate_health.spatio_temporal_data.temporal_dataclass import SpatioTemporalDict
from climate_health.time_period import TimePeriod, Month, PeriodRange
from climate_health.time_period.dataclasses import Period as OurPeriod
from pandas import Period


@tsdataclass
class HydrometDengueData(TimeSeriesData):
    dengue_cases: int
    pdsi: float
    urban: float
    tmax: float
    tmin: float



@tsdataclass
class HydroClimateData(TimeSeriesData):
    pdsi: float
    urban: float
    tmax: float
    tmin: float


def hydromet_from_pandas(df):
    #df = pd.read_csv(filename)
    df = df.sort_values(by=['micro_code', 'year', 'month'])
    period = []
    for _, row in df.iterrows():
        string_period = f"{row['year']}-{row['month']}"
        period.append(Period(string_period))

    df['time_period'] = period
    #grouped = df.groupby('micro_name_ibge')
    grouped = df.groupby('micro_code')

    data_dict = {}
    for name, group in grouped:
        tmax = group['tmax'].values
        tmin = group['tmin'].values
        tmean = (tmax + tmin) / 2
        data_dict[name] = HydrometDengueData(
            PeriodRange.from_pandas(group['time_period']),
            group['dengue_cases'].values, group['pdsi'].values, group['urban'].values, tmax, tmin)

    return SpatioTemporalDict(data_dict)


def hydromet_to_pandas(data: SpatioTemporalDict[HydrometDengueData]):
    df = data.to_pandas()

    # change column location to micro_name_ibge
    df = df.rename(columns={'location': 'micro_name_ibge'})

    # change time_period to year and month
    df['year'] = df['time_period'].apply(lambda x: x.year)
    df['month'] = df['time_period'].apply(lambda x: x.month)

    return df


def test_read_write_hydromet():
    df = pd.read_csv('example_data/masked_data_til_2005.csv')
    data = hydromet_from_pandas(df)
    new_df = hydromet_to_pandas(data)

    assert np.all(np.sort(df.year) == np.sort(new_df.year))
    assert np.all(np.sort(df.month) == np.sort(new_df.month))




train_command = "Rscript external_models/hydromet_dengue/train.R {train_data} {model} external_models/hydromet_dengue/map.graph"
setup_command = "Rscript external_models/hydromet_dengue/setup.R"
predict_command = "Rscript external_models/hydromet_dengue/predict.R {future_data} {model}"

model = ExternalCommandLineModel(
    name='r_env',
    train_command=train_command,
    predict_command=predict_command,
    data_type=None,
    setup_command=setup_command,
    conda_env_file="external_models/hydromet_dengue/env.yml"
)

model.setup()


all_data = hydromet_from_pandas(pd.read_csv('example_data/masked_data_til_2005.csv'))
split_points = get_split_points_for_data_set(all_data, max_splits=2)

splits = split_test_train_on_period(all_data, split_points, future_length=None, include_future_weather=True,
                                    future_weather_class=HydroClimateData)
split = list(splits)[-1]

train_data, future_truth, future_climate_data = split

model.train(train_data)
