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
                        company_data["comments_per_month"][f'{month}/1/{year}'] = value

                elif "Total Entries" in line:
                        company_data["task_interactions_per_month"][f"{month}/1/{year}"] = value
    
                elif "Total Tasks" in line:
                        company_data["tasks_per_month"][f"{month}/1/{year}"] = value
                    
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
    months = ['3/1/2023', '4/1/2023', '5/1/2023', '6/1/2023', '7/1/2023', '8/1/2023', '9/1/2023', '10/1/2023', '11/1/2023', '12/1/2023',
              '1/1/2024', '2/1/2024', '3/1/2024', '4/1/2024', '5/1/2024', '6/1/2024', '7/1/2024', '8/1/2024']
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile) 
        company_names = [item[0] for item in all_companies_data]
        total_comments = [item[1]['total_comments'] for item in all_companies_data]
        writer.writerow(["Category"]+company_names)
        writer.writerow(["Total Comments (All Times)"] + total_comments)

        writer.writerow(["Comments per Month"])
        for month in months:
            comments_in_month = [item[1]['comments_per_month'].get(month) or 0 for item in all_companies_data]
            writer.writerow([month]+comments_in_month)

        writer.writerow(["Tasks Interactions per Month"])
        for month in months:
            interaction_in_month = [item[1]['task_interactions_per_month'].get(month) or 0 for item in all_companies_data]
            writer.writerow([month]+interaction_in_month)

        total_tasks = [item[1]['total_tasks'] for item in all_companies_data]
        writer.writerow(["Total Tasks (All time)"] + total_tasks)

        writer.writerow(["Tasks per Month"])
        for month in months:
            interaction_in_month = [item[1]['task_interactions_per_month'].get(month) or 0 for item in all_companies_data]
            writer.writerow([month]+interaction_in_month)

        most_common_title = [item[1]['most_common_title'] for item in all_companies_data]
        writer.writerow(["Most Common Title"] + most_common_title)

        most_common_location = [item[1]['most_common_location'] for item in all_companies_data]
        writer.writerow(["Most Common Location"] + most_common_location)
            

parse_company_data("companies_data.txt", "output_company_data_grouped.csv")         

