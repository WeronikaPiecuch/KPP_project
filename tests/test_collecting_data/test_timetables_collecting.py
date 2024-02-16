import os
import pytest
from project.collecting_data.timetables_collecting import get_lines_list, get_line_timetable, get_timetables, get_lines
import pandas as pd
from unittest.mock import patch


@pytest.fixture(scope="module")
def mocked_response_lines():
    return [
        {
            "values": [{"value": "1", "key": "key"}]
        },
        {
            "values": [{"value": "2", "key": "key"}]
        }
    ]


@pytest.fixture(scope="module")
def mocked_response_timetables():
    return [
        {
            "values": [{"value": "1", "key": "brygada"}, {"value": "12:00:00", "key": "czas"}]
        }
    ]


@pytest.fixture(scope="module")
def mocked_bus_stops_df():
    return pd.DataFrame({
        'zespol': ['1', '2'],
        'slupek': ['1001', '1002']
    })


def test_get_lines_list(mocked_response_lines):
    with patch('project.collecting_data.timetables_collecting.get_response') as mocked_get_response:
        mocked_get_response.return_value = mocked_response_lines
        lines_list = get_lines_list('1', '1001')
    assert lines_list == ['1', '2']


def test_get_line_timetable(tmp_path, mocked_response_timetables):
    os.makedirs(tmp_path / 'timetables', exist_ok=True)
    with patch('project.collecting_data.timetables_collecting.get_response') as mocked_get_response:
        mocked_get_response.return_value = mocked_response_timetables
        get_line_timetable('1', '1001', '1', tmp_path)
        csv_file_path = tmp_path / 'timetables' / '1_1001_1.csv'
    assert os.path.isfile(csv_file_path)


def test_get_timetables(tmp_path, mocked_response_timetables, mocked_bus_stops_df, monkeypatch):
    os.makedirs(tmp_path / 'timetables', exist_ok=True)
    with patch('project.collecting_data.timetables_collecting.get_lines_list') as mocked_get_lines_list:
        mocked_get_lines_list.return_value = ['1', '2']
        get_timetables(mocked_bus_stops_df, tmp_path)
    csv_file_path = tmp_path / 'timetables' / '1_1001_1.csv'
    assert os.path.isfile(csv_file_path)
    csv_file_path = tmp_path / 'timetables' / '1_1001_2.csv'
    assert os.path.isfile(csv_file_path)


def test_get_lines(tmp_path, monkeypatch):
    os.makedirs(tmp_path / 'timetables', exist_ok=True)
    with open(tmp_path / 'timetables' / '1_1001_1.csv', 'w') as f:
        f.write('brygada,czas\n1,12:00:00\n')
    with open(tmp_path / 'timetables' / '1_1001_2.csv', 'w') as f:
        f.write('brygada,czas\n1,12:00:00\n')

    get_lines(tmp_path)
    assert os.path.isdir(
        tmp_path / 'timetables' / 'lines'), f"Directory {tmp_path / 'timetables' / 'lines'} does not exist"
    csv_file_path = tmp_path / 'timetables' / 'lines' / '1.csv'
    assert os.path.isfile(csv_file_path), f"File {csv_file_path} does not exist"
    csv_file_path = tmp_path / 'timetables' / 'lines' / '2.csv'
    assert os.path.isfile(csv_file_path), f"File {csv_file_path} does not exist"
