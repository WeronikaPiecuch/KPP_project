import os

# SPEED ANALYSIS
SPEED_LIMIT = 50
FAILURE_LIMIT = 100

PERCENTAGE_ABOVE_LIMIT = 0.5

# COLLECTING DATA
COLLECTING_TIME = 3600  # 1 hour
URL = 'https://api.um.warszawa.pl/api/action/'
APIKEY = 'f0d27023-e36a-4368-bf82-e4431539ed6d'

# GEOGRAPHICAL COORDINATES
MIN_LON = 20.0
MAX_LON = 22.0
NUMBER_OF_LON_POINTS = 2000  # points form 0 to NUMBER_OF_LON_POINTS

MIN_LAT = 51.0
MAX_LAT = 53.0
NUMBER_OF_LAT_POINTS = 2000  # points form 0 to NUMBER_OF_LAT_POINTS

WARSAW_CENTER = [52.237049, 21.017532]

EARTH_RADIUS = 6371009  # in meters

# PUNCTUALITY ANALYSIS
ACCEPTABLE_DISTANCE = 100  # in meters
ACCEPTABLE_DELAY = 60  # in seconds
DELAY_LIMITS = [0, 60, 120, 300, 600, 1800, 3600]  # in seconds
DELAY_LABELS = ["Before time", "On time", "Delay under 2 minutes", "Delay from 2 to 5 minutes",
                "Delay from 5 to 10 minutes", "Delay from 10 to 30 minutes", "Delay from 30 minutes to 1 hour"]
BEFORE_TIME_LIMIT = 600  # in seconds
