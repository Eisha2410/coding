import re
import os
import ast
from collections import defaultdict
from datetime import datetime

start_date = datetime(2023, 3, 1)
end_date = datetime(2024, 8, 31)

def extract_year_month(line):
    match = re.search(r'Year:\s*(\d+),\s*Month:\s*(\d+)', line)
    if match:
        year = int(match.group(1))
        month = int(match.group(2))
        date = datetime(year, month, 1)
        if start_date <= date <= end_date:
            return date.strftime("%Y-%m")
    return None

file_path = "C:\\Users\\eisha.raazia_arbisof\\Documents\\arbisoftProject\\coding\\pythonscript\\companies_data.txt"
print("looking for file in:", os.getcwd())
print(f"Trying to open file: {file_path}")


if os.path.isfile(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
else:
    print(f"File {file_path} does not exist")
    lines = []

companies_data = {}
current_company = None
current_section = None

for line in lines:
    line = line.strip()

    if not line or line.startswith("Total_comments") or line.startswith("Task_counts"):
        continue

    if line.isalpha():
        current_company = line
        companies_data[current_company] = {
            'comments_per_month' : defaultdict(int),
            'task_per_month' : defaultdict(int),
            'task_interactions_per_month' : defaultdict(int),
            'most_common_title' : defaultdict(int),
            'most_common_location' : defaultdict(int),
            'Total_comments' : 0,
            'Task_counts': 0
        }
        continue

    year_month = extract_year_month(line)
    if current_company:
        data = companies_data[current_company]
        if re.search(r'comments per month', line, re.IGNORECASE):
            current_section = 'comments' 
        elif re.search(r'tasks interactions per month', line, re.IGNORECASE):
            current_section = 'tasks_interactions'
        elif re.search(r'tasks per month', line, re.IGNORECASE):
            current_section = 'tasks'
        elif re.search(r'Most_common_title', line, re.IGNORECASE):
            current_section = 'most_common_title'
            print(f"Entering most_common_title section for {current_company}")
        elif re.search(r'Most_common_location', line, re.IGNORECASE):
            current_section = 'most_common_location'
            print(f"Entering most_common_location section for {current_company}")
        else:
            if current_section:
                print(f"Processing line under section {current_section} for company {current_company}: {line}")

            if current_section == 'comments' and year_month:
                match = re.search(r'Total Comments:\s*(\d+)', line)
                if match:
                    data['comments_per_month'][year_month] += int(match.group(1))
                    data['Total_comments'] += int(match.group(1))

            elif current_section == 'tasks_interactions' and year_month:
                match = re.search(r'Total Entries:\s*(\d+)', line)
                if match:
                    data['task_interactions_per_month'][year_month] += int(match.group(1))

            elif current_section == 'tasks' and year_month:
                match = re.search(r'Total Tasks:\s*(\d+)', line)
                if match:
                    data['task_per_month'][year_month] += int(match.group(1))
                    data['Task_counts'] += int(match.group(1))

            elif current_section == 'most_common_title':
                print(f"data for section {current_section} for company {current_company}: {line}")
                try:
                    title_dict = ast.literal_eval(line)
                    title = title_dict.get('title')
                    title_count = title_dict.get('title_count', 0)
                    if title:
                        data['most_common_title'][title] += title_count
                        print(f"Parsed title: {title} with count: {title_count} for {current_company}")
                    else:
                        print(f"No title found in line: {line}")
                except (SyntaxError, ValueError) as e:
                    print(f"error parsing line for tilte: {line} - {e}")

            elif current_section == 'most_common_location':
                print(f"data for section {current_section} for company {current_company}: {line}")
                try:
                    location_dict = ast.literal_eval(line)
                    location = f"{location_dict.get('location__building')}, {location_dict.get('location__floor')}, {location_dict.get('location__room')}"
                    location_count = location_dict.get('location_count', 0)
                    if location:
                        data['most_common_location'][location] += location_count
                        print(f"Parsed location: {location} with count: {location_count} for {current_company}")
                    else:
                        print(f"No location found in line: {line}")
                except (SyntaxError, ValueError) as e:
                    print(f"error parsing line for location: {line} - {e}")

for company, data in companies_data.items():
    print(f"\nCompany: {company}") 
    print("Comments per month:", dict(data['comments_per_month']))
    print("Task interactions per month:", dict(data['task_interactions_per_month']))
    print("Total comments:", data['Total_comments'])
    print("Task counts:", data['Task_counts'])
    print("Task per month:", dict(data['task_per_month']))

    if data['most_common_title']:
        most_common_title = max(data['most_common_title'], key=data['most_common_title'].get)
        print("Most common title:", most_common_title)
    else:
        print("most common title: no data available")

    if data['most_common_location']:
        most_common_location = max(data['most_common_location'], key=data['most_common_location'].get)
        print("Most common location:", most_common_location)
    else:
        print("most common location: no data available")          
