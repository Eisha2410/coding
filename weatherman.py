import os
import sys

for w in sys.argv:
    print(w)

my_weatherlist = []

def read_files(file_name):
    file = open (file_name , "r")
    read = file.read().splitlines(",")
    for i in range(2, len(read)-1):
        my_weatherlist.append(read[i].split(","))
        read[i].split(",")

files = sys.argv[1:]

global_max_temp = float('-inf')
global_min_temp = float('inf')
highest_humidity = float('-inf')

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
        if temperature > global_max_temp:
           global_max_temp = temperature
        if temperature < global_min_temp:
           global_min_temp = temperature

        if humidity > highest_humidity:
           highest_humidity = humidity
           humidity = (humidity * highest_humidity)/ 100.0

    except (ValueError, IndexError) as e:
        line: {e}
        continue

print(f'Highhest: {global_max_temp}')
print(f'Lowest: {global_min_temp}')
print(f'Humidity: {highest_humidity}')