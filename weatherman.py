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

MONTH_SYMBOL = {
        "1": "Jan", "2": "Feb", "3": "Mar", "4": "Apr", "5": "May", "6": "Jun",
        "7": "Jul", "8": "Aug", "9": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"
    }

def read_files(file_name, my_weatherlist):
    file = open (file_name , "r")
    read = file.read().splitlines()
    for i in range(2, len(read)-1):
        my_weatherlist.append(read[i].split(","))
        read[i].split(",")

def execute_e_argument(my_weatherlist):
    global_max_temp = float('-inf')
    global_min_temp = float('inf')
    highest_humidity = float('-inf')
    max_temp_date = None
    min_temp_date = None
    humidity_date = None

    for line in my_weatherlist:
        try:
            max_temperature = float(line[1])  
            min_temperature = float(line[3])
            humidity = float(line[7])
            date_str = line[0]
            date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")

            if max_temperature > global_max_temp:
                global_max_temp = max_temperature
                max_temp_date =  date_obj
            if min_temperature < global_min_temp:
                global_min_temp = min_temperature
                min_temp_date = date_obj
            if humidity > highest_humidity:
                highest_humidity = humidity
                humidity_date = date_obj

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

    print(f'Highest: {round(global_max_temp)}C on {max_temp_str}')
    print(f'Lowest: {round(global_min_temp)}C on {min_temp_str}')
    print(f'Humidity: {round(highest_humidity)} on {humidity_date_str}')

def execute_a_argument(my_weatherlist):
    temp_dict = {}

    for line in my_weatherlist:
        try:
            date_str = line[0]
            max_temperature = float(line[1])
            min_temperature = float(line[3])
            humidity = float(line[8])
            date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")

            if date_obj not in temp_dict:
                temp_dict[date_obj] = {'temp1' : [],'temp2' : [], 'humidities' : []}

            temp_dict[date_obj]['temp1'].append(max_temperature)
            temp_dict[date_obj]['temp2'].append(min_temperature)
            temp_dict[date_obj]['humidities'].append(humidity)
        except (ValueError, IndexError) as e:
            continue
    
    highest_avg_temp = float('-inf')
    lowest_avg_temp = float('inf')

    for year in temp_dict:
        temp_list1 = temp_dict[year]['temp1']
        temp_list2 = temp_dict[year]['temp2']
        humidity_list = temp_dict[year]['humidities']

        if temp_list1 and temp_list2 and humidity_list:
            avg_temp1 = sum(temp_list1) / len(temp_list1)
            avg_temp2 = sum(temp_list2) / len(temp_list2)
            avg_humidity = sum(humidity_list) / len(humidity_list)

            if avg_temp1 > highest_avg_temp:
                highest_avg_temp = avg_temp1
            if avg_temp2 < lowest_avg_temp:
                lowest_avg_temp = avg_temp2
 
    print(f'Highest Average Temperature: {round(highest_avg_temp)}C')
    print(f'Lowest Average Temperature: {round(lowest_avg_temp)}C')
    print(f'Average Mean Humidity: {round(avg_humidity)}%')

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
            pattern = os.path.join(directory, f"lahore_weather_{year}*")
        files.extend(glob.glob(pattern))

    my_weatherlist = []

    for file_path in files:
        if os.path.exists(file_path):
            try:
                read_files(file_path, my_weatherlist)
            except Exception as e:
                file_path: {e}

    print(year, month)                
    return my_weatherlist

def main():
    parsed_flags = parse_arguments()
    
    for flag, years_month in parsed_flags:
        if flag == '-e':
            my_weatherlist = process_files([years_month], {}, '-e')
            execute_e_argument(my_weatherlist)
        elif flag in ['-a', '-c']:
            year, month = years_month.split('/')
            month = MONTH_SYMBOL[month.lstrip('0')]
            my_weatherlist = process_files([year], {year: month}, flag, year, month)
            if flag == '-a':
                execute_a_argument(my_weatherlist)
            elif flag == '-c':
                execute_c_argument(my_weatherlist, year, month)
        
if __name__ == "__main__":
    main()
