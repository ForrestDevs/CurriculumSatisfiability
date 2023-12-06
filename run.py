from data import *
from display import *
from stageOne import *
from stageTwo import *

from tqdm import tqdm
from itertools import combinations, product
from collections import defaultdict
from bauhaus import constraint
from bauhaus.utils import count_solutions
from nnf import config
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

    # Ensure that there is at most 1 lecture for a course per day
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

def schedule_professors(solution):
    # Example usage
    scheduled_courses = [CourseAssigned("Math101", "R1", "T1", "Monday", "9AM"),
                        CourseAssigned("Physics101", "R2", "T1", "Tuesday", "10AM"),
                        # ... more scheduled courses ...
                        ]
    courses_per_professor = 2  # Each professor can teach 2 courses

    professor_requirements = generate_professor_requirements(scheduled_courses, courses_per_professor)
    print(professor_requirements)
    
    return E1


def generate_professor_requirements(scheduled_courses, courses_per_professor):
    """
    Generates a dictionary of required professors and the courses they can teach.

    :param scheduled_courses: List of scheduled courses (CourseAssigned objects).
    :param courses_per_professor: Number of courses each professor is qualified to teach.
    :return: Dictionary of professors and their assigned courses.
    """
    # Identify unique courses in the schedule
    unique_courses = set(course.course for course in scheduled_courses)

    # Calculate the number of professors needed
    num_professors = -(-len(unique_courses) // courses_per_professor)  # Ceiling division

    # Create a list of professors (e.g., P1, P2, P3, ...)
    professors = [f"P{i+1}" for i in range(num_professors)]

    # Assign courses to professors
    professor_assignments = {prof: [] for prof in professors}
    for i, course in enumerate(unique_courses):
        professor = professors[i % num_professors]
        professor_assignments[professor].append(course)

    return professor_assignments



if __name__ == "__main__":
    # Stage 1 - Course Scheduling
    print("Building Course Schedule Encoding...")
    C = schedule_programs()
    print("Begin compiling the encoding...")
    C = C.compile()
    print("\nSatisfiable: %s" % C.satisfiable())
    print("# Solutions: %d" % count_solutions(C))
    print("VARS: ", len(C.vars()))
    print("OPs: ", C.size())
    solution = C.solve()
    if solution:
        display_course_schedule(solution)
        # Stage 2 - Professor Scheduling
        print("\nBuilding Professor Schedule Encoding...")
        P = schedule_professors(solution)
        print("Begin compiling the encoding...")
        P = P.compile()
        print("\nSatisfiable: %s" % P.satisfiable())
        print("# Solutions: %d" % count_solutions(P))
        print("VARS: ", len(P.vars()))
        print("OPs: ", P.size())
        solution = P.solve()
        if solution:
            display_final_schedule(solution)
    else: 
        print("No solution found, ending program.")

    


