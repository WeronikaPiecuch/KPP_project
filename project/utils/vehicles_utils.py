from project.utils.csv_utils import read_csv_file, get_all_vehicles
from project.utils.coordinates_utils import geographical_distance, get_all_approx_points, init_points_dict
from project.utils.constants import FAILURE_LIMIT
import pandas as pd


def mps_to_kmph(mps):
    return mps * 3.6


def kmph_to_mps(kmph):
    return kmph / 3.6


def calculate_vehicle_speeds(vehicle_number, points_on_map, dir_path):
    lines = read_csv_file(f'{dir_path}/{vehicle_number}.csv')
    columns = ['speed', 'distance', 'time']
    speeds_dict = {column: [] for column in columns}

    failed_measurements = 0

    for i in range(1, len(lines)):
        line1 = lines[i - 1].split(',')
        line2 = lines[i].split(',')
        time1, lon1, lat1 = float(line1[0]), float(line1[1]), float(line1[2])
        time2, lon2, lat2 = float(line2[0]), float(line2[1]), float(line2[2])

        distance = geographical_distance(lat1, lon1, lat2, lon2)
        time = time2 - time1
        speed = mps_to_kmph(distance / time)

        if speed <= FAILURE_LIMIT:
            speeds_dict['speed'].append(speed)
            speeds_dict['distance'].append(distance)
            speeds_dict['time'].append(time)
            approx_points = get_all_approx_points(lon1, lat1, lon2, lat2)
            for (lon, lat) in approx_points:
                if vehicle_number not in points_on_map[(lon, lat)] or points_on_map[(lon, lat)][vehicle_number] < speed:
                    points_on_map[(lon, lat)][vehicle_number] = speed
        else:
            failed_measurements += 1

    speeds_df = pd.DataFrame(speeds_dict, columns=columns)
    return speeds_df, failed_measurements, points_on_map


def calculate_all_vehicle_speeds(vehicles, points_on_map, dir_path):
    speeds = dict()
    failed_measurements = 0
    correct_measurements = 0
    for vehicle in vehicles:
        speeds[vehicle], failed, points_on_map = calculate_vehicle_speeds(vehicle, points_on_map, dir_path)
        failed_measurements += failed
        correct_measurements += len(speeds[vehicle])
    return speeds, points_on_map, correct_measurements, failed_measurements


def get_vehicles_speeds(dir_path):
    vehicles = get_all_vehicles(dir_path)
    points_on_map = init_points_dict()
    return calculate_all_vehicle_speeds(vehicles, points_on_map, dir_path)


def get_vehicles_lines(dir_path):
    vehicles_lines_df = pd.read_csv(f'{dir_path}/vehicles.csv', index_col=0)
    vehicles_lines_df.columns = ['line', 'brigade']
    return vehicles_lines_df
