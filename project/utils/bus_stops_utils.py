import pandas as pd


def get_bus_stops(data_dir):
    bus_stops_df = pd.read_csv(f'{data_dir}/bus_stops.csv')
    return bus_stops_df
