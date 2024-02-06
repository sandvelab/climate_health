from climate_health.datatypes import ClimateHealthTimeSeries
from climate_health.plotting import plot_timeseries_data


def test():
    data = ClimateHealthTimeSeries.from_csv("../example_data/data.csv")
    fig = plot_timeseries_data(data)
    fig.show()
