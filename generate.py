import argparse
import ipaddress
import os
import random
from datetime import datetime, timedelta


def utc_to_timestamp(time):
    return int((time - datetime(1970, 1, 1)).total_seconds())


def get_ip_range(servers_count=1000):
    assert servers_count < 65536, '''Assuming we're working within 192.168.0.0/16 network'''
    return [str(ip) for ip in ipaddress.IPv4Network('192.168.0.0/16')][0:servers_count]


def get_random_cpu_usage():
    return random.randrange(0, 101)


def write_to_named_file(data_dir, file_name, lines):
    tmp_file = os.path.join(data_dir, file_name)
    with open(tmp_file, 'w+') as f:
        f.write('\n'.join(str(tick_line) for tick_line in lines))


def get_seconds_in_range(start_time=datetime.utcnow(), delta=timedelta(days=1)):
    return [str(i) for i in range(utc_to_timestamp(start_time), utc_to_timestamp(start_time + delta))]


def get_minutes_in_range(start_time=datetime.utcnow(), delta=timedelta(days=1)):
    return [str(i) for i in range(utc_to_timestamp(start_time), utc_to_timestamp(start_time + delta), 60)]


def generate_sample_data(timestamp_ticks, servers_count=1000, cpu_per_server=2):
    output_string_format = '''{} {} {} {}'''
    result = []

    ips = get_ip_range(servers_count)

    for tick in timestamp_ticks:
        for ip in ips:
            for cpu in range(cpu_per_server):
                result.append(output_string_format.format(tick, ip, cpu, get_random_cpu_usage()))

    return result


def print_progress_bar(iteration, total, decimals=1, length=100, fill='█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print('\r|%s| %s%%' % (bar, percent), end='\r')
    if iteration == total:
        print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generates sample logs for one day (default 2014-10-31)')
    parser.add_argument('data_path', type=str, help='Generated logs output path')
    args = parser.parse_args()

    assert os.path.exists(args.data_path), 'Nonexistent directory'

    all_minutes_in_day = get_minutes_in_range(start_time=datetime(year=2014, month=10, day=31), delta=timedelta(days=1))

    minutes_in_day = 1440

    for per_minute_in_day in range(0, minutes_in_day):
        print_progress_bar(per_minute_in_day, minutes_in_day - 1)

        current_minute = all_minutes_in_day[per_minute_in_day]
        data = generate_sample_data([current_minute], servers_count=1000)

        filename = str(current_minute) + '.log'
        write_to_named_file(args.data_path, filename, data)
