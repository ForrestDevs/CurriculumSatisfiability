from data import *
from tabulate import tabulate
from tqdm import tqdm
from itertools import combinations, product
from collections import defaultdict
from bauhaus import Encoding, proposition, constraint, Or, And
from bauhaus.utils import count_solutions, likelihood
from propositions import *
from nnf import config
import pandas as pd

# Configure SAT backend
config.sat_backend = "kissat"

# Define course scheduling using CourseAssigned propositions
course_assigned_props = list()
for course, term, room, day, time in tqdm(product(COURSES.keys(), TERMS, CLASSROOMS, DAYS, TIMESLOTS), desc="Adding course assigned propositions"):
    course_assigned_props.append(CourseAssigned(course, room, term, day, time))

# Define course prerequisites using CoursePrerequisite propositions
course_prerequisite_props = list()
for course, value in tqdm(COURSES.items(), desc="Adding course prerequisite propositions"):
    if len(value['reqs']) > 0:
        # print("REQS: ", value['reqs'])
        for prerequisite in value['reqs']:
                course_prerequisite_props.append(CoursePrerequisite(course, prerequisite))

def schedule_programs():
    # Ensure that prerequisites are scheduled in a term before the course that requires them (IFF the course is the same level as the course that requires it)
    for prop in tqdm(course_prerequisite_props, desc="Adding course constraints (1/3)"):
            course = prop.course
            prerequisite = prop.prerequisite
            course_level = int(course.split()[1][0])  # Extract the course level from the course code
            prerequisite_level = int(prerequisite.split()[1][0])  # Extract the course level from the prerequisite code

            if course_level == prerequisite_level:  # Check if the course level matches the prerequisite level
                # for i in range(len(TERMS) - 1):  # We subtract 1 because we're looking ahead by 1 term 
                    for room, day in product(CLASSROOMS, DAYS):
                        # Propositions for the prerequisite course in Term 1
                        prereq_in_term1 = [CourseAssigned(prerequisite, room, "T-2", day, time) for time in TIMESLOTS]
                        # Propositions for the course in Term 2
                        course_in_term2 = [CourseAssigned(course, room, "T-1", day, time) for time in TIMESLOTS]

                        # Add the implies constraint for each timeslot
                        for course_time in course_in_term2:
                                E.add_constraint(~course_time)

                        for course_time in prereq_in_term1:
                                E.add_constraint(~course_time)
    
    # Organize the propositions into a dictionary by course, day and term
    course_times_per_day = defaultdict(list)
    for prop in course_assigned_props:
          course_times_per_day[(prop.course, prop.term, prop.day)].append(prop)

    # Ensure that there is at most 1 lecture for a course per term per day
    for daily_times in tqdm(course_times_per_day.values(), desc="Adding course constraints (2/3)"):
        constraint.add_at_most_one(E, daily_times)

    # Organize the propositions into a dictionary by day, term, time, and classroom
    room_bookings = defaultdict(list)
    for prop in course_assigned_props:
          room_bookings[(prop.time, prop.term, prop.day, prop.room)].append(prop)

    # Ensure there are no classroom conflicts
    for booked_room in tqdm(room_bookings.values(), desc="Adding course constraints (3/3)"):
        constraint.add_at_most_one(E, booked_room)

    return E


# Function to transform the list of CourseAssigned instances into a DataFrame
def create_schedule(assignments):
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

# Function to generate HTML schedule from the pivot table
def generate_html_schedule(pivot_table):
    # Convert the pivot table to HTML
    html = pivot_table.to_html(classes='schedule_table')

    # Add custom styling
    html_style = '''
    <style>
        .schedule_table {
            width: 100%;
            border-collapse: collapse;
        }
        .schedule_table, .schedule_table th, .schedule_table td {
            border: 1px solid black;
        }
        .schedule_table th, .schedule_table td {
            padding: 5px;
            text-align: center;
        }
        .schedule_table th {
            background-color: #f2f2f2;
        }
        /* Additional styles can be added here */
    </style>
    '''

    # Combine style and HTML
    complete_html = f"<html><head>{html_style}</head><body>{html}</body></html>"

    # Return the complete HTML
    return complete_html


def display_solution(solution):
    print("SOLUTION Length:", len(solution))

    # Filter out the propositions that are true in the solution
    true_props = [prop for prop, value in solution.items() if value]

    print("True Length: ", len(true_props))

    print("True Props: ", true_props)

    # Get the complete HTML for the schedule
    complete_html_schedule = generate_html_schedule(create_schedule(true_props))

    # Write the HTML to a file
    with open('schedule.html', 'w') as file:
        file.write(complete_html_schedule)

    print("Schedule saved as HTML.")

    
    # # Sort the propositions by term, day, and time
    # sorted_props = sorted(true_props, key=lambda prop: (TERMS.index(prop.term), DAYS.index(prop.day), TIMESLOTS.index(prop.time)))

    # # Prepare the data for the table
    # table_data = []
    # for prop in sorted_props:
    #     # professor = professor_by_time.get((prop.term, prop.day, prop.time), 'N/A')
    #     table_data.append([prop.course, prop.room, prop.term, prop.day, prop.time])

    # # Display the table
    # print(tabulate(table_data, headers=["Course", "Classroom", "Term", "Day", "Time"]))


if __name__ == "__main__":
    print("Building theory...")
    T = schedule_programs()
    print("Begin compiling...")
    T = T.compile()
    print("\nSatisfiable: %s" % T.satisfiable())
    # print("# Solutions: %d" % count_solutions(T))
    print("VARS: ", len(T.vars()))
    print("OPs: ", T.size())
    
    solution = T.solve()
    # print("Solution: ", solution)
    if solution:
        display_solution(solution)

    # print()

