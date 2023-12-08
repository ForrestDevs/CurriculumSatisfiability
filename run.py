from data import *
from display import *
from propositions import *
from tqdm import tqdm
from itertools import combinations, product
from collections import defaultdict
from bauhaus import constraint
from bauhaus.utils import count_solutions
from nnf import config
config.sat_backend = "kissat"

max_lectures_per_term = 2  # Each course can be taught a maximum of 4 times per term
courses_per_professor = 2  # Each professor can teach 2 courses

def schedule_programs():
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
    # Ensure that prerequisites are scheduled in a term before the course that requires them (IFF the course is the same level as the course that requires it)
    for prop in tqdm(course_prerequisite_props, desc="Adding course constraints (1/4)"):
            course = prop.course
            prerequisite = prop.prerequisite
            course_level = int(course.split()[1][0])  # Extract the course level from the course code
            prerequisite_level = int(prerequisite.split()[1][0])  # Extract the course level from the prerequisite code

            if course_level == prerequisite_level:  # Check if the course level matches the prerequisite level
                prereq_in_prev_term = [CourseAssigned(prerequisite, room, "T-1", day, time) for room in CLASSROOMS for day in DAYS for time in TIMESLOTS]
                course_in_next_term = [CourseAssigned(course, room, "T-2", day, time) for room in CLASSROOMS for day in DAYS for time in TIMESLOTS]
                # Add constraint for the entire term, not each room and day
                constraint.add_implies_all(E, course_in_next_term, prereq_in_prev_term)
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
        constraint.add_at_most_k(E, max_lectures_per_term, course_times)

    return E

def schedule_professors(solution):
    # Filter out the CourseAssigned Propositions that are true in the solution, which gives us the scheduled courses
    scheduled_courses = [prop for prop, value in solution.items() if value]
    # Organize the propositions into a dictionary by course
    courses = defaultdict(list)
    for prop in scheduled_courses:
        courses[(prop.course)].append(prop)
    # Identify unique courses in the schedule
    unique_courses = set(course.course for course in scheduled_courses)
    # Calculate the number of professors needed
    num_professors = -(-len(unique_courses) // courses_per_professor)  # Ceiling division
    # Create a list of professors (e.g., P1, P2, P3, ...)
    professors = [f"P{i+1}" for i in range(num_professors)]
    # Assign courses to professors
    professor_assignments = {course: '' for course in unique_courses}
    for i, course in enumerate(unique_courses):
        professor = professors[i % num_professors]
        professor_assignments[course] = professor
    # Assign profs to the courses that their qualified to teach
    prof_assigned_props = list()
    for code, course_list in courses.items(): 
        prof = professor_assignments[code]
        for course_assigned in course_list:
            prof_assigned_props.append(ProfessorAssigned(prof, course_assigned.course, course_assigned.term, course_assigned.day, course_assigned.time))
    # Create a dictionary of professors by term, time, and day and their assigned courses
    prof_book = defaultdict(list)
    for prop in prof_assigned_props:
        prof_book[(prop.term, prop.time, prop.day, prop.professor)].append(prop) 
    # Ensure that for each term, time, and day, there is exactly 1 professor assigned
    for prof_times in prof_book.values():
        constraint.add_exactly_one(E1, prof_times)

    return E1

if __name__ == "__main__":
    # Stage 1 - Course Scheduling
    print("Building Course Schedule Encoding...")
    C = schedule_programs()
    print("Begin compiling the encoding...")
    C = C.compile()
    print("\nSatisfiable: %s" % C.satisfiable())
    # print("# Solutions: %d" % count_solutions(C))
    print("VARS: ", len(C.vars()))
    print("OPs: ", C.size())
    course_schedule = C.solve()
    if course_schedule:
        # Stage 2 - Professor Scheduling
        print("\nBuilding Professor Schedule Encoding...")
        P = schedule_professors(course_schedule)
        print("Begin compiling the encoding...")
        P = P.compile()
        print("\nSatisfiable: %s" % P.satisfiable())
        # print("# Solutions: %d" % count_solutions(P))
        print("VARS: ", len(P.vars()))
        print("OPs: ", P.size())
        professor_schedule = P.solve()
        if professor_schedule:
            display_final_schedule(course_schedule, professor_schedule)
    else: 
        print("No solution found, ending program.")
