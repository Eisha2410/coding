import os
import glob
import sys

sys.argv
for w in sys.argv:
    print(w)

my_weatherlist = []

def func_access(file_name):
    file = open (file_name , "r")
    read = file.read().splitlines()
    for i in range(2, len(read)-1):
        my_weatherlist.append(read[i].split())
        print(read[i].split())
    print(read[0])

directory = '/weatherman'
pattern = os.path.join(directory, '*2002*.txt')
files = glob.glob(pattern)

global_max_temp = float('-inf')
global_min_temp = float('inf')
highest_humidity = float('-inf')

for file_path in files:
    print(f'processing file: {file_path}')
    try:
        func_access(files)
        with open(file_path, 'r') as  file:
            next(file)
            for line in file:
                columns = line.strip().split('\t')
                temperature = float(columns[0])  
                humidity = float(columns[1])
                if temperature > global_max_temp:
                    global_max_temp = temperature
                if temperature < global_min_temp:
                    global_min_temp = temperature
                
                if humidity > highest_humidity:
                    highest_humidity = humidity   
    except Exception as e:
        print(f'error processing file {file_path}: {e}')


print(f'Maximum Temperature: {global_max_temp}')
print(f'Minimum Temperature: {global_min_temp}')
print(f'Highest Humidity: {highest_humidity}')

