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
    """
    ptr = 1
    with open(file_name , "w") as re:
        for line in read:
            if ptr != 1:
                re.write(line)
            ptr += 1
    for line in read:
        my_weatherlist.append(line.split())
        print(line.split())
        file.seek(0)
        file.remove(0)
        file.remove(1)
        file.remove(len-1)
        file.writeline(line[2:range(len-2)])
        print(line.split())
    """  
my_file = "weatherdata/lahore_weather_2002_Feb.txt"
func_access(my_file)

