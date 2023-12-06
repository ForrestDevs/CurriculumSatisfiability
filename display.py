import pandas as pd
# Function to transform the list of CourseAssigned instances into a DataFrame
def create_schedule(assignments):
    # Convert assignments to a DataFrame
    data = [{'Course': assign.course, 'Room': assign.room, 'Term': assign.term, 
             'Day': assign.day, 'Time': assign.time}
            for assign in assignments]
    df = pd.DataFrame(data)

     # Define the order for days and time slots
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    time_order = sorted(set(df['Time']))  # Assuming df['Time'] contains all time slots

    # Convert 'Day' and 'Time' columns to categorical types with the specified order
    df['Day'] = pd.Categorical(df['Day'], categories=day_order, ordered=True)
    df['Time'] = pd.Categorical(df['Time'], categories=time_order, ordered=True)

    # Combine Course and Room into a single string for each assignment
    df['CourseRoom'] = df.apply(lambda x: f"{x['Course']} (Room: {x['Room']})", axis=1)

    # Separate data for each term
    df_term1 = df[df['Term'] == 'T-1']
    df_term2 = df[df['Term'] == 'T-2']

    # Function to format the cell content
    def format_cell(items):
        return ' / '.join(items)

    # Create pivot tables for each term
    pivot_table_term1 = df_term1.pivot_table(index=['Time', 'Room'], columns='Day', values='CourseRoom', 
                                             aggfunc=format_cell).fillna('')
    pivot_table_term2 = df_term2.pivot_table(index=['Time', 'Room'], columns='Day', values='CourseRoom', 
                                             aggfunc=format_cell).fillna('')

    return pivot_table_term1, pivot_table_term2

# Function to generate HTML schedule from the pivot table
def generate_html_schedule(pivot_table_term1, pivot_table_term2):
    # Convert both pivot tables to HTML
    html_term1 = pivot_table_term1.to_html(classes='schedule_table', escape=False)
    html_term2 = pivot_table_term2.to_html(classes='schedule_table', escape=False)

    # Add custom styling
    html_style = '''
    <style>
        .schedule_table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px; /* space between tables */
        }
        .schedule_table, .schedule_table th, .schedule_table td {
            border: 1px solid black;
            padding: 8px;
            text-align: left;
            vertical-align: top;
        }
        .schedule_table th {
            background-color: #f2f2f2;
        }
        .term-heading {
            font-size: 20px;
            font-weight: bold;
            margin-top: 20px;
        }
        /* Additional styles can be added here */
    </style>
    '''

    # Combine style and HTML for both terms
    complete_html = f'''
    <html>
        <head>{html_style}</head>
        <body>
            <div class="term-heading">Term 1 Schedule</div>
            {html_term1}
            <div class="term-heading">Term 2 Schedule</div>
            {html_term2}
        </body>
    </html>
    '''

    return complete_html


def display_solution(solution):
    print("SOLUTION Length:", len(solution))

    # Filter out the propositions that are true in the solution
    true_props = [prop for prop, value in solution.items() if value]

    print("True Length: ", len(true_props))

    # print("True Props: ", true_props)

    # Create a schedule from the true propositions
    schedule_pivot_table_term1, schedule_pivot_table_term2 = create_schedule(true_props)
    # Usage
    complete_html_schedule = generate_html_schedule(schedule_pivot_table_term1, schedule_pivot_table_term2)

    # Write the HTML to a file
    with open('combined_schedule.html', 'w') as file:
        file.write(complete_html_schedule)

    print("Combined schedule saved as HTML.")
import pandas as pd

# Function to transform the list of CourseAssigned instances into a DataFrame
def create_pivot(assignments):
    # Extract information into a list of dictionaries
    data = [
        {'Course': assign.course, 'Room': assign.room, 'Term': assign.term, 
         'Day': assign.day, 'Time': assign.time}
        for assign in assignments
    ]

    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(data)

    # Pivot the DataFrame to get the desired layout: index=time, columns=day, values=course
    pivot_table = df.pivot_table(index=['Time', 'Term', 'Room'], columns='Day', values='Course', aggfunc=lambda x: ' / '.join(x))

    return pivot_table

def create_twoterm_pivot(assignments):
    # Extract information into a list of dictionaries
    data = [
        {'Course': assign.course, 'Room': assign.room, 'Term': assign.term, 
         'Day': assign.day, 'Time': assign.time}
        for assign in assignments
    ]

    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(data)

    # Separate data for each term
    df_term1 = df[df['Term'] == 'T-1']
    df_term2 = df[df['Term'] == 'T-2']

    # Create pivot tables for each term
    pivot_table_term1 = df_term1.pivot_table(index=['Time', 'Room'], columns='Day', values='Course', aggfunc=lambda x: ' / '.join(x)).fillna('')
    pivot_table_term2 = df_term2.pivot_table(index=['Time', 'Room'], columns='Day', values='Course', aggfunc=lambda x: ' / '.join(x)).fillna('')

    return pivot_table_term1, pivot_table_term2


def create_schedule(assignments):
    # Extract information into a list of dictionaries
    data = [
        {'Course': assign.course, 'Room': assign.room, 'Term': assign.term, 
         'Day': assign.day, 'Time': assign.time, 'Professor': assign.professor}
        for assign in assignments
    ]

    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(data)

    # Define the order for days and time slots
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    time_order = sorted(set(df['Time']))  # Assuming df['Time'] contains all time slots
    
    # Separate data for each term
    df_term1 = df[df['Term'] == 'T-1']
    df_term2 = df[df['Term'] == 'T-2']

    # HTML template for a course block
    course_block_template = '''
    <div class="course-block">
        <strong>{course_code}</strong><br>
        Room: {room}<br>
        Prof: {professor}
    </div>
    '''

    # Function to format the cell content
    def format_cell(x):
        return ' / '.join([course_block_template.format(course_code=item['Course'], 
                                                        room=item['Room'], 
                                                        professor=item['Professor']) 
                           for item in x])

    # Create pivot tables for each term
    pivot_table_term1 = df_term1.pivot_table(index=['Time', 'Room'], columns='Day', values=['Course', 'Room', 'Professor'], 
                                             aggfunc=lambda x: format_cell(x.dropna().to_dict('records'))).fillna('')
    pivot_table_term2 = df_term2.pivot_table(index=['Time', 'Room'], columns='Day', values=['Course', 'Room', 'Professor'], 
                                             aggfunc=lambda x: format_cell(x.dropna().to_dict('records'))).fillna('')

    return pivot_table_term1, pivot_table_term2


def generate_html_schedule(pivot_table_term1, pivot_table_term2):
    # Convert both pivot tables to HTML
    html_term1 = pivot_table_term1.to_html(classes='schedule_table', escape=False)
    html_term2 = pivot_table_term2.to_html(classes='schedule_table', escape=False)

    # Add custom styling
    html_style = '''
    <style>
        .schedule_table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px; /* space between tables */
        }
        .schedule_table, .schedule_table th, .schedule_table td {
            border: 1px solid black;
            padding: 8px;
            text-align: left;
            vertical-align: top;
        }
        .schedule_table th {
            background-color: #f2f2f2;
        }
        .term-heading {
            font-size: 20px;
            font-weight: bold;
            margin-top: 20px;
        }
        /* Additional styles can be added here */
    </style>
    '''

    # Combine style and HTML for both terms
    complete_html = f'''
    <html>
        <head>{html_style}</head>
        <body>
            <div class="term-heading">Term 1 Schedule</div>
            {html_term1}
            <div class="term-heading">Term 2 Schedule</div>
            {html_term2}
        </body>
    </html>
    '''

    # Return the complete HTML
    return complete_html

# Usage
complete_html_schedule = generate_html_schedule(schedule_pivot_table_term1, schedule_pivot_table_term2)

# Write the HTML to a file
with open('combined_schedule.html', 'w') as file:
    file.write(complete_html_schedule)

print("Combined schedule saved as HTML.")



# Start of the HTML string
html_string = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Weekly Schedule</title>
<style>
    body { font-family: Arial, sans-serif; }
    table { width: 100%; border-collapse: collapse; }
    th, td { border: 1px solid #ddd; text-align: center; padding: 8px; }
    th { background-color: #f2f2f2; }
    .lecture { background-color: #4CAF50; }
    .exercise { background-color: #f44336; }
    .project { background-color: #008CBA; }
    /* Additional styles */
</style>
</head>
<body>
<table>
    <tr>
        <th>Time</th>
        <th>Monday</th>
        <th>Tuesday</th>
        <th>Wednesday</th>
        <th>Thursday</th>
        <th>Friday</th>
    </tr>"""

# Generate table rows
for entry in schedule_data:
    html_string += f"""
    <tr>
        <td>{entry['time']}</td>
        <td class="{entry.get('Monday', '').lower()}">{entry.get('Monday', '')}</td>
        <td class="{entry.get('Tuesday', '').lower()}">{entry.get('Tuesday', '')}</td>
        <td class="{entry.get('Wednesday', '').lower()}">{entry.get('Wednesday', '')}</td>
        <td class="{entry.get('Thursday', '').lower()}">{entry.get('Thursday', '')}</td>
        <td class="{entry.get('Friday', '').lower()}">{entry.get('Friday', '')}</td>
    </tr>"""

# End of the HTML string
html_string += """
</table>
</body>
</html>
"""

# Write the string to an HTML file
with open('schedule.html', 'w') as file:
    file.write(html_string)


# import pandas as pd

# scheduled_courses = [
#     ('Computer Science', 'C1', 'Monday', '9:00', 'A1'),
#     ('Computer Science', 'C2 + Types', 'Monday', '9:00', 'A3'),
#     ('Computer Science', 'C2 + Types', 'Monday', '9:00', 'A3'),
#     ('Computer Science', 'C2 + Types', 'Monday', '9:00', 'A3'),
#     ('Computer Science', 'C2 + Types', 'Monday', '9:00', 'A3'),
#     ('Computer Science', 'C2 + Types', 'Monday', '9:00', 'A3'),
#     ('Computer Science', 'C2 + Types', 'Monday', '9:00', 'A3'),
#     ('Computer Science', 'C2 + Types', 'Monday', '9:00', 'A3'),
#     ('Computer Science', 'C2 + Types', 'Monday', '9:00', 'A3'),
#     ('Computer Science', 'Review', 'Tuesday', '9:00', 'A2'),
# ]
# # Days and timeslots
# days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
# timeslots = ["8AM-930AM", "930AM-11AM", "11AM-1230PM", "1230PM-2PM", "2PM-330PM", "330PM-5PM", "5PM-630PM", "630PM-8PM"]


# df = pd.DataFrame(scheduled_courses, columns=['Program', 'Course', 'Day', 'Time', 'Room'])
# pivot_table = df.pivot_table(index=['Time'], columns=['Day'], values='Course', aggfunc=lambda x: ' / '.join(x))

# # Export the DataFrame to an Excel file
# with pd.ExcelWriter('timetable.xlsx', engine='xlsxwriter') as writer:
#     pivot_table.to_excel(writer, sheet_name='Weekly Schedule')
    
#     # Get the xlsxwriter workbook and worksheet objects
#     workbook  = writer.book
#     worksheet = writer.sheets['Weekly Schedule']
    
#     # Apply formatting using xlsxwriter (this is just a start; you'll need to do much more)
#     merge_format = workbook.add_format({
#         'align': 'center',
#         'valign': 'vcenter',
#         'border': 1
#     })
#     worksheet.set_column('B:F', 20)  # Example: Set the width of columns B through F

# # Initialize a timetable as a dictionary
# # timetable = {day: {timeslot: '' for timeslot in timeslots} for day in days}

# # # Populate the timetable
# # for course, day, timeslot, room in scheduled_courses:
# #     timetable[day][timeslot] = f"{course} in {room}"

# # # Display the timetable
# # for timeslot in timeslots:
# #     print(f"{timeslot:15}", end=" | ")
# #     for day in days:
# #         print(f"{timetable[day][timeslot]:20}", end=" | ")
# #     print("\n" + "-"*100)
