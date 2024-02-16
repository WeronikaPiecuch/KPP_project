import os
import pytest
from project.utils.constants import *


def test_speed_analysis_constants():
    assert isinstance(SPEED_LIMIT, int)
    assert isinstance(FAILURE_LIMIT, int)
    assert isinstance(PERCENTAGE_ABOVE_LIMIT, float)


def test_collecting_data_constants():
    assert isinstance(COLLECTING_TIME, int)
    assert isinstance(URL, str)
    assert isinstance(APIKEY, str)


def test_geographical_coordinates_constants():
    assert isinstance(MIN_LON, float)
    assert isinstance(MAX_LON, float)
    assert isinstance(NUMBER_OF_LON_POINTS, int)
    assert isinstance(MIN_LAT, float)
    assert isinstance(MAX_LAT, float)
    assert isinstance(NUMBER_OF_LAT_POINTS, int)
    assert isinstance(WARSAW_CENTER, list)
    assert len(WARSAW_CENTER) == 2
    assert all(isinstance(coord, float) for coord in WARSAW_CENTER)
    assert isinstance(EARTH_RADIUS, int)


def test_punctuality_analysis_constants():
    assert isinstance(ACCEPTABLE_DISTANCE, int)
    assert isinstance(ACCEPTABLE_DELAY, int)
    assert isinstance(DELAY_LIMITS, list)
    assert all(isinstance(limit, int) for limit in DELAY_LIMITS)
    assert isinstance(DELAY_LABELS, list)
    assert all(isinstance(label, str) for label in DELAY_LABELS)
    assert isinstance(BEFORE_TIME_LIMIT, int)
