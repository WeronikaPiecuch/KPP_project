import os
import pytest
from project.utils.csv_utils import *


@pytest.fixture
def sample_csv_file(tmp_path):
    sample_data = "vehicle,line,brigade\n1,100,01\n2,200,01"
    sample_csv_path = tmp_path / 'vehicles.csv'
    with open(sample_csv_path, 'w') as file:
        file.write(sample_data)
    return sample_csv_path


def test_read_csv_file(sample_csv_file):
    lines = read_csv_file(sample_csv_file)
    assert len(lines) == 2
    assert lines[0].strip() == "1,100,01"
    assert lines[1].strip() == "2,200,01"


def test_get_all_vehicles(sample_csv_file):
    vehicles = get_all_vehicles(os.path.dirname(sample_csv_file))
    assert vehicles == {1, 2}
