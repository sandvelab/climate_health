from climate_health.climate_data.gee import ERA5DataBase
from climate_health.datatypes import Location, ClimateData
from climate_health.time_period import Month, Day, TimePeriod
import pytest


@pytest.mark.skip('ee not supported')
def test_era5():
    location = Location(17.9640988, 102.6133707)
    start_month = Month(2012, 1)
    mocked_data = ERA5DataBase().get_data(location, start_month, Month(2012, 7))
    assert len(mocked_data) == 6
    mocked_data = ERA5DataBase().get_data(location, start_month, Month(2013, 7))
    assert len(mocked_data) == 18
    full_data = ERA5DataBase().get_data(location, Month(2010, 1), Month(2024, 1))
    full_data.to_csv('climate_data.csv')


@pytest.mark.skip('ee not supported')
def test_era5_daily():
    location = Location(17.9640988, 102.6133707)
    start_day = Day(2012, 1, 1)
    mocked_data = ERA5DataBase().get_data(location, start_day, Day(2012, 2, 2))
    assert len(mocked_data) == 32
    mocked_data = ERA5DataBase().get_data(location, start_day, Day(2013, 1, 1))
    assert len(mocked_data) == 366
    full_data = ERA5DataBase().get_data(location, Day(2010, 1, 1), Day(2015, 1, 1))
    full_data.to_csv('climate_data_daily.csv')
