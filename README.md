# Analysis of the operation of city buses in Warsaw
### *Author:* Weronika Piecuch, University of Warsaw

## Collecting data
To collect data use `collect_data.py` with options from: --download-bus-stops, --download-timetables, --collect-online-locations

## Analysis
To analyze data use `run_analysis.py` with name of dir (in format `YYYY-MM-DD_HH-MM-SS`, eg. `2024-02-15_08-03-56`) with collected online locations (dir should be in location `data/online_locations/`) with options from: --punctuality, --speed.
