from datetime import datetime

import pytest

from climate_health.time_period.date_util_wrapper import TimePeriod, TimeStamp, delta_month, PeriodRange, delta_year, \
    Month, Day, Year


@pytest.fixture
def period1():
    return TimePeriod.parse('2020-1')


@pytest.fixture
def period2():
    return TimePeriod.parse('2020-2')


@pytest.fixture
def period3():
    return TimePeriod.parse('2021-2')


@pytest.fixture
def edge_timestamps():
    texts = ['2019-12-31', '2020-1-1', '2020-1-31', '2020-2-1']
    return [TimeStamp.parse(text) for text in texts]


def test_init_with_numbers(period2):
    assert Month(2020, 2) == period2
    assert Day(2020, 2, 3) == Day(datetime(2020, 2, 3))
    assert Year(2020) == TimePeriod.parse('2020')

def test_parse(period1):
    assert period1.year == 2020
    assert period1.month == 1


def test_ge(period1, period2):
    assert period2 >= period1
    assert period1 >= period1


def test_le(period1, period2):
    assert not (period2 <= period1)
    assert period1 <= period1


def test_greater_than(period1, period2):
    assert period2 > period1
    assert not period1 > period2


def test_less_than(period1, period2):
    assert period1 < period2
    assert not period2 < period1


def test_compare_period_and_timestamp(period1, edge_timestamps):
    le_comparisons = [period1 <= ts for ts in edge_timestamps]
    assert le_comparisons == [False, True, True, True]
    lt_comparisons = [period1 < ts for ts in edge_timestamps]
    assert lt_comparisons == [False, False, False, True]
    ge_comparisons = [period1 >= ts for ts in edge_timestamps]
    assert ge_comparisons == [True, True, True, False]
    gt_comparisons = [period1 > ts for ts in edge_timestamps]
    assert gt_comparisons == [True, False, False, False]


def test_add_month(period1, period2):
    assert period1 + delta_month == period2


def test_divide_timedelta():
    assert delta_year // delta_month == 12


@pytest.fixture
def period_range(period1, period3):
    return PeriodRange.from_time_periods(start_period=period1, end_period=period3)


def test_period_range(period_range):
    assert len(period_range) == 14


def test_period_range_slice(period_range):
    assert len(period_range[1:3]) == 2
    assert len(period_range[1:-2]) == 11


def test_period_range_iter(period_range, period1, period3):
    assert len(period_range) == 14
    l = list(period_range)
    assert len(l) == 14
    assert l[0] == period1
    assert l[-1] == period3


def test_period_range_eq(period_range, period2):
    mask = period_range == period2
    assert len(mask) == len(period_range)
    assert mask[1]
    assert mask.sum() == 1


def test_period_range_ne(period_range, period2):
    mask = period_range != period2
    assert len(mask) == len(period_range)
    assert not mask[1]
    assert mask.sum() == 13


def test_period_range_lt(period_range, period2):
    mask = period_range < period2
    assert len(mask) == len(period_range)
    assert mask[0]
    assert mask.sum() == 1


def test_period_range_le(period_range, period2):
    mask = period_range <= period2
    assert len(mask) == len(period_range)
    assert mask[0] and mask[1]
    assert mask.sum() == 2


def test_period_range_gt(period_range, period2):
    mask = period_range > period2
    assert len(mask) == len(period_range)
    assert (not mask[0]) and (not mask[1])
    assert mask.sum() == 12


def test_period_range_ge(period_range, period2):
    mask = period_range >= period2
    assert len(mask) == len(period_range)
    assert (not mask[0])
    assert mask.sum() == 13

# def period_range_ge():
#    period_range = PeriodRange(start_period=period1, end_period=period3)
