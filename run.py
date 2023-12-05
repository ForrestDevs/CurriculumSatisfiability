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

    # # Ensure that courses with 6 credits are scheduled for both term 1 and term 2
    # for key, value in tqdm(COURSES.items(), desc="Adding course constraints (2/3)"):
    #     if value['credits'] == 6:  # Check if the course has 6 credits
    #         assignments_T1 = [CourseAssigned(key, room, "T-1", day, time) for room, day, time in product(CLASSROOMS, DAYS, TIMESLOTS)]
    #         # Create a list of CourseAssigned propositions for term "T-2"
    #         assignments_T2 = [CourseAssigned(key, room, "T-2", day, time) for room, day, time in product(CLASSROOMS, DAYS, TIMESLOTS)]
    #         # Add a constraint that at least one proposition from each list is true
    #         constraint.add_at_least_one(E, assignments_T1)
    #         constraint.add_at_least_one(E, assignments_T2)
    
    # Organize the propositions into a dictionary by course and term
    course_term_to_props = defaultdict(list)
    for prop in course_assigned_props:
        course_term_to_props[(prop.course, prop.term)].append(prop)

    print("COURESS: ", course_term_to_props)
    # Ensure that there are 2 lectures per course
    for course in tqdm(COURSES.keys(), desc="Adding course constraints (3/3)"):
        for term in TERMS:
              # Create a list of all possible CourseAssigned propositions for this course and term
            assignments = [CourseAssigned(course, room, term, day, time) for room, day, time in product(CLASSROOMS, DAYS, TIMESLOTS)]

            # Add a constraint that at most two of these propositions are true
            constraint.at_most_k(assignments, 2)

            # Generate all combinations of pairs from assignments
            pair_combinations = list(combinations(assignments, 2))

            # Create a new list where each element is a conjunction of a pair of assignments
            pair_constraints = [E.add_constraint(pair[0] & pair[1]) for pair in pair_combinations]

            # Add a constraint that exactly one of these pair constraints is true
            constraint.add_exactly_one(E, pair_constraints)

            # # Create a list of all possible CourseAssigned propositions for this course and term
            # assignments = [CourseAssigned(course, room, term, day, time) for room, day, time in product(CLASSROOMS, DAYS, TIMESLOTS)]

            # # Add a constraint that at most two of these propositions are true
            # constraint.at_most_k(E, assignments, 2)

            # # Create and add a constraint that at least two of these propositions are true
            # # We create combinations of all propositions and ensure that at least one combination is true
            # at_least_two = [E.add_constraint(assignments[i] & assignments[j]) for i, j in combinations(range(len(assignments)), 2)]
            # E.add_constraint(sum(at_least_two) >= 1)
            # constraint.add_exactly_one
            # # Create a list of all possible CourseAssigned propositions for this course and term
            # assignments = [CourseAssigned(course, room, term, day, time) for room, day, time in product(CLASSROOMS, DAYS, TIMESLOTS)]
            
            # constraint.at_most_k(E, assignments, 2)
            # E.add_constraint()
            
            # # Create a list of all possible combinations of 2 assignments
            # assignment_pairs = list(combinations(assignments, 2))
            # # Create a list of constraints, each indicating that at most one assignment in a pair can be true
            # constraints = [Or(~assignment1, ~assignment2) for assignment1, assignment2 in assignment_pairs]
            # # Add all constraints to the encoding
            # for constraintF in constraints:
            #     E.add_constraint(constraintF)

    # for course in tqdm(COURSES.keys(), desc="Adding course constraints (3/3)"):
    #     for term in TERMS:
    #         # Create a list of all possible CourseAssigned propositions for this course and term
    #         assignments = [CourseAssigned(course, room, term, day, time) for room, day, time in product(CLASSROOMS, DAYS, TIMESLOTS)]
    #         # Create a list of all possible combinations of 2 assignments
    #         assignment_pairs = list(combinations(assignments, 2))
    #         # Create a list of constraints, each indicating that exactly one assignment in a pair can be true
    #         constraints = [Or(assignment1, assignment2) for assignment1, assignment2 in assignment_pairs]
    #         # Add a constraint that at least one pair of assignments is true
    #         E.add_constraint(Or(constraints))
    #         # Add constraints that at most one assignment in each pair can be true
    #         for constraintF in constraints:
    #             E.add_constraint(constraintF)

        
        # for term in TERMS: 
        #     # Add each lecture to the list for its time slot
        #     for room, day, time in product(CLASSROOMS, DAYS, TIMESLOTS):
        #         lecture = CourseAssigned(course, room, term, day, time)
        #         lectures_by_timeslot[(day, time)].append(lecture)
        #     # Ensure that no more than one lecture is scheduled at the same time
        #     for lectures in lectures_by_timeslot.values():
        #         constraint.add_at_most_one(E, lectures)

        #     # Ensure that at least 2 lectures are scheduled
        #     for lectures in lectures_by_timeslot.values():
        #         if len(lectures) > 1:
        #             constraint.add_at_least_one(E, lectures)

    # Classroom Constraints:
    # Ensure that a course can't be assigned to a classroom that already has a course scheduled at a specific day and time.
    # assignments_by_block = defaultdict(list)
    # for assignment in course_assigned_props:
    #     block = (assignment.room, assignment.term, assignment.day, assignment.time)
    #     assignments_by_block[block].append(assignment)
    # for assignments in tqdm(assignments_by_block.values(), desc="Adding classroom constraints"):
    #     for assignment1, assignment2 in combinations(assignments, 2):
    #         E.add_constraint(~assignment1 | ~assignment2)

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


