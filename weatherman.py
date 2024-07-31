import os
import glob
import sys
import datetime

if len(sys.argv) < 3:
    sys.exit(1)

years = sys.argv[2]
sys.argv[3] if len(sys.argv) > 3 and sys.argv[2] == "-e" else None

my_weatherlist = []

def read_files(file_name):
    file = open (file_name , "r")
    read = file.read().splitlines()
    for i in range(2, len(read)-1):
        my_weatherlist.append(read[i].split(","))
        read[i].split(",")

directory = "./weatherdata"
pattern = os.path.join(directory, f"*{years}*" )
files = glob.glob(pattern)

global_max_temp = float('-inf')
global_min_temp = float('inf')
highest_humidity = float('-inf')
humidity_count = 0
humidity_percentage = 0
max_temp_date = ""
min_temp_date = ""
humidity_date = ""


for file_path in files:
    if os.path.exists(file_path):
        try:
            read_files(file_path)
        except Exception as e:
            file_path: {e}

for line in my_weatherlist:
    try:
        temperature = float(line[1])  
        humidity = float(line[-1])
        date_str = line[0]
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")

        if temperature > global_max_temp:
           global_max_temp = temperature
           max_temp_date = date_obj
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

print(f'Highest: {global_max_temp} on {max_temp_date.strftime("%B %d")}')
print(f'Lowest: {global_min_temp} on {min_temp_date.strftime("%B %d")}')
print(f'Humidity: {humidity_percentage} on {humidity_date.strftime("%B %d")}')
