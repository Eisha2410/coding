import csv

def parse_company_data(file_path, output_csv):
    with open(file_path, 'r') as file:
        company_data = {}
        current_company = None
        all_companies_data = []

        for line in file:
            line = line.strip()

            if line and not line.startswith(('Year', 'Comments per month', 'Tasks', 'Total_comments', 'Task_count', 'Most_common')):
                if current_company and company_data:
                    all_companies_data.append((current_company, company_data))
                current_company = line
                company_data = {
                "comments_per_month": {},
                "task_interactions_per_month": {},
                "tasks_per_month": {},
                "total_comments": 0,
                "total_tasks": 0,
                "most_common_title": "None",
                "most_common_location": "None",
                }

            elif line.startswith('Year'):
                parts = line.split(',')
                if len(parts) < 3:
                    print(f"Error parsing line: {line}")
                    continue

                try:
                    year = parts[0].split(' ')[1]
                    month = parts[1].split(' ')[2]
                    value = int(parts[2].split(' ')[-1])
                except (IndexError, ValueError) as e:
                    print(f"Error parsing line: {line}, Exception: {e}")
                    continue

                if "Total Comments" in line:
                        company_data["comments_per_month"][f'{year}-{month}'] = value

                elif "Total Entries" in line:
                        company_data["task_interactions_per_month"][f"{year}-{month}"] = value
    
                elif "Total Tasks" in line:
                        company_data["tasks_per_month"][f"{year}-{month}"] = value
                    
            elif line.startswith('Total_comments'):
                try:
                    company_data['total_comments'] = int(line.split(' ')[1])
                except ValueError:
                    print(f"Error parsing total comments in line: {line}")

            elif line.startswith('Task_counts'):
                try:
                    company_data['total_tasks'] = int(line.split(' ')[1])
                except ValueError:
                    print(f"Error parsing total tasks in line: {line}")

            elif line.startswith("Most_common_title"):
                if 'None' not in line:
                    try:
                        company_data['most_common_title'] = eval(line.split(' ', 1)[1])['title']
                    except (SyntaxError, KeyError):
                        print(f"Error parsing most common title in line: {line}")

            elif line.startswith('Most_common_location'):
                if 'None' not in line:
                    try:
                        location_data = eval(line.split(' ', 1)[1])
                        company_data['most_common_location'] = f"{location_data['location__building']}, {location_data['location__floor']}, {location_data['location__room']}"
                    except(SyntaxError, KeyError):
                        print(f"Error parsing most common location in line: {line}")

        if current_company and company_data:
            all_companies_data.append((current_company, company_data))
    
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile) 

        for company, data in all_companies_data:
            writer.writerow([f'Company: {company}'])
            writer.writerow(['Comments per month:'])
            if data["comments_per_month"]:
                for date, count in data["comments_per_month"].items():
                    year, month = date.split('-')
                    writer.writerow([f'Year: {year}, Month: {month}, Total Comments: {count}'])
            else:
                writer.writerow(['No data available'])

            writer.writerow(['Tasks interactions per month:'])
            if data["task_interactions_per_month"]:
                for date, count in data["task_interactions_per_month"].items():
                    year, month = date.split('-')
                    writer.writerow([f'Year: {year}, Month: {month}, Total Entries: {count}'])
            else:
                writer.writerow(['No data available'])

            writer.writerow([f'Total_comments {data["total_comments"]}'])
            writer.writerow([f'Task_counts {data["total_tasks"]}'])

            writer.writerow(['Tasks per month:'])
            if data["tasks_per_month"]:
                for date, count in data["tasks_per_month"].items():
                    year, month = date.split('-')
                    writer.writerow([f'Year: {year}, Month: {month}, Total Tasks: {count}'])
            else:
                writer.writerow(['No data available'])

            writer.writerow([f'Most_common_title {data["most_common_title"]}'])
            writer.writerow([f'Most_common_location {data["most_common_location"]}'])
            writer.writerow([])
            

parse_company_data("companies_data.txt", "output_company_data_grouped.csv")         

