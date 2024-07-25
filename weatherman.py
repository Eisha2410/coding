import sys
sys.argv

for w in sys.argv:
    print(w)

my_weatherlist = []

def func_access(file_name):
    file = open (file_name , "r+")
    read = file.read().splitlines()
    for i in range(2, len(read)-1):
        my_weatherlist.append(read[i].split())
        print(read[i].split())
    print(read[0])

my_file = "weatherdata/lahore_weather_2002_Feb.txt"
func_access(my_file)

