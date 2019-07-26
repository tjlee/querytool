import argparse
from os import path, listdir
import os
import psutil
import sys
from datetime import datetime


def get_file_contents(file_name):
    with open(file_name, "r") as tmp_file:
        data = tmp_file.read().splitlines()
    return data


def read_files_contents_to_list(path_to_data):
    file_names = map(lambda x: path.join(path_to_data, x), listdir(path_to_data))

    file_contents = []
    for file_name in file_names:
        file_contents.append(get_file_contents(file_name))
    return file_contents


def fill_dictionary(file_records):
    cache_collection = {}

    for file_record in file_records:
        for record in file_record:
            # 1414713603 192.168.0.1 1 14
            timestamp, ip, cpu, usage = record.split(' ')

            if ip not in cache_collection:
                cache_collection[ip] = {cpu: [[timestamp, usage]]}
            else:
                if cpu not in cache_collection[ip]:
                    cache_collection[ip][cpu] = [[timestamp, usage]]
                else:
                    # ip & cpu in collection => append timestamp, usage
                    cache_collection[ip][cpu].append([[timestamp, usage]])

    return cache_collection


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('data_path', default='./tmp/', type=str, help='Generated logs output path')
    args = parser.parse_args()

    raw_data = read_files_contents_to_list(args.data_path)
    cache_dictionary = fill_dictionary(raw_data)

    exit_term = 'EXIT'

    import time

    while True:
        query = input('>')
        if query == exit_term:
            break

        if query.startswith('QUERY'):
            raw_query = query.replace('QUERY ', '').split(' ')
            if len(raw_query) == 6:
                ip, cpu, start, end = \
                    raw_query[0], raw_query[1], raw_query[2] + ' ' + raw_query[3], raw_query[4] + ' ' + raw_query[5]

                start_time = time.time()

                if ip in cache_dictionary:
                    if cpu in cache_dictionary[ip]:

                        print(ip, cpu, start, end)

                        date_format = '%Y-%m-%d %H:%M'

                        try:
                            start_dt = datetime.strptime(start, date_format)
                        except ValueError:
                            print('Start date is invalid. Valid format:{}'.format(date_format))

                        try:
                            end_dt = datetime.strptime(end, date_format)
                        except ValueError:
                            print('End date is invalid. Valid format:{}'.format(date_format))

                        if start_dt > end_dt:
                            print('Start date is greater than end date')

                        delta = end_dt - start_dt

                        first_element = cache_dictionary[ip][cpu][0][0]

                        another_date_format = '%Y-%m-%d %H:%M:%S'
                        first_element_timestap = datetime.utcfromtimestamp(int(first_element)).strftime(
                            another_date_format)

                        begin_delta = start_dt - datetime.strptime(first_element_timestap, another_date_format)

                        # 2014-10-31 00:00
                        # 2014-10-31 00:05

                        print(cache_dictionary[ip][cpu][begin_delta.seconds:delta.seconds])
                        print(ip, cpu, start, end)

                        # CPU1 usage on 192.168.1.10: (2014-10-31 00:00, 90%), (2014-10-31 00:01, 89%), (2014-10-31 00:02, 87%), (2014-10-31 00:03, 94%) (2014-10-31 00:04, 88%)

                else:
                    print(cpu)
                    print('CPU out of range:', cpu)

                print("--- %s seconds ---" % (time.time() - start_time))

            else:
                print('IP out of range:', ip)

        else:
            print('Invalid query format. Valid is "QUERY IP cpu_id time_start time_end"')
