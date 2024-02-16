from math import isclose
from project.utils.coordinates_utils import *
from project.utils.constants import *


def test_geographical_distance():
    lat1, lon1 = 51.0, 21.0
    lat2, lon2 = 51.2, 21.2
    expected_distance = 2640
    distance = geographical_distance(lat1, lon1, lat2, lon2)
    assert isclose(distance, expected_distance, rel_tol=10)


def test_get_approx_lon_lat():
    lat, lon = MIN_LAT, (MIN_LON + MAX_LON) / 2
    expected_approx_lat, expected_approx_lon = 0, NUMBER_OF_LON_POINTS / 2
    approx_lon, approx_lat = get_approx_lon_lat(lon, lat)
    assert approx_lon == expected_approx_lon
    assert approx_lat == expected_approx_lat


def test_get_lon_lat():
    approx_lat, approx_lon = NUMBER_OF_LAT_POINTS / 2, NUMBER_OF_LON_POINTS / 2
    expected_lat, expected_lon = (MIN_LAT + MAX_LAT) / 2, (MIN_LON + MAX_LON) / 2
    lon, lat = get_lon_lat(approx_lon, approx_lat)
    assert lon == expected_lon
    assert lat == expected_lat


def test_get_all_approx_points():
    lon1, lat1 = MAX_LON, MAX_LAT
    lon2, lat2 = MIN_LON, MIN_LAT
    approx_points = get_all_approx_points(lon1, lat1, lon2, lat2)
    assert len(approx_points) == NUMBER_OF_LON_POINTS + 1


def test_init_points_dict():
    points_dict = init_points_dict()
    assert len(points_dict) == (NUMBER_OF_LAT_POINTS + 1) * (NUMBER_OF_LON_POINTS + 1)
