from data import *
from tabulate import tabulate
from tqdm import tqdm
from itertools import combinations, product
from collections import defaultdict
from bauhaus import Encoding, proposition, constraint, Or, And
from bauhaus.utils import count_solutions, likelihood
import pandas as pd

from nnf import config, Var
config.sat_backend = "kissat"

E = Encoding()

class Hashable:
    def __hash__(self):
        return hash(str(self))

    def __eq__(self, __value: object) -> bool:
        return hash(self) == hash(__value)

    def __repr__(self):
        return str(self)

# Professor Props:
@proposition(E)
class ProfessorAssigned(Hashable):
    def __init__(self, professor, course, term, day, time) -> None:
        self.professor = professor
        self.course = course
        self.term = term
        self.day = day
        self.time = time

    def __repr__(self) -> str:
        return f"Professor_Assigned(professor={self.professor}, course={self.course}, term={self.term}, day={self.day}, time={self.time})"

@proposition(E)
class ProfessorQualified(Hashable): 
    def __init__(self, professor, course)-> None:
        self.professor = professor
        self.course = course

    def __repr__(self) -> str:
        return f"ProfessorQualifiedForCourse(professor={self.professor}, course={self.course})"

# Course Props:
@proposition(E)
class CourseAssigned(Hashable):
    def __init__(self, course, room, term, day, time) -> None:
        self.course = course
        self.room = room
        self.term = term
        self.day = day
        self.time = time

    def __repr__(self) -> str:
        return f"CourseAssigned(course={self.course}, room={self.room}, term={self.term}, day={self.day}, time={self.time})"

@proposition(E)
class CoursePrerequisite(Hashable):
    def __init__(self, course, prerequisite) -> None:
        self.course = course
        self.prerequisite = prerequisite

    def __repr__(self) -> str:
        return f"Course_Prerequisite(course={self.course}, prerequisite={self.prerequisite})"

# Program Props:
@proposition(E)
class ProgramReqCourse:
    def __init__(self, course, program, year):
        self.course = course
        self.program = program
        self.year = year

    def __repr__(self):
        return f"Program_Req_Course(course={self.course}, program={self.program}, year={self.year})"

@proposition(E)
class ProgramSharesPreReq:
    def __init__(self, program1, program2, course):
        self.program1 = program1
        self.program2 = program2
        self.course = course

    def __repr__(self):
        return f"Program_Shares_PreReq(program1={self.program1}, program2={self.program2}, course={self.course})"

@proposition(E)
class ProgramCanComplete:
    def __init__(self, program, term):
        self.program = program
        self.term = term
        
    def __repr__(self):
        return f"Program_Can_Complete(program={self.program}, term={self.term})"

# Classroom Props:
@proposition(E)
class ClassroomAssigned(Hashable):
    def __init__(self, room, course, term, day, time) -> None:
        self.room = room
        self.course = course
        self.term = term
        self.day = day
        self.time = time

    def __repr__(self) -> str:
        return f"ClassroomAssigned(room={self.room}, course={self.course}, term={self.term}, day={self.day}, time={self.time})"

# Define course scheduling using CourseAssigned propositions
course_assigned_props = []
for course, term, room, day, time in tqdm(product(COURSES.keys(), TERMS, CLASSROOMS, DAYS, TIMESLOTS), desc="Adding course assigned propositions"):
    course_assigned_props.append(CourseAssigned(course, room, term, day, time))

# Define course prerequisites using CoursePrerequisite propositions
course_prerequisite_props = []
for course, value in tqdm(COURSES.items(), desc="Adding course prerequisite propositions"):
    print(course, value)
    if value['reqs']:
        print("REQS: ", value['reqs'])
        for prerequisite in value['reqs']:
            if prerequisite:
                course_prerequisite_props.append(CoursePrerequisite(course, prerequisite))

# Program Props:
# program_req_course_props = []
# for program, years in PROGRAMS.items():
#     for year, courses in years.items():
#         for course in courses:
#             program_req_course_props.append(ProgramReqCourse(course, program, year))

# program_shares_prereq_props = []
# for program1, program2 in combinations(PROGRAMS.keys(), 2):
    # for course in COURSE_REQS.keys():
    #     program_shares_prereq_props.append(ProgramSharesPreReq(program1, program2, course))

# Classroom Props:
# classroom_assigned_props = []
# for room in CLASSROOMS:
#     for term in TERMS:
#         for course in COURSE_REQS.keys():
#             for day in DAYS:
#                 for time in TIMESLOTS:
#                     classroom_assigned_props.append(ClassroomAssigned(room, course, term, day, time))

# Create the CourseAssigned propositions with the corresponding variables
# course_assigned_props = [CourseAssigned(course, room, term, day, time, variables[(course, term, room, day, time)]) for course, term, room, day, time in product(COURSES.keys(), TERMS, CLASSROOMS, DAYS, TIMESLOTS)]

def schedule_programs():
    course_times_per_term = defaultdict(list)
    for prop in course_assigned_props:
          course_times_per_term[(prop.course, prop.term)].append(prop)
    # Organize the propositions into a dictionary by course, day and term
    course_times_per_day = defaultdict(list)
    for prop in course_assigned_props:
          course_times_per_day[(prop.course, prop.term, prop.day)].append(prop)
    
    # Ensure that prerequisites are scheduled in a term before the course that requires them (IFF the course is the same level as the course that requires it)
    for prop in tqdm(course_prerequisite_props, desc="Adding prereq constraints (1/1)"):
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

    # Ensure that there is at most 1 lecture for a course per day
    for daily_times in tqdm(course_times_per_day.values(), desc="Adding course constraints (1/4)"):
        constraint.add_at_most_one(E, daily_times)

    # Ensure that there is at most 3 lectures for a course per term
    for course, term in tqdm(product(COURSES, TERMS), desc="Adding course constraints (2/4)"):
        # Create propositions for this course being scheduled in any room, on any day and time slot of the week
        weekly_course_assignments = [CourseAssigned(course, room, term, day, time) for room, day, time in product(CLASSROOMS, DAYS, TIMESLOTS)]
        # Ensure no more than X lectures are scheduled in total per week
        constraint.add_at_most_k(E, 3, weekly_course_assignments)
               
    # # Ensure that for all 3 credit courses, they are only booked in one term
    # for key, value in tqdm(COURSES.items(), desc="Adding course constraints (3/4)"):
    #     if value['credits'] == 3:  # Check if the course has 3 credits
    #         term_assignments = {term: [CourseAssigned(key, room, term, day, time) for room, day, time in product(CLASSROOMS, DAYS, TIMESLOTS)] for term in TERMS}

    #         # Add constraints to ensure the course is only scheduled in one term
    #         for term1 in TERMS:
    #             for term2 in TERMS:
    #                 if term1 != term2:
    #                     # If the course is scheduled in term1, it should not be scheduled in term2
    #                     for assign1 in term_assignments[term1]:
    #                         for assign2 in term_assignments[term2]:
    #                             E.add_constraint(~assign1 | ~assign2)  # Not both true

    # # # Ensure that courses with 6 credits are scheduled for both term 1 and term 2
    # for key, value in tqdm(COURSES.items(), desc="Adding course constraints (4/4)"):
    #     if value['credits'] == 6:  # Check if the course has 6 credits
    #         assignments_T1 = [CourseAssigned(key, room, "T-1", day, time) for room, day, time in product(CLASSROOMS, DAYS, TIMESLOTS)]
    #         # Create a list of CourseAssigned propositions for term "T-2"
    #         assignments_T2 = [CourseAssigned(key, room, "T-2", day, time) for room, day, time in product(CLASSROOMS, DAYS, TIMESLOTS)]
    #         # Add a constraint that at least one proposition from each list is true
    #         constraint.add_at_least_one(E, assignments_T1)
    #         constraint.add_at_least_one(E, assignments_T2)

    # Ensure no two courses are scheduled in the same classroom at the same timeslot
    for room, day, time, term in tqdm(product(CLASSROOMS, DAYS, TIMESLOTS, TERMS), desc="Adding classroom constraints"):
        # Create a list of propositions for each course being scheduled in this classroom at this timeslot
        course_assignments = [CourseAssigned(course, room, term, day, time) for course in COURSES]
        # Add a constraint that at most one of these propositions can be true
        constraint.add_at_most_one(E, course_assignments)

    return E

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


