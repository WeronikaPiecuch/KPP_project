import argparse
import os
from project.collecting_data.bus_stops_collecting import download_bus_stops
from project.collecting_data.timetables_collecting import collect_timetables
from project.collecting_data.online_locations_collecting import collect_online_locations


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('--download-bus-stops', action='store_true', help='Download bus stops data')
    parser.add_argument('--download-timetables', action='store_true', help='Download timetables data')
    parser.add_argument('--collect-online-locations', action='store_true', help='Collect online locations data')

    return parser.parse_args()


def main():
    data_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data'))
    args = parse_arguments()

    if not args.download_bus_stops and not args.download_timetables and not args.collect_online_locations:
        print('No arguments provided, use --help for more information')
        return

    if args.download_bus_stops:
        download_bus_stops(data_dir)

    if args.download_timetables:
        collect_timetables(data_dir)

    if args.collect_online_locations:
        collect_online_locations(data_dir)


if __name__ == '__main__':
    main()
