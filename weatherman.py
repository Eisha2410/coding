import os
import glob
import sys
import datetime
from colorama import Fore, Style

class WeatherData:
    MONTH_SYMBOL = {
        "1": "Jan", "2": "Feb", "3": "Mar", "4": "Apr", "5": "May", "6": "Jun",
        "7": "Jul", "8": "Aug", "9": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"
    }

    def __init__(self):
        self.weather_data = []
        self.parsed_flags = []

    def parse_arguments(self):
        args = sys.argv[1:]
        if not args:
            sys.exit("error: no arguments provided")

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

            self.parsed_flags.append((flag, years_month))
            i += 1

    def read_files(self, file_name):
        with open (file_name , "r") as file:
            lines = file.read().splitlines()
            for line in lines[2: len(lines)-1]:
                self.weather_data.append(line.split(","))
    
    def process_files(self, years, months, flag, year=None, month=None):
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

        for file_path in files:
            if os.path.exists(file_path):
                try:
                    self.read_files(file_path)
                except Exception as e:
                    file_path: {e}
    
    def find_extremes(self):
        global_max_temp = float('-inf')
        global_min_temp = float('inf')
        highest_humidity = float('-inf')
        max_temp_date = None
        min_temp_date = None
        humidity_date = None

        for line in self.weather_data:
            try:
                max_temperature = float(line[1])  
                min_temperature = float(line[3])
                humidity = float(line[7])
                date_obj = datetime.datetime.strptime(line[0], "%Y-%m-%d")

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
        return global_max_temp, max_temp_date, global_min_temp, min_temp_date, highest_humidity, humidity_date
    
    def calculate_averages(self):
        temp_dict = {}

        for line in self.weather_data:
            try:
                max_temperature = float(line[1])
                min_temperature = float(line[3])
                humidity = float(line[8])
                date_obj = datetime.datetime.strptime(line[0], "%Y-%m-%d")

                if date_obj not in temp_dict:
                    temp_dict[date_obj] = {'temp1' : [],'temp2' : [], 'humidities' : []}

                temp_dict[date_obj]['temp1'].append(max_temperature)
                temp_dict[date_obj]['temp2'].append(min_temperature)
                temp_dict[date_obj]['humidities'].append(humidity)
            except (ValueError, IndexError) as e:
                continue
    
        highest_avg_temp = float('-inf')
        lowest_avg_temp = float('inf')
        avg_humidity = 0

        for date, values in temp_dict.items():
            if values['temp1'] and values['temp2'] and values ['humidities']:
                avg_temp1 = sum(values['temp1']) / len(values['temp1'])
                avg_temp2 = sum(values['temp2']) / len(values['temp2'])
                avg_humidity = sum(values['humidities']) / len(values['humidities'])

                if avg_temp1 > highest_avg_temp:
                    highest_avg_temp = avg_temp1
                if avg_temp2 < lowest_avg_temp:
                    lowest_avg_temp = avg_temp2
        return highest_avg_temp, lowest_avg_temp, avg_humidity
    
    def generate_chart(self, year, month):
        days = {}
    
        for line in self.weather_data:
            try:
                low_temp = float(line[2])
                high_temp = float(line[1])
                date_obj = datetime.datetime.strptime(line[0], "%Y-%m-%d")

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

            print(f'{day:02d} {low_plus_sign}{high_plus_sign} {round(low_temp)}C-{round(high_temp)}C')

    def execute(self):
        for flag, years_month in self.parsed_flags:
            if flag == '-e':
                self.process_files([years_month], {}, '-e')
                global_max_temp, max_temp_date, global_min_temp, min_temp_date, highest_humidity, humidity_date = self.find_extremes()
            
                print(f'Highest: {round(global_max_temp)}C on {max_temp_date.strftime("%B %d") if max_temp_date else "N/A"}')
                print(f'Lowest: {round(global_min_temp)}C on {min_temp_date.strftime("%B %d") if min_temp_date else "N/A"}')
                print(f'Humidity: {round(highest_humidity)} on {humidity_date.strftime("%B %d")}')


            elif flag in ['-a', '-c']:
                year, month = years_month.split('/')
                month = WeatherData.MONTH_SYMBOL[month.lstrip('0')]
                self.process_files([year], {year: month}, flag, year, month)

                if flag == '-a':
                    highest_avg_temp, lowest_avg_temp, avg_humidity = self.calculate_averages()
                    print(f'Highest Average Temperature: {round(highest_avg_temp)}C')
                    print(f'Lowest Average Temperature: {round(lowest_avg_temp)}C')
                    print(f'Average Mean Humidity: {round(avg_humidity)}%')

                elif flag == '-c':
                    self.generate_chart(year, month)
    
def main():
    weather_data = WeatherData()
    weather_data.parse_arguments()
    weather_data.execute()
        
if __name__ == "__main__":
    main()
