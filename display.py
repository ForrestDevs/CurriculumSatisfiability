# Sample schedule data
schedule_data = [
    {'time': '9:00', 'Monday': 'Intro + Types', 'Tuesday': 'Review', 'Wednesday': 'Review', 'Thursday': '', 'Friday': 'Review'},
    {'time': '9:00', 'Monday': 'Intro + Types', 'Tuesday': 'Review', 'Wednesday': 'Review', 'Thursday': '', 'Friday': 'Review'},
    {'time': '9:00', 'Monday': 'Intro + Types', 'Tuesday': 'Review', 'Wednesday': 'Review', 'Thursday': '', 'Friday': 'Review'},
    {'time': '9:00', 'Monday': 'Intro + Types', 'Tuesday': 'Review', 'Wednesday': 'Review', 'Thursday': '', 'Friday': 'Review'},
    {'time': '9:00', 'Monday': 'Intro + Types', 'Tuesday': 'Review', 'Wednesday': 'Review', 'Thursday': '', 'Friday': 'Review'},
    {'time': '9:00', 'Monday': 'Intro + Types', 'Tuesday': 'Review', 'Wednesday': 'Review', 'Thursday': '', 'Friday': 'Review'},
    {'time': '9:00', 'Monday': 'Intro + Types', 'Tuesday': 'Review', 'Wednesday': 'Review', 'Thursday': '', 'Friday': 'Review'},
    {'time': '9:00', 'Monday': 'Intro + Types', 'Tuesday': 'Review', 'Wednesday': 'Review', 'Thursday': '', 'Friday': 'Review'},
    {'time': '10:00', 'Monday': 'Intro + Types', 'Tuesday': 'Review', 'Wednesday': 'Review', 'Thursday': '', 'Friday': 'Review'}
    
    # ... additional time slots
]

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
