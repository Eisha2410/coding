import os
import glob
import sys
import datetime

def parse_arguments():
    if len(sys.argv) < 3:
        sys.exit(1)

    flag = sys.argv[1]
    years_month = []

    if flag == '-e':
        if len(sys.argv) != 3:
            sys.exist(1)
        years_month = [sys.argv[2]]
    elif flag == '-a':
        if len(sys.argv) < 3:
            sys.exit(1)
        years_month = [sys.argv[2:]]
    else:
        sys.exit(1)
    return years_month, flag

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
            if month not in month_symbol:
                sys.exit(1)
            years.append(year)
            months[year] = month_symbol[month]
        else:
            sys.exit(1)
    return years, months

def read_files(file_name, my_weatherlist):
    file = open (file_name , "r")
    read = file.read().splitlines()
    for i in range(2, len(read)-1):
        my_weatherlist.append(read[i].split(","))
        read[i].split(",")

def data_execution(my_weatherlist):
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
            line: {e}
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

def handling_e_command(year_month):
    years, months = map_months([year_month])
    process_files(years, months)

def handling_a_command(years_month):
    years, months = map_months(years_month)
    process_files(years, months)

def process_files(years, months):
    directory = "./weatherdata"
    files = []
    for year in years:
        if year in months:
            pattern = os.path.join(directory, f"lahore_weather_{year}_{months[year]}*")
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

    data_execution(my_weatherlist)

def main():
    flag, years_months = parse_arguments()
    
    if flag == '-e':
        handling_e_command(years_months)
    elif flag == '-a':
        handling_a_command(years_months)

if __name__ == "__main__":
    main()
