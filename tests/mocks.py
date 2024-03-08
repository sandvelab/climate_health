import numpy as np
import pytest

from climate_health.datatypes import Shape, Location, ClimateData
from climate_health.time_period import TimePeriod, Month as sMonth
from climate_health.time_period.dataclasses import Month
from climate_health.time_period.period_range import period_range


class ClimateDataBaseMock:
    def get_data(self, region: Shape, start_period: TimePeriod, end_period, exclusive_end=False):

        assert hasattr(region, 'latitude'), f'Expected Location, got {type(region)}'
        assert not exclusive_end
        period = period_range(start_period, end_period)
        # generate periodic monthly temperature
        w = 365.24 if hasattr(start_period, 'day') else 12
        temperature = 20 + 5 * np.sin(2 * np.pi * period.month / w)
        rainfall = 100 + 50 * np.sin(2 * np.pi * period.month / w)
        return ClimateData(period, rainfall, temperature, temperature)

@pytest.fixture
def climate_database():
    return ClimateDataBaseMock()