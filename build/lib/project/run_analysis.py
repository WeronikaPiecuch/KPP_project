from project.analysis.speed_analysis import do_speed_analysis
from project.analysis.punctuality_analysis import do_punctuality_analysis
import os
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', help='Directory with data to analyze')
    parser.add_argument('--punctuality', action='store_true', help='Perform punctuality analysis')
    parser.add_argument('--speed', action='store_true', help='Perform speed analysis')

    return parser.parse_args()


def main():
    data_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data'))
    output_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../output'))

    args = parse_arguments()
    dir_name = args.dir

    if dir_name in os.listdir(f'{data_dir}/online_locations'):
        print('Directory found')
    else:
        print('Directory not found')
        return

    if not args.punctuality and not args.speed:
        print('No analysis specified')
        return

    if args.speed:
        print('Executing speed analysis...\n')
        do_speed_analysis(dir_name, output_dir, data_dir)

    if args.punctuality:
        print('Executing punctuality analysis...\n')
        do_punctuality_analysis(dir_name, output_dir, data_dir)


if __name__ == '__main__':
    main()
