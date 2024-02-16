import json
import pandas as pd
from project.utils.request_utils import get_response


def download_bus_stops(data_dir):
    response = get_response('dbstore_get', {'id': 'ab75c33d-3a26-4342-b36a-6e5fef0a3ac3'})
    with open(f'{data_dir}/bus_stops.json', 'w') as file:
        json.dump(response, file, indent=4)

    print(f'Bus stops data downloaded and saved to {data_dir}/bus_stops.json')

    bus_stops = response
    for i in range(len(bus_stops)):
        values = bus_stops[i]['values']
        bus_stops[i] = {values[j]['key']: values[j]['value'] for j in range(len(values))}
    columns = ['zespol', 'slupek', 'szer_geo', 'dlug_geo']
    bus_stops_dict = {column: [] for column in columns}
    for stop in bus_stops:
        for column in columns:
            bus_stops_dict[column].append(stop[column])

    bus_stops_df = pd.DataFrame(bus_stops_dict, columns=columns)
    bus_stops_df.columns = ['zespol', 'slupek', 'lat', 'lon']
    bus_stops_df.to_csv(f'{data_dir}/bus_stops.csv', index=False)

    print(f'Bus stops data downloaded and saved to {data_dir}/bus_stops.csv')
