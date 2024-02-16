import pytest
from unittest.mock import patch
from project.collecting_data.online_locations_collecting import *


TEST_COLLECTING_TIME = 10


@pytest.fixture(scope="function")
def test_data_dir(tmp_path):
    return tmp_path / 'test_data'


@pytest.fixture(scope="function")
def mocked_response():
    # this will be unvalid from 15-02-2025
    sample_response = [
        {'VehicleNumber': '123', 'Lines': 'A', 'Brigade': '1', 'Time': '2025-02-15 12:00:00', 'Lon': '123.456',
         'Lat': '456.789'},
        {'VehicleNumber': '456', 'Lines': 'B', 'Brigade': '2', 'Time': '2025-02-15 12:01:00', 'Lon': '234.567',
         'Lat': '567.890'}
    ]
    return sample_response


def test_prepare_files(mocked_response, tmp_path):
    with patch('project.collecting_data.online_locations_collecting.get_results') as mock_get_results:
        mock_get_results.return_value = mocked_response
        test_data_dir = tmp_path / 'test_data'
        os.makedirs(test_data_dir, exist_ok=True)
        os.makedirs(test_data_dir / 'online_locations', exist_ok=True)

        vehicles_last_time, vehicles_constant_data, data_dir_name = prepare_files(str(test_data_dir))

        assert os.path.isdir(data_dir_name)
        assert os.path.isfile(os.path.join(data_dir_name, 'vehicles.csv'))
        assert os.path.isfile(os.path.join(data_dir_name, '123.csv'))
        assert os.path.isfile(os.path.join(data_dir_name, '456.csv'))


def test_collect_result(mocked_response, test_data_dir):
    os.makedirs(test_data_dir, exist_ok=True)
    with open(test_data_dir / '123.csv', 'w') as f:
        f.write("Time,Lon,Lat\n")

    with patch('project.collecting_data.online_locations_collecting.get_results') as mock_get_results:
        mock_get_results.return_value = mocked_response

        vehicles_last_time = {123: time.time() - 3600}
        vehicles_last_time_old = vehicles_last_time.copy()
        vehicles_constant_data = {'123': ['A', '1']}
        vehicles_last_time = collect_result(vehicles_last_time, vehicles_constant_data, str(test_data_dir))

        csv_file_path = test_data_dir / '123.csv'
        assert os.path.isfile(csv_file_path)

        with open(csv_file_path, 'r') as f:
            lines = f.readlines()
            print(lines)
        assert len(lines) == 2

        assert vehicles_last_time[123] > vehicles_last_time_old[123]


def test_collect_online_locations(mocked_response, test_data_dir):
    os.makedirs(test_data_dir, exist_ok=True)
    os.makedirs(test_data_dir / 'online_locations', exist_ok=True)
    with patch('project.collecting_data.online_locations_collecting.get_results') as mock_get_results:
        mock_get_results.return_value = mocked_response
        with patch('project.collecting_data.online_locations_collecting.COLLECTING_TIME', TEST_COLLECTING_TIME):
            collect_online_locations(test_data_dir)

    expected_dir = test_data_dir / 'online_locations'
    new_dir = os.listdir(expected_dir)[-1]
    expected_dir = expected_dir / new_dir
    expected_csv_path_123 = expected_dir / '123.csv'
    expected_csv_path_456 = expected_dir / '456.csv'
    expected_csv_path_vehicles = expected_dir / 'vehicles.csv'

    assert expected_csv_path_vehicles.is_file()
    assert expected_csv_path_123.is_file()
    assert expected_csv_path_456.is_file()
