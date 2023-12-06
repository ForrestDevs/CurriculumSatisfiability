from data import *
from tabulate import tabulate
from tqdm import tqdm
from itertools import combinations, product
from collections import defaultdict
from bauhaus import Encoding, proposition, constraint, Or, And
from bauhaus.utils import count_solutions, likelihood
from propositions import *
from nnf import config
from display import display_solution

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
    for prop in tqdm(course_prerequisite_props, desc="Adding course constraints (1/4)"):
            course = prop.course
            prerequisite = prop.prerequisite
            course_level = int(course.split()[1][0])  # Extract the course level from the course code
            prerequisite_level = int(prerequisite.split()[1][0])  # Extract the course level from the prerequisite code

            if course_level == prerequisite_level:  # Check if the course level matches the prerequisite level
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
    for daily_times in tqdm(course_times_per_day.values(), desc="Adding course constraints (2/4)"):
        constraint.add_at_most_one(E, daily_times)

    # Organize the propositions into a dictionary by day, term, time, and classroom
    room_bookings = defaultdict(list)
    for prop in course_assigned_props:
        room_bookings[(prop.time, prop.term, prop.day, prop.room)].append(prop)

    # Ensure there are no classroom conflicts
    for booked_room in tqdm(room_bookings.values(), desc="Adding course constraints (3/4)"):
        constraint.add_at_most_one(E, booked_room)

    # Organize the propositions into a dictionary by course and term
    term_courses = defaultdict(list)
    for prop in course_assigned_props:
        term_courses[(prop.course, prop.term)].append(prop)

    # Ensure that there are at most 2 lectures per course per term 
    for course_times in tqdm(term_courses.values(), desc="Adding course constraints (4/4)"):
        constraint.add_at_most_k(E, 2, course_times)

    return E

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

