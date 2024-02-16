import os
import pytest
from unittest.mock import patch
from project.collecting_data.bus_stops_collecting import *


def test_download_bus_stops(tmp_path):
    with patch('project.collecting_data.bus_stops_collecting.get_response') as mock_get_response:
        sample_response = [{'values': [{'key': 'zespol', 'value': '200'}, {'key': 'slupek', 'value': '1'},
                                       {'key': 'szer_geo', 'value': 123.456}, {'key': 'dlug_geo', 'value': 456.789}]}]
        expected_response = sample_response.copy()
        mock_get_response.return_value = sample_response
        test_data_dir = tmp_path / 'test_data'
        os.makedirs(test_data_dir, exist_ok=True)

        download_bus_stops(str(test_data_dir))

        json_file_path = test_data_dir / 'bus_stops.json'
        assert json_file_path.exists()
        with open(json_file_path) as json_file:
            json_data = json.load(json_file)
            assert json_data == expected_response

        csv_file_path = test_data_dir / 'bus_stops.csv'
        assert csv_file_path.exists()
        csv_data = pd.read_csv(csv_file_path)
        expected_columns = ['zespol', 'slupek', 'lat', 'lon']
        assert list(csv_data.columns) == expected_columns
        assert csv_data.iloc[0]['zespol'] == 200
        assert csv_data.iloc[0]['slupek'] == 1
        assert pytest.approx(csv_data.iloc[0]['lat'], 0.001) == 123.456
        assert pytest.approx(csv_data.iloc[0]['lon'], 0.001) == 456.789
