from data import *
from tabulate import tabulate
from tqdm import tqdm
from itertools import combinations, product
from collections import defaultdict
from bauhaus import Encoding, proposition, constraint, Or, And
from bauhaus.utils import count_solutions, likelihood

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

# Course Props:
@proposition(E)
class CourseAssigned(Hashable):
    def __init__(self, course, room, term, day, time, var) -> None:
        self.course = course
        self.room = room
        self.term = term
        self.day = day
        self.time = time
        self.var = var

    def __repr__(self) -> str:
        return f"CourseAssigned(course={self.course}, room={self.room}, term={self.term}, day={self.day}, time={self.time}, var={self.var})"

@proposition(E)
class CoursePrerequisite(Hashable):
    def __init__(self, course, prerequisite) -> None:
        self.course = course
        self.prerequisite = prerequisite

    def __repr__(self) -> str:
        return f"Course_Prerequisite(course={self.course}, prerequisite={self.prerequisite})"

# Create the variables
variables = {(course, term, room, day, time): Var(f"{course}_{term}_{room}_{day}_{time}") for course, term, room, day, time in product(COURSES.keys(), TERMS, CLASSROOMS, DAYS, TIMESLOTS)}

# Create the CourseAssigned propositions with the corresponding variables
course_assigned_props = [CourseAssigned(course, room, term, day, time, variables[(course, term, room, day, time)]) for course, term, room, day, time in product(COURSES.keys(), TERMS, CLASSROOMS, DAYS, TIMESLOTS)]

# Define course prerequisites using CoursePrerequisite propositions
course_prerequisite_props = []
for course, value in tqdm(COURSES.items(), desc="Adding course prerequisite propositions"):
    if len(value['reqs']) > 0:
        print("REQS: ", value['reqs'])
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
            for i in range(len(TERMS) - 1):  # We subtract 1 because we're looking ahead by 1 term

                current_term = TERMS[i]
                next_term = TERMS[i + 1]
                
                for room, day, time in product(CLASSROOMS, DAYS, TIMESLOTS):
                    # Ensure that the prerequisite course is offered in the current term
                    prereq_in_current_term = CourseAssigned(prerequisite, room, current_term, day, time, variables[(prerequisite, current_term, room, day, time)])
                    course_in_next_term = CourseAssigned(course, room, next_term, day, time, variables[(course, next_term, room, day, time)]) 

                    E.add_constraint(prereq_in_current_term & course_in_next_term)

    # Ensure that courses with 6 credits are scheduled for both term 1 and term 2
    for key, value in tqdm(COURSES.items(), desc="Adding course constraints (2/3)"):
        if value['credits'] == 6:  # Check if the course has 6 credits
            assignments_T1 = [CourseAssigned(key, room, "T-1", day, time, variables[(key, "T-1", room, day, time)]) for room, day, time in product(CLASSROOMS, DAYS, TIMESLOTS)]
            assignments_T2 = [CourseAssigned(key, room, "T-2", day, time, variables[(key, "T-2", room, day, time)]) for room, day, time in product(CLASSROOMS, DAYS, TIMESLOTS)]
            # Add a constraint that at least one proposition from each list is true
            constraint.add_at_least_one(E, assignments_T1)
            constraint.add_at_least_one(E, assignments_T2)
    
    # Organize the propositions into a dictionary by course and term
    course_term_to_props = defaultdict(list)
    for prop in course_assigned_props:
        course_term_to_props[(prop.course, prop.term)].append(prop)

    print("COURESS: ", course_term_to_props)
    # Ensure that there are 2 lectures per course
    for course in tqdm(COURSES.keys(), desc="Adding course constraints (3/3)"):
        for term in TERMS:
            # Get all possible CourseAssigned propositions for this course and term
            assignments = course_term_to_props[(course, term)]
            assignment_vars = [prop.var for prop in assignments]
            # Add a constraint that at least two assignments can be true
            constraint.add_at_least_one(E, [And(var1, var2) for var1, var2 in combinations(assignment_vars, 2)])
            for var in assignment_vars:
                constraint.add_at_most_one(E, [var1 for var1 in assignment_vars if var1 != var])

    return E


def display_solution(solution):
    # Filter out the propositions that are true in the solution
    true_props = [prop for prop, value in solution.items() if value]

    # print(true_props)


    # Sort the propositions by term, day, and time
    sorted_props = sorted(true_props, key=lambda prop: (TERMS.index(prop.term), DAYS.index(prop.day), TIMESLOTS.index(prop.time)))

    # Prepare the data for the table
    table_data = []
    for prop in sorted_props:
        # professor = professor_by_time.get((prop.term, prop.day, prop.time), 'N/A')
        table_data.append([prop.course, prop.room, prop.term, prop.day, prop.time])

    # Display the table
    print(tabulate(table_data, headers=["Course", "Classroom", "Term", "Day", "Time"]))

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
    print("Solution: ", solution)
    if solution:
        display_solution(solution)

    # print()


