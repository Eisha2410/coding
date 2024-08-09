import os
import glob
import sys
import datetime
from colorama import Fore, Style

def parse_arguments():
    args = sys.argv[1:]
    if not args:
        sys.exit("error: no arguments provided")

    parsed_flag = [] 
    i = 0

    while i < len(args):
        flag = args[i]
        if flag not in [ '-e', '-a', '-c']:
            sys.exit(f"error: invalid flag {flag}")
        i += 1

        if i >= len(args):
            sys.exit(f"error: missing year/month after {flag}")
    
        years_month = args[i]
        if flag == '-e' and '/' in years_month:
            sys.exit("error: -e flag requires only one year")
        elif flag in ['-a', '-c'] and '/' not in years_month:
            sys.exit(f"error: {flag} flag requires year/month ")

        parsed_flag.append((flag, years_month))
        i += 1

    return parsed_flag

def map_months(years_month): 
    month_symbol = {
        "1": "Jan", "2": "Feb", "3": "Mar", "4": "Apr", "5": "May", "6": "Jun",
        "7": "Jul", "8": "Aug", "9": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"
    }

    year, month = years_month.split('/')
    month = month.lstrip('0')
    if month not in month_symbol:
        sys.exit("error: Invalid month in argument")

    return year, month_symbol[month]

def read_files(file_name, my_weatherlist):
    file = open (file_name , "r")
    read = file.read().splitlines()
    for i in range(2, len(read)-1):
        my_weatherlist.append(read[i].split(","))
        read[i].split(",")

def data_execution(my_weatherlist, flag, year=None, month=None):
    if flag == '-e':
        execute_e_argument(my_weatherlist)
    elif flag == '-a':
        execute_a_argument(my_weatherlist)
    elif flag == '-c':
        execute_c_argument(my_weatherlist, year, month)

def execute_e_argument(my_weatherlist):
    global_max_temp = float('-inf')
    global_min_temp = float('inf')
    highest_humidity = float('-inf')
    humidity_count = 0
    humidity_percentage = 0
    max_temp_date = None
    min_temp_date = None
    humidity_date = None

    for line in my_weatherlist:
        try:
            temperature = float(line[1])  
            humidity = float(line[-1])
            date_str = line[0]
            date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")

            if temperature > global_max_temp:
                global_max_temp = temperature
                max_temp_date =  date_obj
            if temperature < global_min_temp:
                global_min_temp = temperature
                min_temp_date = date_obj
            if humidity > highest_humidity:
                highest_humidity = humidity 
                humidity_date = date_obj

            humidity_percentage += humidity
            humidity_count += 1
            humidity_percentage = (humidity/highest_humidity)* 100.0

        except (ValueError, IndexError) as e:
            continue
    if max_temp_date:
        max_temp_str = max_temp_date.strftime("%B %d")
    else:
        max_temp_str = "N/A"

    if min_temp_date:
        min_temp_str = min_temp_date.strftime("%B %d")
    else:
        min_temp_str = "N/A"

    if humidity_date:
        humidity_date_str = humidity_date.strftime("%B %d")
    else:
        humidity_date_str = "N/A"

    print(f'Highest: {global_max_temp} on {max_temp_str}')
    print(f'Lowest: {global_min_temp} on {min_temp_str}')
    print(f'Humidity: {humidity_percentage} on {humidity_date_str}')

def execute_a_argument(my_weatherlist):
    temp_dict = {}

    for line in my_weatherlist:
        try:
            date_str = line[0]
            temperature = float(line[1])
            humidity = float(line[-1])
            date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            year = date_obj.year

            if year not in temp_dict:
                temp_dict[year] = {'temp' : [], 'humidities' : []}

            temp_dict[year]['temp'].append(temperature)
            temp_dict[year]['humidities'].append(humidity)
        except (ValueError, IndexError) as e:
            continue
    
    highest_avg_temp = float('-inf')
    lowest_avg_temp = float('inf')
    total_humidity_sum = 0
    total_humidity_count = 0

    for year in temp_dict:
        temp_list = temp_dict[year]['temp']
        humidity_list = temp_dict[year]['humidities']

        if temp_list and humidity_list:
            avg_temp = sum(temp_list) / len(temp_list)
            avg_humidity = sum(humidity_list) / len(humidity_list)

            if avg_temp > highest_avg_temp:
                highest_avg_temp = avg_temp
            if avg_temp < lowest_avg_temp:
                lowest_avg_temp = avg_temp

            total_humidity_sum += sum(humidity_list)
            total_humidity_count += len(humidity_list)
    
    if total_humidity_count == 0:
        avg_humidity_percentage = 0
    else:
        avg_humidity_percentage = total_humidity_sum / total_humidity_count

    print(f'Highest Average Temperature: {round(highest_avg_temp)}')
    print(f'Lowest Average Temperature: {round(lowest_avg_temp)}')
    print(f'Average Mean Humidity Percentage: {avg_humidity_percentage:.2f}%')

def execute_c_argument(my_weatherlist, year, month):
    days = {}
    
    for line in my_weatherlist:
        try:
            date_str = line[0]
            low_temp = float(line[2])
            high_temp = float(line[1])
            date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            if date_obj.year == int(year) and date_obj.strftime('%b') == month:
                day = date_obj.day
                if day not in days:
                    days[day] ={ 'high': [], 'low': []}
                days[day]['high'].append(high_temp)
                days[day]['low'].append(low_temp)
        except (ValueError, IndexError) as e:
            continue
    
    for day in sorted(days):
        high_temp = max(days[day]['high'])
        low_temp = min(days[day]['low'])

        high_plus_sign = Fore.RED + "+" * int(high_temp) + Style.RESET_ALL
        low_plus_sign = Fore.BLUE + "+" * int(low_temp) + Style.RESET_ALL

        print(f'{day:02d} {high_plus_sign} {high_temp}C')
        print(f'{day:02d} {low_plus_sign} {low_temp}C')

def process_files(years, months, flag, year=None, month=None):
    directory = "./weatherdata"
    files = []
    for year in years:
        if flag == '-a' and year in months:
                pattern = os.path.join(directory, f"lahore_weather_{year}_{months[year]}*")
        elif flag == '-c':
            pattern = os.path.join(directory, f"lahore_weather_{year}_{month}*")
        else:
            pattern = os.path.join(directory, f"lahore_weather_{years}*")
        files.extend(glob.glob(pattern))

    my_weatherlist = []

    for file_path in files:
        if os.path.exists(file_path):
            try:
                read_files(file_path, my_weatherlist)
            except Exception as e:
                file_path: {e}

    data_execution(my_weatherlist, flag, year, month)

def main():
    parsed_flags = parse_arguments()
    
    for flag, years_month in parsed_flags:
        if flag == '-e':
            process_files([years_month], {}, '-e')
        elif flag == '-a':
            year, month = map_months(years_month)
            process_files([year], {year: month}, '-a')
        elif flag == '-c':
            year, month = map_months(years_month)
            process_files([year], {year: month}, '-c', year, month)

if __name__ == "__main__":
    main()
