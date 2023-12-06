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
