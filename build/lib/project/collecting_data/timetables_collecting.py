import pandas as pd
import time
from project.utils.request_utils import get_response
from project.utils.bus_stops_utils import get_bus_stops
import os


def get_lines_list(stop_id, stop_nr):
    response = get_response('dbtimetable_get',
                            {'id': '88cd555f-6f31-43ca-9de4-66c479ad5942', 'busstopId': stop_id, 'busstopNr': stop_nr})
    lines_list = []
    for line in response:
        lines_list.append(line['values'][0]['value'])
    return lines_list


def get_line_timetable(stop_id, stop_nr, line, data_dir):
    timetable = get_response('dbtimetable_get',
                             {'id': 'e923fa0e-d96c-43f9-ae6e-60518c9f3238', 'busstopId': stop_id, 'busstopNr': stop_nr,
                              'line': line})
    columns = ['brygada', 'czas']
    timetable_dict = {column: [] for column in columns}
    for i in range(len(timetable)):
        for j in range(len(timetable[i]['values'])):
            column = timetable[i]['values'][j]['key']
            if column in columns:
                value = timetable[i]['values'][j]['value']
                timetable_dict[column].append(value)
    timetable_df = pd.DataFrame(timetable_dict, columns=columns)
    timetable_df.to_csv(f'{data_dir}/timetables/{stop_id}_{stop_nr}_{line}.csv', index=False)


def get_timetables(bus_stops_df, data_dir):
    start_time = time.time()
    for i in range(len(bus_stops_df)):
        stop_id = bus_stops_df['zespol'][i]
        stop_nr = bus_stops_df['slupek'][i]
        lines = get_lines_list(stop_id, stop_nr)
        for line in lines:
            get_line_timetable(stop_id, stop_nr, line, data_dir)
        text = f'Successfully collected timetables for bus stop {stop_id} - {stop_nr},'
        text += f'completed {i + 1} out of {len(bus_stops_df)} stops in {time.time() - start_time} seconds.'
        print(text)
    print(f'Successfully collected timetables for all bus stops in {time.time() - start_time} seconds.')


def get_lines(data_dir):
    files = os.listdir(f'{data_dir}/timetables')
    stops_for_lines = dict()
    if 'lines' in files:
        files.remove('lines')
    else:
        os.mkdir(f'{data_dir}/timetables/lines')
    for file in files:
        print(file)
        filename = file.split('.')[0]
        stop_id, stop_nr, line = filename.split('_')
        if line in stops_for_lines:
            stops_for_lines[line].append((stop_id, stop_nr))
        else:
            stops_for_lines[line] = [(stop_id, stop_nr)]
    for line in stops_for_lines:
        bus_stops = stops_for_lines[line]
        bus_stops_df = pd.DataFrame(bus_stops, columns=['zespol', 'slupek'])
        bus_stops_df.to_csv(f'{data_dir}/timetables/lines/{line}.csv', index=False)


def collect_timetables(data_dir):
    bus_stops_df = get_bus_stops(data_dir)
    get_timetables(bus_stops_df, data_dir)
    get_lines(data_dir)
