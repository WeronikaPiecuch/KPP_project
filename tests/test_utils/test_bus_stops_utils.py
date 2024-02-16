import pytest
from project.utils.bus_stops_utils import *


@pytest.fixture
def sample_bus_stops_df(tmp_path):
    sample_data = {
        'zespol': [1, 2, 1],
        'slupek': ['01', '01', '02'],
        'lat': [52.345, 52.456, 52.567],
        'lon': [21.012, 21.123, 21.234]
    }
    sample_df = pd.DataFrame(sample_data)
    sample_csv_path = tmp_path / 'bus_stops.csv'
    sample_df.to_csv(sample_csv_path, index=False)
    return tmp_path


def test_get_bus_stops(sample_bus_stops_df):
    bus_stops_df = get_bus_stops(sample_bus_stops_df)
    assert isinstance(bus_stops_df, pd.DataFrame)
