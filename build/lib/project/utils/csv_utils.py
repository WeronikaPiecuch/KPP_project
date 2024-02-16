def read_csv_file(filepath):
    with open(f'{filepath}', 'r') as file:
        lines = file.readlines()
        lines = lines[1:]
    return lines


def get_all_vehicles(dir_path):
    vehicles = set()
    lines = read_csv_file(f'{dir_path}/vehicles.csv')
    for line in lines:
        line = line.split(',')
        vehicles.add(int(line[0]))
    return vehicles
