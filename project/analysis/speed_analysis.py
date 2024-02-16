from project.utils.constants import SPEED_LIMIT, WARSAW_CENTER
from project.utils.coordinates_utils import get_lon_lat
from project.utils.vehicles_utils import get_vehicles_speeds, get_vehicles_lines
import folium
import pandas as pd
import os
import matplotlib.pyplot as plt
import shutil


def show_speeds_at_points(speeds_at_points, dir_name, output_dir):
    m = folium.Map(location=WARSAW_CENTER, zoom_start=10)
    for point in speeds_at_points:
        lon, lat = get_lon_lat(point[0], point[1])
        counter_above = 0
        counter_all = 0
        for vehicle in speeds_at_points[point]:
            if speeds_at_points[point][vehicle] > SPEED_LIMIT:
                counter_above += 1
            counter_all += 1
        if counter_all > 0 and counter_above / counter_all > 0.5:
            percent = counter_above / counter_all * 100
            folium.CircleMarker([lat, lon],
                                popup=f'Percent of vehicles above speed limit at point {(lon, lat)}: {percent}%',
                                radius=1).add_to(m)
    m.save(f'{output_dir}/above_limit_map_{dir_name}.html')


def get_average_speeds(vehicles_speeds):
    columns = ['vehicle', 'average_speed', 'distance_sum', 'time_sum']
    average_speeds = {column: [] for column in columns}
    for vehicle, vehicle_speeds_df in vehicles_speeds.items():
        if len(vehicle_speeds_df > 0):
            distance_sum = vehicle_speeds_df['distance'].sum()
            time_sum = vehicle_speeds_df['time'].sum()
        else:
            distance_sum = 0
            time_sum = 0
        if time_sum > 0:
            average_speed = distance_sum / time_sum
        else:
            average_speed = 0
        average_speeds['vehicle'].append(vehicle)
        average_speeds['average_speed'].append(average_speed)
        average_speeds['distance_sum'].append(distance_sum)
        average_speeds['time_sum'].append(time_sum)
    average_speeds_df = pd.DataFrame(average_speeds, columns=columns)
    return average_speeds_df


def get_maximum_speeds(vehicles_speeds):
    columns = ['vehicle', 'maximum_speed']
    maximum_speeds = {column: [] for column in columns}
    for vehicle, vehicle_speeds_df in vehicles_speeds.items():
        if len(vehicle_speeds_df) > 0:
            maximum_speed = vehicle_speeds_df['speed'].max()
        else:
            maximum_speed = 0
        maximum_speeds['vehicle'].append(vehicle)
        maximum_speeds['maximum_speed'].append(maximum_speed)
    maximum_speeds_df = pd.DataFrame(maximum_speeds, columns=columns)
    return maximum_speeds_df


def show_speeds_plots(speeds_for_lines, output_dir, kind):
    speeds_for_lines = speeds_for_lines.sort_values(by='line')
    speeds_for_lines['label'] = speeds_for_lines.index + " (" + speeds_for_lines['number_of_vehicles'].astype(str) + ")"
    unique_first_chars = speeds_for_lines.index.str[0].unique()

    os.mkdir(f'{output_dir}/{kind.lower()}_speeds_plots')

    for char in unique_first_chars:
        subset = speeds_for_lines[speeds_for_lines.index.str.startswith(char)]

        plt.figure(figsize=(15, 10))
        bars = plt.bar(subset.index, subset[f'{kind}_speed'], tick_label=subset['label'], color='skyblue')

        for bar in bars:
            yval = round(bar.get_height(), 1)
            plt.text(bar.get_x() + bar.get_width() / 2, yval, str(yval), va='bottom')

        plt.xlabel('Line')
        plt.ylabel(f'{kind[0].upper() + kind[1:]} Speed (number of vehicles in brackets)')
        plt.title(f'{kind[0].upper() + kind[1:]} Speed for lines starting with "{char}"')
        plt.xticks(rotation=45)
        plt.grid(axis='y')

        plt.tight_layout()

        plt.savefig(f'{output_dir}/{kind.lower()}_speeds_plots/{kind.lower()}_speeds_plot_{char}.png')
        plt.close()


def show_average_speeds(average_speeds_df, vehicles_lines_df, dir_name):
    average_speeds_with_lines = average_speeds_df.merge(vehicles_lines_df, left_on='vehicle', right_index=True)

    average_speeds_with_lines = average_speeds_with_lines[['line', 'distance_sum', 'time_sum']]
    average_speeds_with_lines['number_of_vehicles'] = 1
    average_speeds_for_lines = average_speeds_with_lines.groupby('line').agg(
        {'distance_sum': 'sum', 'time_sum': 'sum', 'number_of_vehicles': 'sum'})
    average_speeds_for_lines['average_speed'] = average_speeds_for_lines['distance_sum'] / average_speeds_for_lines[
        'time_sum']
    average_speeds_for_lines[average_speeds_for_lines['time_sum'] == 0] = 0

    show_speeds_plots(average_speeds_for_lines, dir_name, 'average')


def show_maximum_speeds(maximum_speeds_df, vehicles_lines_df, dir_name):
    maximum_speeds_with_lines = maximum_speeds_df.merge(vehicles_lines_df, left_on='vehicle', right_index=True)

    maximum_speeds_with_lines = maximum_speeds_with_lines[['line', 'maximum_speed']]
    maximum_speeds_with_lines['number_of_vehicles'] = 1
    maximum_speeds_for_lines = maximum_speeds_with_lines.groupby('line').agg(
        {'maximum_speed': 'max', 'number_of_vehicles': 'sum'})

    show_speeds_plots(maximum_speeds_for_lines, dir_name, 'maximum')


def do_speed_analysis(dir_name, output_dir, data_dir):
    output_dir = f'{output_dir}/speed_analysis_results/{dir_name}'
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.mkdir(output_dir)

    dir_path = data_dir + '/online_locations/' + dir_name

    vehicles_speeds, speeds_at_points, correct_measurements, failed_measurements = get_vehicles_speeds(dir_path)
    vehicles_lines_df = get_vehicles_lines(dir_path)

    average_speeds_df = get_average_speeds(vehicles_speeds)
    show_average_speeds(average_speeds_df, vehicles_lines_df, output_dir)

    maximum_speeds_df = get_maximum_speeds(vehicles_speeds)
    show_maximum_speeds(maximum_speeds_df, vehicles_lines_df, output_dir)

    show_speeds_at_points(speeds_at_points, dir_name, output_dir)

    percentage = failed_measurements / (correct_measurements + failed_measurements) * 100
    vehicles_above_limit = len(maximum_speeds_df[maximum_speeds_df['maximum_speed'] > SPEED_LIMIT])
    all_vehicles = len(maximum_speeds_df)

    print(f'Correct measurements: {correct_measurements}')
    print(f'Failed measurements: {failed_measurements}')
    print(f'Percentage of failed measurements: {percentage:.3f}%\n')

    percent = vehicles_above_limit / all_vehicles * 100
    print(
        f'{vehicles_above_limit} of {all_vehicles} ({percent:.3f}%) vehicles exceeded speed limit\n')

    print(f'Analysis results saved in {output_dir} directory\n')
