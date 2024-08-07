import os
import glob
import sys
import datetime
import matplotlib.pyplot as plt
import numpy as np

def parse_arguments():
    if len(sys.argv) < 3:
        sys.exit(1)

    flag = sys.argv[1]
    if flag not in['-e', '-a', '-c']: 
        sys.exit(1)
    
    years_month = sys.argv[2:]
    if flag == '-e' and len(years_month) != 1:
        sys.exit("error: -e flag requires only one year")
    elif flag == '-a'and len(years_month) != 1:
        sys.exit("error: -a flag requires one year/month ")
    elif flag == '-c' and len(years_month) != 1:
        sys.exit("error: -c flag requires one year/twodigitmonth ")


    return flag, years_month

def map_months(years_month): 
    month_symbol = {
        "1": "Jan", "2": "Feb", "3": "Mar", "4": "Apr", "5": "May", "6": "Jun",
        "7": "Jul", "8": "Aug", "9": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"
    }

    years = []
    months = {}
    for ym in years_month:
        if '/' in ym:
            year, month = ym.split('/')
            month = month.lstrip('0')
            if month not in month_symbol:
                sys.exit(1)
            years.append(year)
            months[year] = month_symbol[month]
        else:
            sys.exit("error: -a flag requires year/month in argument")
    return years, months

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
    total_avg_humidity = 0
    year_count = 0

    for year in temp_dict:
        avg_temp = sum(temp_dict[year]['temp']) / len(temp_dict[year]['temp'])
        avg_humidity = sum(temp_dict[year]['humidities']) / len(temp_dict[year]['humidities'])

        if avg_temp > highest_avg_temp:
            highest_avg_temp = avg_temp
        if avg_temp < lowest_avg_temp:
            lowest_avg_temp = avg_temp

        total_avg_humidity += avg_humidity
        year_count += 1

    avg_humidity_percentage = (total_avg_humidity / year_count)

    print(f'Highest Average Temperature: {round(highest_avg_temp)}')
    print(f'Lowest Average Temperature: {round(lowest_avg_temp)}')
    print(f'Average Mean Humidity Percentage: {avg_humidity_percentage:.2f}%')

def execute_c_argument(my_weatherlist, year, month):
    days = []
    lows = []
    highs = []
    
    for line in my_weatherlist:
        try:
            date_str = line[0]
            low_temp = float(line[2])
            high_temp = float(line[1])
            date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            if date_obj.year == int(year) and date_obj.strftime('%b') == month:
                day = date_obj.day
                days.append(day)
                lows.append(low_temp)
                highs.append(high_temp)
        except (ValueError, IndexError) as e:
            continue
        
    plot_temperature_chart(days,lows, highs, year, month)

def plot_temperature_chart(days,lows, highs, year, month):
    fig, ax = plt.subplots()

    y = np.arange(len(days))
    ax.barh(y - 0.2, lows, height=0.4, align='center', color='blue', label='Low Temps')
    ax.barh(y + 0.2, highs, height=0.4, align='center', color='red', label='High Temps')

    ax.set_yticks(y)
    ax.set_yticklabels(days)

    ax.set_xlabel('Temperature (°C)')
    ax.set_ylabel('Day')
    ax.set_title(f'Temperatures for {year}/{month}')
    ax.legend()

    plt.show()

def handling_e_command(year_month):
    years = year_month
    months = {}
    process_files(years, months, '-e')
    print("command e")

def handling_a_command(years_month):
    years, months = map_months(years_month)
    process_files(years, months, '-a')
    print("command a")

def Handling_c_command(years_month):
    years, months = map_months(years_month)
    process_files(years, months, '-c', years[0], months[years[0]])
    print("command c")

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

    data_execution(my_weatherlist, flag, year)

def main():
    flag, years_months = parse_arguments()
    
    if flag == '-e':
        handling_e_command(years_months)
    elif flag == '-a':
        handling_a_command(years_months)
    elif flag == '-c':
        Handling_c_command(years_months)

if __name__ == "__main__":
    main()
