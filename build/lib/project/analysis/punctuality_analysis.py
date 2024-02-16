from project.utils.vehicles_utils import get_vehicles_lines
from project.utils.coordinates_utils import geographical_distance
from project.utils.constants import ACCEPTABLE_DISTANCE, BEFORE_TIME_LIMIT, DELAY_LIMITS, DELAY_LABELS
from project.utils.bus_stops_utils import get_bus_stops
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import os
import shutil


def read_start_end_time(dir_path):
    with open(f'{dir_path}/time.txt', 'r') as file:
        start_time = file.readline()
        end_time = file.readline()
    start_time = float(start_time[:-1])
    end_time = float(end_time[:-1])
    start_time = pd.to_datetime(start_time, unit='s').tz_localize('UTC').tz_convert('Europe/Warsaw')
    end_time = pd.to_datetime(end_time, unit='s').tz_localize('UTC').tz_convert('Europe/Warsaw')
    start_time, end_time = start_time.time(), end_time.time()
    return start_time, end_time


def get_day_date(dir_path):
    return dir_path.split('/')[-1].split('_')[0]


def get_timetable(stop_id, stop_nr, line, brigade, start_time, end_time, data_dir):
    timetable = pd.read_csv(f'{data_dir}/timetables/{stop_id}_{stop_nr}_{line}.csv')
    timetable = timetable[timetable['brygada'].astype(str) == str(brigade)]
    timetable['czas'] = (timetable['czas'].str.split(':').apply(lambda x: int(x[0]) % 24)).astype(str) + ':' + \
        timetable['czas'].str.split(':').apply(lambda x: x[1]) + ':' + timetable['czas'].str.split(':') \
        .apply(lambda x: x[2])
    timetable['czas'] = pd.to_datetime(timetable['czas'], format='%H:%M:%S')
    timetable['czas'] = timetable['czas'].apply(lambda x: x.time())    

    if len(timetable) == 0:
        return timetable

    if start_time > end_time:
        timetable = timetable[(timetable['czas'] >= start_time) | (timetable['czas'] <= end_time)]
    else:
        timetable = timetable[(timetable['czas'] >= start_time) & (timetable['czas'] <= end_time)]

    return timetable


def get_stop_time(stop, day_date):
    stop_time = stop['czas']
    stop_time = datetime.strptime(f'{day_date} {stop_time}', '%Y-%m-%d %H:%M:%S')
    stop_time = stop_time.timestamp()
    return stop_time


def punctuality_of_vehicle(dir_path, vehicle, vehicles_lines, bus_stops_for_lines, start_time, end_time, data_dir):
    line = vehicles_lines.loc[vehicle, 'line']
    brigade = vehicles_lines.loc[vehicle, 'brigade']

    vehicle_data = pd.read_csv(f'{dir_path}/{vehicle}.csv')

    day_date = get_day_date(dir_path)
    bus_stops = bus_stops_for_lines[line]

    under_delay_limits = {delay: 0 for delay in DELAY_LIMITS}

    for _, bus_stop in bus_stops.iterrows():
        stop_id = bus_stop['zespol']
        stop_nr = bus_stop['slupek']

        timetable = get_timetable(stop_id, stop_nr, line, brigade, start_time, end_time, data_dir)

        for _, stop in timetable.iterrows():
            stop_time = get_stop_time(stop, day_date)

            for _, vehicle_row in vehicle_data.iterrows():
                if vehicle_row['Time'] < stop_time - BEFORE_TIME_LIMIT:
                    continue

                distance = geographical_distance(vehicle_row['Lon'], vehicle_row['Lat'], bus_stop['lon'],
                                                 bus_stop['lat'])

                if distance < ACCEPTABLE_DISTANCE:
                    delay = vehicle_row['Time'] - stop_time
                    for delay_limit in DELAY_LIMITS:
                        if delay < delay_limit:
                            under_delay_limits[delay_limit] += 1
                            break
                    break

    return under_delay_limits


def get_lines_list(vehicles_lines):
    lines = vehicles_lines['line'].unique()
    return lines


def get_bus_stops_for_lines(lines, data_dir):
    bus_stops = get_bus_stops(data_dir)
    bus_stops['zespol/slupek'] = bus_stops['zespol'].astype(str) + '/' + bus_stops['slupek'].astype(str)

    bus_stops_for_lines = dict()

    for line in lines:
        bus_stops_for_lines[line] = pd.read_csv(f'{data_dir}/timetables/lines/{line}.csv', header=0, dtype=str)
        bus_stops_for_lines[line].columns = ['zespol', 'slupek']
        bus_stops_for_lines[line]['zespol/slupek'] = bus_stops_for_lines[line]['zespol'].astype(str) + '/' + \
            bus_stops_for_lines[line]['slupek'].astype(str)
        bus_stops_for_lines[line] = bus_stops[
            bus_stops['zespol/slupek'].isin(bus_stops_for_lines[line]['zespol/slupek'])]

    return bus_stops_for_lines


def punctuality_of_vehicles(dir_path, data_dir):
    vehicles_lines = get_vehicles_lines(dir_path)

    vehicles = vehicles_lines.index
    lines = get_lines_list(vehicles_lines)

    bus_stops_for_lines = get_bus_stops_for_lines(lines, data_dir)

    start_time, end_time = read_start_end_time(dir_path)

    delays = {delay: [] for delay in DELAY_LIMITS}
    delays['line'] = []
    delays['brigade'] = []

    for i, vehicle in enumerate(vehicles, 1):
        vehicle_delays = punctuality_of_vehicle(dir_path, vehicle, vehicles_lines, bus_stops_for_lines, start_time,
                                                end_time, data_dir)
        for delay in DELAY_LIMITS:
            delays[delay].append(vehicle_delays[delay])
        delays['line'].append(vehicles_lines.loc[vehicle, "line"])
        delays['brigade'].append(vehicles_lines.loc[vehicle, "brigade"])
        if i % 100 == 0:
            print(f'Calculated punctuality for {i} out of {len(vehicles)} vehicles.')

    delays_df = pd.DataFrame(delays, index=vehicles)

    return delays_df


def get_punctuality_plot(delays_df, output_dir):
    aggregate_dict = {delay: 'sum' for delay in DELAY_LABELS}
    aggregate_dict['brigade'] = 'count'
    delays_for_lines = delays_df.groupby('line').agg(aggregate_dict)
    for delay in DELAY_LABELS:
        delays_for_lines[delay] = delays_for_lines[delay] / delays_for_lines['brigade']

    unique_first_chars = delays_for_lines.index.str[0].unique()

    os.mkdir(f'{output_dir}/punctuality_plots')

    for first_char in unique_first_chars:
        title = f'Average number of bus stops for each delay for vehicles on lines starting with {first_char}'
        delays_for_lines[delays_for_lines.index.str[0] == first_char].plot(kind='bar', stacked=True,
                                                                           y=list(DELAY_LABELS),
                                                                           title=title,
                                                                           figsize=(15, 10), legend=True,
                                                                           colormap=matplotlib.cm.get_cmap('RdYlGn_r'))
        plt.savefig(f'{output_dir}/punctuality_plots/punctuality_plot_{first_char}.png')


def do_punctuality_analysis(dir_name, output_dir, data_dir):
    output_dir = f'{output_dir}/punctuality_analysis_results/{dir_name}'
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.mkdir(output_dir)

    dir_path = data_dir + '/online_locations/' + dir_name

    delays = punctuality_of_vehicles(dir_path, data_dir)
    delays[DELAY_LABELS] = delays[DELAY_LIMITS]
    delays.drop(DELAY_LIMITS, axis=1, inplace=True)

    delays.to_csv(f'{output_dir}/punctuality.csv')
    delays = delays[['line', 'brigade'] + DELAY_LABELS]

    get_punctuality_plot(delays, output_dir)

    print(f'\nPunctuality analysis for {dir_name} completed.')
    print(f'Results saved in {output_dir}.')
    print(f'Note: An empty graph for a given line means that no bus arrived at any stop.')
