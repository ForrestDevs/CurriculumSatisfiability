import pandas as pd




def combine_course_professor(course_assigned_props, professor_assigned_props):
    combined_info = {}
    for course_assign in course_assigned_props:
        for prof_assign in professor_assigned_props:
            if (course_assign.course == prof_assign.course and
                course_assign.room == prof_assign.room and
                course_assign.term == prof_assign.term and
                course_assign.day == prof_assign.day and
                course_assign.time == prof_assign.time):
                combined_info_key = (course_assign.term, course_assign.day, course_assign.time, course_assign.room)
                combined_info[combined_info_key] = (course_assign.course, prof_assign.professor)
    return combined_info

def create_final_schedule(combined_info):
    # Create DataFrame from combined info
    data = [{'Term': key[0], 'Day': key[1], 'Time': key[2], 'Room': key[3], 
             'Course': f"{value[0]} (Prof: {value[1]})"}
            for key, value in combined_info.items()]
    df = pd.DataFrame(data)

    # Define the order for days and time slots
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    time_order = sorted(set(df['Time']))  # Assuming df['Time'] contains all time slots

    # Convert 'Day' and 'Time' columns to categorical types with the specified order
    df['Day'] = pd.Categorical(df['Day'], categories=day_order, ordered=True)
    df['Time'] = pd.Categorical(df['Time'], categories=time_order, ordered=True)

    # Combine Course and Room into a single string for each assignment
    # df['CourseRoom'] = df.apply(lambda x: f"{x['Course']} (Room: {x['Room']})", axis=1)

    # Separate data for each term
    df_term1 = df[df['Term'] == 'T-1']
    df_term2 = df[df['Term'] == 'T-2']

    # Function to format the cell content with custom styling
    def format_cell(items):
        return ' / '.join([f'<div class="course-schedule">{item}</div>' for item in items])

     # Create pivot tables for each term with corrected values field
    pivot_table_term1 = df_term1.pivot_table(index=['Time', 'Room'], columns='Day', values='Course', 
                                             aggfunc=format_cell).fillna('')
    pivot_table_term2 = df_term2.pivot_table(index=['Time', 'Room'], columns='Day', values='Course', 
                                             aggfunc=format_cell).fillna('')

    return pivot_table_term1, pivot_table_term2

def generate_final_html(pivot_table_term1, pivot_table_term2):
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
        .course-schedule {
            background-color: grey;
            padding: 5px;
            margin: 5px;
            display: inline-block; /* For multiple blocks in the same cell */
        }
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

# Function to display the final course schedule with professors
def display_final_schedule(course_schedule, professor_schedule):
    # Filter out the propositions that are true in the solution
    true_course_schedule = [prop for prop, value in course_schedule.items() if value]
    true_professor_schedule = [prop for prop, value in professor_schedule.items() if value]
    # Combine the course and professor schedules
    combined_info = combine_course_professor(true_course_schedule, true_professor_schedule)
    # Create a schedule from the true propositions
    schedule_pivot_table_term1, schedule_pivot_table_term2 = create_final_schedule(combined_info)
    # Generate HTML schedule
    complete_html_schedule = generate_final_html(schedule_pivot_table_term1, schedule_pivot_table_term2)
    # Write the HTML to a file
    with open('schedule_with_professors.html', 'w') as file:
        file.write(complete_html_schedule)
    print("Final schedule saved as HTML.")





# # Function to transform the list of CourseAssigned instances into a DataFrame
# def create_schedule(assignments):
#     # Convert assignments to a DataFrame
#     data = [{'Course': assign.course, 'Room': assign.room, 'Term': assign.term, 
#              'Day': assign.day, 'Time': assign.time}
#             for assign in assignments]
#     df = pd.DataFrame(data)

#     # Define the order for days and time slots
#     day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
#     time_order = sorted(set(df['Time']))  # Assuming df['Time'] contains all time slots

#     # Convert 'Day' and 'Time' columns to categorical types with the specified order
#     df['Day'] = pd.Categorical(df['Day'], categories=day_order, ordered=True)
#     df['Time'] = pd.Categorical(df['Time'], categories=time_order, ordered=True)

#     # Combine Course and Room into a single string for each assignment
#     df['CourseRoom'] = df.apply(lambda x: f"{x['Course']} (Room: {x['Room']})", axis=1)

#     # Separate data for each term
#     df_term1 = df[df['Term'] == 'T-1']
#     df_term2 = df[df['Term'] == 'T-2']

#     # Function to format the cell content
#     def format_cell(items):
#         return ' / '.join(items)

#     # Create pivot tables for each term
#     pivot_table_term1 = df_term1.pivot_table(index=['Time', 'Room'], columns='Day', values='CourseRoom', 
#                                              aggfunc=format_cell).fillna('')
#     pivot_table_term2 = df_term2.pivot_table(index=['Time', 'Room'], columns='Day', values='CourseRoom', 
#                                              aggfunc=format_cell).fillna('')

#     return pivot_table_term1, pivot_table_term2

# # Function to transform the list of ProffesorAssigned instances into a DataFrame
# def create_schedule_with_professors(assignments):
#     # Convert assignments to a DataFrame
#     data = [{'Course': assign.course, 'Room': assign.room, 'Term': assign.term, 
#              'Day': assign.day, 'Time': assign.time, 'Professor': assign.professor}
#             for assign in assignments]
#     df = pd.DataFrame(data)

#     # Define the order for days and time slots
#     day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
#     time_order = sorted(set(df['Time']))  # Assuming df['Time'] contains all time slots
    
# # Function to generate HTML schedule from the pivot table
# def generate_html_schedule(pivot_table_term1, pivot_table_term2):
#     # Convert both pivot tables to HTML
#     html_term1 = pivot_table_term1.to_html(classes='schedule_table', escape=False)
#     html_term2 = pivot_table_term2.to_html(classes='schedule_table', escape=False)

#     # Add custom styling
#     html_style = '''
#     <style>
#         .schedule_table {
#             width: 100%;
#             border-collapse: collapse;
#             margin-bottom: 20px; /* space between tables */
#         }
#         .schedule_table, .schedule_table th, .schedule_table td {
#             border: 1px solid black;
#             padding: 8px;
#             text-align: left;
#             vertical-align: top;
#         }
#         .schedule_table th {
#             background-color: #f2f2f2;
#         }
#         .term-heading {
#             font-size: 20px;
#             font-weight: bold;
#             margin-top: 20px;
#         }
#         /* Additional styles can be added here */
#     </style>
#     '''

#     # Combine style and HTML for both terms
#     complete_html = f'''
#     <html>
#         <head>{html_style}</head>
#         <body>
#             <div class="term-heading">Term 1 Schedule</div>
#             {html_term1}
#             <div class="term-heading">Term 2 Schedule</div>
#             {html_term2}
#         </body>
#     </html>
#     '''

#     return complete_html

# # Function to display the course schedule
# def display_course_schedule(solution):
#     print("SOLUTION Length:", len(solution))

#     # Filter out the propositions that are true in the solution
#     true_props = [prop for prop, value in solution.items() if value]

#     print("True Length: ", len(true_props))

#     # print("True Props: ", true_props)

#     # Create a schedule from the true propositions
#     schedule_pivot_table_term1, schedule_pivot_table_term2 = create_schedule(true_props)
#     # Usage
#     complete_html_schedule = generate_html_schedule(schedule_pivot_table_term1, schedule_pivot_table_term2)

#     # Write the HTML to a file
#     with open('combined_schedule.html', 'w') as file:
#         file.write(complete_html_schedule)

#     print("Combined schedule saved as HTML.")

