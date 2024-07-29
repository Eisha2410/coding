import os
import glob
import sys

sys.argv
for w in sys.argv:
    print(w)
if len(sys.argv) < 3:
    sys.exit(1)

my_weatherlist = []

def read_files(file_name):
    file = open (file_name , "r")
    read = file.read().splitlines(",")
    for i in range(2, len(read)-1):
        my_weatherlist.append(read[i].split(","))
        read[i].split(",")

directory = sys.argv[1]
year = sys.argv[3] if len(sys.argv) > 3 and sys.argv[2] == "-e" else None

pattern = os.path.join(directory, '*2002*.txt')
files = glob.glob(pattern)

global_max_temp = float('-inf')
global_min_temp = float('inf')
highest_humidity = float('-inf')
humidity_count = 0
humidity_percentage = 0

for file_path in files:
    if os.path.exists(file_path):
        try:
            read_files(file_path)
        except Exception as e:
            file_path: {e}

for line in my_weatherlist:
    try:
        temperature = float(line[1])  
        humidity = float(line[1])
        if temperature > global_max_temp:
           global_max_temp = temperature
        if temperature < global_min_temp:
           global_min_temp = temperature
        if humidity > highest_humidity:
           highest_humidity = humidity 

        humidity_percentage += humidity
        humidity_count += 1
        humidity_percentage = (humidity/highest_humidity)* 100.0


    except (ValueError, IndexError) as e:
        line: {e}
        continue

print(f'Highest: {global_max_temp}')
print(f'Lowest: {global_min_temp}')
print(f'Humidity: {humidity_percentage}')