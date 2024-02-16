from math import radians, cos, sqrt
from project.utils.constants import MIN_LAT, MAX_LAT, MIN_LON, MAX_LON, NUMBER_OF_LON_POINTS, NUMBER_OF_LAT_POINTS, \
    EARTH_RADIUS
from project.utils.csv_utils import read_csv_file, get_all_vehicles


def geographical_distance(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(float, [lat1, lon1, lat2, lon2])
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    mlat = (lat1 + lat2) / 2
    distance = EARTH_RADIUS * sqrt(dlat ** 2 + (cos(mlat) * dlon) ** 2)
    return distance


def get_approx_lon_lat(lon, lat):
    approx_lon = int((lon - MIN_LON) / (MAX_LON - MIN_LON) * NUMBER_OF_LON_POINTS)
    approx_lat = int((lat - MIN_LAT) / (MAX_LAT - MIN_LAT) * NUMBER_OF_LAT_POINTS)
    return approx_lon, approx_lat


def get_lon_lat(approx_lon, approx_lat):
    lon = approx_lon / NUMBER_OF_LON_POINTS * (MAX_LON - MIN_LON) + MIN_LON
    lat = approx_lat / NUMBER_OF_LAT_POINTS * (MAX_LAT - MIN_LAT) + MIN_LAT
    return lon, lat


def get_all_approx_points(lon1, lat1, lon2, lat2):
    approx_points = set()
    approx_lon1, approx_lat1 = get_approx_lon_lat(lon1, lat1)
    approx_lon2, approx_lat2 = get_approx_lon_lat(lon2, lat2)
    approx_points.add((approx_lon1, approx_lat1))
    approx_points.add((approx_lon2, approx_lat2))
    if abs(approx_lon1 - approx_lon2) > 1:
        if approx_lon1 > approx_lon2:
            approx_lon1, approx_lon2 = approx_lon2, approx_lon1
            approx_lat1, approx_lat2 = approx_lat2, approx_lat1
        for i in range(approx_lon1 + 1, approx_lon2):
            approx_lat = int(
                approx_lat1 + (approx_lat2 - approx_lat1) * (i - approx_lon1) / (approx_lon2 - approx_lon1))
            approx_points.add((i, approx_lat))
    return approx_points


def init_points_dict():
    points = dict()
    for lon in range(NUMBER_OF_LON_POINTS + 1):
        for lat in range(NUMBER_OF_LAT_POINTS + 1):
            points[(lon, lat)] = dict()
    return points
