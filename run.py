from data import *
from tabulate import tabulate
from tqdm import tqdm
from itertools import combinations, product
from collections import defaultdict
from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood
from nnf import config
from propositions import *

config.sat_backend = "kissat"

# Define course scheduling using CourseAssigned propositions
course_assigned_props = []
for course in COURSE_REQS.keys():
    for term in TERMS:
        for room in CLASSROOMS:
            for day in DAYS:
                for time in TIMESLOTS:
                    course_assigned_props.append(CourseAssigned(course, room, term, day, time))

# Define course prerequisites using CoursePrerequisite propositions
course_prerequisite_props = []
for course, prerequisites in COURSE_REQS.items():
    for prerequisite in prerequisites:
        course_prerequisite_props.append(CoursePrerequisite(course, prerequisite))

# Program Props:
program_req_course_props = []
for program, years in PROGRAMS.items():
    for year, courses in years.items():
        for course in courses:
            program_req_course_props.append(ProgramReqCourse(course, program, year))

program_shares_prereq_props = []
for program1, program2 in combinations(PROGRAMS.keys(), 2):
    for course in COURSE_REQS.keys():
        program_shares_prereq_props.append(ProgramSharesPreReq(program1, program2, course))

# Classroom Props:
classroom_assigned_props = []
for room in CLASSROOMS:
    for term in TERMS:
        for course in COURSE_REQS.keys():
            for day in DAYS:
                for time in TIMESLOTS:
                    classroom_assigned_props.append(ClassroomAssigned(room, course, term, day, time))

def schedule_programs(E):
    # Ensure that prerequisites are scheduled in a term before the course that requires them
    for prop in tqdm(course_prerequisite_props, desc="Adding course constraints (1/2)"):
        course = prop.course
        prerequisite = prop.prerequisite
        for i in range(len(TERMS) - 1):  # We subtract 1 because we're looking ahead by 1 term

            current_term = TERMS[i]
            next_term = TERMS[i + 1]
            
            for room, day, time in product(CLASSROOMS, DAYS, TIMESLOTS):
                # Ensure that the prerequisite course is offered in the current term
                prereq_in_current_term = CourseAssigned(prerequisite, room, current_term, day, time)
                # And the course that requires it is offered in the next term
                course_in_next_term = CourseAssigned(course, room, next_term, day, time)
                E.add_constraint(prereq_in_current_term & course_in_next_term)
   
    # Ensure that there are at least 2 lectures per course
    for course in tqdm(COURSE_REQS.keys(), desc="Adding course constraints (2/2)"):
        # Create a dictionary to store the lectures for each time slot
        lectures_by_timeslot = {(day, time): [] for day in DAYS for time in TIMESLOTS}
        
        for term in TERMS: 
            # Add each lecture to the list for its time slot
            for room, day, time in product(CLASSROOMS, DAYS, TIMESLOTS):
                lecture = CourseAssigned(course, room, term, day, time)
                lectures_by_timeslot[(day, time)].append(lecture)
            # Ensure that no more than one lecture is scheduled at the same time
            for lectures in lectures_by_timeslot.values():
                constraint.add_at_most_one(E, lectures)

            # Ensure that at least 2 lectures are scheduled
            for timeslot, lectures in lectures_by_timeslot.items():
                if len(lectures) > 1:
                    constraint.add_at_least_one(E, lectures)

    # Classroom Constraints:
    for room, term, day, time in tqdm(product(CLASSROOMS, TERMS, DAYS, TIMESLOTS), desc="Adding classroom constraints"):
        courses = [CourseAssigned(course, room, term, day, time) for course in COURSE_REQS.keys()]
        constraint.add_at_most_one(E, courses)
    return E


def display_solution(solution):
    # Filter out the propositions that are true in the solution
    true_props = [prop for prop, value in solution.items() if value]

    print(true_props)


    # Sort the propositions by term, day, and time
    sorted_props = sorted(true_props, key=lambda prop: (TERMS.index(prop.term), DAYS.index(prop.day), TIMESLOTS.index(prop.time)))

    # Prepare the data for the table
    table_data = []
    for prop in sorted_props:
        # professor = professor_by_time.get((prop.term, prop.day, prop.time), 'N/A')
        table_data.append([prop.course, prop.term, prop.day, prop.time])

    # Display the table
    print(tabulate(table_data, headers=["Course", "Term", "Day", "Time"]))

if __name__ == "__main__":
    print("Building theory...")
    T = schedule_programs(Encoding())
    print("Begin compiling...")
    T = T.compile()
    print("\nSatisfiable: %s" % T.satisfiable())
    # print("# Solutions: %d" % count_solutions(T))
    print("VARS: ", len(T.vars()))
    print("OPs: ", T.size())
    solution = T.solve()
    print("Solution: ")
    display_solution(solution)
# endregion Compile + Run


