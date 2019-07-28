import argparse
import os
from datetime import datetime
from os import path, listdir


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
                cache_collection[ip] = {}
                cache_collection[ip][cpu] = []
                cache_collection[ip][cpu].append([[timestamp, usage]])
            else:
                if cpu not in cache_collection[ip]:
                    cache_collection[ip][cpu] = [[timestamp, usage]]
                else:
                    # ip & cpu in collection => append timestamp, usage
                    cache_collection[ip][cpu].append([[timestamp, usage]])

    return cache_collection


def process_query(query):
    pass


def parse_query(query, query_token='QUERY', date_format='%Y-%m-%d %H:%M'):
    if query.startswith(query_token):
        raw_query = query.replace(query_token, '').split(' ')
        if len(raw_query) == 6:
            ip, cpu, start, end = \
                raw_query[0], raw_query[1], raw_query[2] + ' ' + raw_query[3], raw_query[4] + ' ' + raw_query[5]

            try:
                start_dt = datetime.strptime(start, date_format)
            except ValueError:
                print('Start date is invalid. Valid format:{}'.format(date_format))
                return
            try:
                end_dt = datetime.strptime(end, date_format)
            except ValueError:
                print('End date is invalid. Valid format:{}'.format(date_format))
                return

            return ip, cpu, start_dt, end_dt

    print('Invalid query format. Valid is "%s IP cpu_id time_start time_end"' % query_token)
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('data_path', default='./tmp/', type=str, help='Generated logs output path')
    args = parser.parse_args()

    assert os.path.exists(args.data_path), 'Nonexistent directory'
    raw_data = read_files_contents_to_list(args.data_path)
    cache_dictionary = fill_dictionary(raw_data)

    exit_term = 'EXIT'

    while True:
        query = input('>')
        if query == exit_term:
            break

        if query.startswith('QUERY'):
            raw_query = query.replace('QUERY ', '').split(' ')
            if len(raw_query) == 6:
                ip, cpu, start, end = \
                    raw_query[0], raw_query[1], raw_query[2] + ' ' + raw_query[3], raw_query[4] + ' ' + raw_query[5]

                if ip in cache_dictionary:
                    if cpu in cache_dictionary[ip]:

                        date_format = '%Y-%m-%d %H:%M'

                        start_is_valid = True
                        try:
                            start_dt = datetime.strptime(start, date_format)
                        except ValueError:
                            start_is_valid = False
                            print('Start date is invalid. Valid format:{}'.format(date_format))

                        end_is_valid = True
                        try:
                            end_dt = datetime.strptime(end, date_format)
                        except ValueError:
                            end_is_valid = False
                            print('End date is invalid. Valid format:{}'.format(date_format))

                        if start_is_valid and end_is_valid:
                            if cache_dictionary[ip][cpu]:
                                if cache_dictionary[ip][cpu][0]:
                                    delta = end_dt - start_dt
                                    first_element = cache_dictionary[ip][cpu][0][0]

                                    first_element_timestap = datetime.utcfromtimestamp(int(first_element)).strftime(date_format)

                                    begin_delta = start_dt - datetime.strptime(first_element_timestap, date_format)

                                    start_position = int(begin_delta.total_seconds() / 60)
                                    end_position = int(delta.total_seconds() / 60) + start_position

                                    tmp_list = cache_dictionary[ip][cpu][start_position:end_position]

                                    printable = []

                                    is_slice_issue = False
                                    for i in tmp_list:
                                        if not is_slice_issue and begin_delta.seconds == 0:
                                            printable.append([datetime.utcfromtimestamp(int(i[0])).strftime(date_format), i[1]])
                                            is_slice_issue = True
                                            continue
                                        printable.append([datetime.utcfromtimestamp(int(i[0][0])).strftime(date_format), i[0][1]])

                                    print('CPU{} usage on {}:'.format(cpu, ip) + ', '.join('({}, {}%)'.format(*k) for k in printable))
                    else:
                        print('CPU out of range:', cpu)
                else:
                    print('IP out of range:', ip)
            else:
                print('Invalid query format. Valid is "QUERY IP cpu_id time_start time_end"')
        else:
            print('Invalid query format. Valid is "QUERY IP cpu_id time_start time_end"')