import time
from datetime import datetime
import os
from project.utils.constants import COLLECTING_TIME
from project.utils.request_utils import get_response


def get_results():
    results = get_response('busestrams_get', {'resource_id': 'f2e5503e927d-4ad3-9500-4ab9e55deb59', 'type': 1})
    if type(results) is not list:
        raise Exception('Error in response from server')
    else:
        return results


def read_result(result):
    result['Time'] = datetime.strptime(result['Time'], '%Y-%m-%d %H:%M:%S').timestamp()
    result_time = result['Time']
    vehicle_number = int(result['VehicleNumber'])
    return result, result_time, vehicle_number


def prepare_files(data_dir):
    start_time = time.time()
    vehicles_last_time = dict()
    vehicles_constant_data = dict()
    data_dir_name = str(datetime.fromtimestamp(start_time))
    data_dir_name = data_dir_name.replace(' ', '_').replace(':', '-')
    data_dir_name = data_dir_name.split('.')[0]
    data_dir_name = f'{data_dir}/online_locations/{data_dir_name}'
    os.mkdir(data_dir_name)

    while True:
        try:
            results = get_results()
            break
        except Exception as e:
            print(e)
            time.sleep(5)

    with open(f'{data_dir_name}/vehicles.csv', 'w') as csv_file:
        csv_file.write('VehicleNumber,Lines,Brigade\n')

        for result in results:
            result, result_time, vehicle_number = read_result(result)

            if result_time > start_time - 60:
                vehicles_last_time[vehicle_number] = result_time
                vehicles_constant_data[vehicle_number] = [result['Lines'], result['Brigade']]

                csv_file.write(f'{vehicle_number},{result["Lines"]},{result["Brigade"]}\n')

            with open(f'{data_dir_name}/{vehicle_number}.csv', 'w') as csv_vehicle_file:
                csv_vehicle_file.write('Time,Lon,Lat\n')

    return vehicles_last_time, vehicles_constant_data, data_dir_name


def collect_result(vehicles_last_time, vehicles_constant_data, data_dir):
    try:
        results = get_results()
        for result in results:
            result, result_time, vehicle_number = read_result(result)
            if vehicle_number in vehicles_last_time:
                if result_time > vehicles_last_time[vehicle_number]:
                    vehicles_last_time[vehicle_number] = result_time
                    with open(f'{data_dir}/{vehicle_number}.csv', 'a') as csv_file:
                        csv_file.write(f'{result["Time"]},{result["Lon"]},{result["Lat"]}\n')
    except Exception:
        time.sleep(5)
    return vehicles_last_time


def collect_data(collecting_time, vehicles_last_time, vehicles_constant_data, data_dir):
    start_time = time.time()
    print('Collecting data...')
    while time.time() - start_time < collecting_time:
        print(f'Collecting data for {int(collecting_time - (time.time() - start_time))} seconds left')
        vehicles_last_time = collect_result(vehicles_last_time, vehicles_constant_data,
                                                                    data_dir)
    end_time = time.time()
    with open(f'{data_dir}/time.txt', 'w') as time_file:
        time_file.write(f'{start_time}\n{end_time}\n')
    return vehicles_last_time, vehicles_constant_data


def collect_online_locations(data_dir):
    vehicles_last_time, vehicles_constant_data, data_dir = prepare_files(data_dir)
    collect_data(COLLECTING_TIME, vehicles_last_time, vehicles_constant_data, data_dir)
    print(f'Data collected in directory: {data_dir}')
