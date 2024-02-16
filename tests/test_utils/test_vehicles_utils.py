import pytest
from unittest.mock import patch
from project.utils.vehicles_utils import *
from project.utils.coordinates_utils import init_points_dict


SAMPLE_CSV_DATA = [
    "1000,21.0,51.0\n",
    "2000,21.1,51.1\n",
    "2010,21.2,51.2\n",
]


@pytest.fixture
def sample_points_on_map():
    return init_points_dict()


@pytest.fixture
def sample_dir_path(tmpdir):
    csv_dir = tmpdir.mkdir("csv")
    csv_path = csv_dir.join("100.csv")
    with open(csv_path, "w") as f:
        f.write("Time,Lon,Lat\n")
        f.writelines(SAMPLE_CSV_DATA)
    return str(csv_dir)


@pytest.fixture
def sample_dir_path_lines(tmpdir):
    csv_dir = tmpdir.mkdir("csv")
    csv_path = csv_dir.join("vehicles.csv")
    sample_data = "VehicleNumber,line,brigade\n100,line1,brigade1\n200,line2,brigade2\n"
    csv_path.write(sample_data)
    return str(csv_dir)

def test_calculate_vehicle_speeds(sample_points_on_map, sample_dir_path):
    vehicle_number = 100
    speeds_df, failed_measurements, points_on_map = calculate_vehicle_speeds(vehicle_number, sample_points_on_map,
                                                                             sample_dir_path)
    assert failed_measurements == 1
    assert len(speeds_df) == 1
    assert points_on_map[(1000, 0)][vehicle_number] > 0


@patch('project.utils.vehicles_utils.calculate_vehicle_speeds')
def test_calculate_all_vehicle_speeds(mock_calculate_vehicle_speeds, sample_points_on_map, sample_dir_path):
    mock_calculate_vehicle_speeds.return_value = (
        pd.DataFrame({'speed': [30, 40, 50]}),
        1,
        sample_points_on_map
    )
    vehicles = ["100", "200"]
    speeds, points_on_map, correct_measurements, failed_measurements = \
        calculate_all_vehicle_speeds(vehicles,
                                     sample_points_on_map,
                                     sample_dir_path)
    assert len(speeds["100"]) == 3
    assert correct_measurements == 6
    assert failed_measurements == 2
    assert (1000, 0) in points_on_map


@patch('project.utils.vehicles_utils.get_all_vehicles')
@patch('project.utils.vehicles_utils.calculate_all_vehicle_speeds')
def test_get_vehicles_speeds(mock_calculate_all_vehicle_speeds, mock_get_all_vehicles, sample_points_on_map,
                             sample_dir_path):
    mock_get_all_vehicles.return_value = ["100", "200"]
    mock_calculate_all_vehicle_speeds.return_value = (
        {"100": pd.DataFrame({'speed': [30, 40, 50]}), "200": pd.DataFrame({'speed': [25, 35, 45]})},  # Speeds dict
        sample_points_on_map,
        6,
        2,
    )
    speeds, points_on_map, correct_measurements, failed_measurements = get_vehicles_speeds(sample_dir_path)
    assert len(speeds) == 2
    assert correct_measurements == 6
    assert failed_measurements == 2
    assert (21.0, 51.0) in points_on_map


def test_kmph_to_mps():
    result = kmph_to_mps(72)
    assert result == 20


def test_mps_to_kmph():
    result = mps_to_kmph(20)
    assert result == 72


def test_get_vehicles_lines(sample_dir_path_lines):
    with patch('pandas.read_csv') as mock_read_csv:
        mock_read_csv.return_value = pd.DataFrame({
            'line': ['line1', 'line2'],
            'brigade': ['brigade1', 'brigade2']
        }, index=['100', '200'])

        vehicles_lines_df = get_vehicles_lines(sample_dir_path_lines)

        assert list(vehicles_lines_df.columns) == ['line', 'brigade']

        assert vehicles_lines_df.index.tolist() == ['100', '200']
        assert vehicles_lines_df.loc['100', 'line'] == 'line1'
        assert vehicles_lines_df.loc['100', 'brigade'] == 'brigade1'
        assert vehicles_lines_df.loc['200', 'line'] == 'line2'
        assert vehicles_lines_df.loc['200', 'brigade'] == 'brigade2'
