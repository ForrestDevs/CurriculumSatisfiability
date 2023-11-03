# region SETUP
# Import necessary modules
from data import *
from tabulate import tabulate
from itertools import combinations
from collections import defaultdict
from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood
# These two lines make sure a faster SAT solver is used.
from nnf import config
config.sat_backend = "kissat"
# Encoding that will store all of your constraints
E = Encoding()
# A base class to implement hashable
class Hashable:
    def __hash__(self):
        return hash(str(self))

    def __eq__(self, __value: object) -> bool:
        return hash(self) == hash(__value)

    def __repr__(self):
        return str(self)
# endregion SETUP
# region Propositions
#############################################################################################################
# Professor Props:
#############################################################################################################
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
#############################################################################################################
# Course Props:
#############################################################################################################
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
#############################################################################################################
# Program Props:
#############################################################################################################
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
#############################################################################################################
# Classroom Props:
#############################################################################################################
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
# endregion


# region INIT Props
#############################################################################################################
# Professor Props:
#############################################################################################################
# Initialize a dictionary to store the assignments of each professor
professor_assignments = {professor: set() for professor in PROFS}

# Initialize the props for professor qualifications
professor_qualified_props = []
for professor, courses in PROFS_QUAL.items():
    for course in courses:
        professor_qualified_props.append(ProfessorQualified(professor, course))

# Define professor assignments using ProfessorAssigned propositions
prof_assigned_props = []
for professor in PROFS:
    for term in TERMS:
        for course in COURSES:
            for day in DAYS:
                for time in TIMESLOTS:
                    prof_assigned_props.append(ProfessorAssigned(professor, course, term, day, time))

# Group the ProfessorAssigned propositions by professor, term, day, and time
assignments_by_time = defaultdict(list)
for assignment in prof_assigned_props:
    key = (assignment.professor, assignment.term, assignment.day, assignment.time)
    assignments_by_time[key].append(assignment)
#############################################################################################################
# Course Props:
#############################################################################################################
# Define course scheduling using CourseAssigned propositions
course_assigned_props = []
for course in COURSES:
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
#############################################################################################################
# Program Props:
#############################################################################################################
# Define program requirements using ProgramReqCourse propositions
program_req_course_props = []
for program, years in PROGRAMS.items():
    for year, courses in years.items():
        for course in courses:
            program_req_course_props.append(ProgramReqCourse(course, program, year))
# TODO: Intialize the props for program prerequisite sharing
program_shares_prereq_props = []
for program1, program2 in combinations(PROGRAMS.keys(), 2):
    for course in COURSES:
        program_shares_prereq_props.append(ProgramSharesPreReq(program1, program2, course))
#############################################################################################################
# Classroom Props:
#############################################################################################################
# Define classroom assignments using ClassroomAssigned propositions
classroom_assigned_props = []
for room in CLASSROOMS:
    for term in TERMS:
        for course in COURSES:
            for day in DAYS:
                for time in TIMESLOTS:
                    classroom_assigned_props.append(ClassroomAssigned(room, course, term, day, time))
# endregion INIT Props


# region Add Constraints + Build Theory
#  Build the theory
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.
def schedule_programs():
    print("Adding constraints...")
    #############################################################################################################
    print("Adding prof constraints...")
    # Professor Constraints:
    #############################################################################################################
    # Ensure that a professor isn't assigned to teach two courses at the same time
    [constraint.add_at_most_one(E, assignments) for assignments in assignments_by_time.values()]

    # Ensure that Profs can only teach courses for which they're qualified
    for professor in PROFS: 
        for course in COURSES:
            for term in TERMS:
                for day in DAYS:
                    for time in TIMESLOTS:
                        # If the professor is not qualified to teach the course,
                        # then ensure that the professor is not assigned to teach that course.
                        if not ProfessorQualified(professor, course) in professor_qualified_props:
                            E.add_constraint(~ProfessorAssigned(professor, course, term, day, time))
    #############################################################################################################
    print("Adding course constraints...")
    # Course Constraints:
    #############################################################################################################
    
    # TODO: When adding the following constraints, It severly filiters down the number of solutions
    #  to the point where if there isnt substantial data then it will not find a solution
    # Ensure that prerequisites are scheduled in a term before the course that requires them
    for prop in course_prerequisite_props:
        course = prop.course
        prerequisite = prop.prerequisite
        for i in range(len(TERMS) - 1):  # We subtract 1 because we're looking ahead by 1 term

            current_term = TERMS[i]
            next_term = TERMS[i + 1]
        
            for room in CLASSROOMS:
                for day in DAYS:
                    for time in TIMESLOTS:
                        # Ensure that the prerequisite course is offered in the current term
                        prereq_in_current_term = CourseAssigned(prerequisite, room, current_term, day, time)
                        # And the course that requires it is offered in the next term
                        course_in_next_term = CourseAssigned(course, room, next_term, day, time)
                        E.add_constraint(prereq_in_current_term & course_in_next_term)
    # Ensure that there are at least 2 lectures per course
    for course in COURSES:
        for term in TERMS: 
            # Create a dictionary to store the lectures for each time slot
            lectures_by_timeslot = {(day, time): [] for day in DAYS for time in TIMESLOTS}
            # Add each lecture to the list for its time slot
            for room in CLASSROOMS:
                for day in DAYS:
                    for time in TIMESLOTS:
                        lecture = CourseAssigned(course, room, term, day, time)
                        lectures_by_timeslot[(day, time)].append(lecture)
            # Ensure that no more than one lecture is scheduled at the same time
            for lectures in lectures_by_timeslot.values():
                constraint.add_at_most_one(E, lectures)
            # Ensure that at least 2 lectures are scheduled
            for timeslot1, timeslot2 in combinations(lectures_by_timeslot.keys(), 2):
                lectures1 = lectures_by_timeslot[timeslot1]
                lectures2 = lectures_by_timeslot[timeslot2]
                constraint.add_at_least_one(E, lectures1 + lectures2)
   
   #############################################################################################################
    print("Adding program constraints...")
    # Program Constraints:
    #############################################################################################################

    # Ensure that a course is only scheduled in terms that correspond to the year it's required in
    for prop in program_req_course_props:
        # Get the year from the proposition
        year = prop.year
        # Convert the year to an integer (assuming it's a string like 'Year1', 'Year2', etc.)
        year_num = int(year[4:])  # This gets the number part of the string
        # Calculate the terms that correspond to this year
        # Assuming that 'Fall 1' and 'Winter 1' correspond to 'Year1', 'Fall 2' and 'Winter 2' correspond to 'Year2', etc.
        terms_for_year = [f'Fall {year_num}', f'Winter {year_num}']
        # Add a constraint that the course can only be scheduled in these terms
        for term in TERMS:
            for day in DAYS:
                for time in TIMESLOTS:
                    for room in CLASSROOMS:
                        if term not in terms_for_year:
                            E.add_constraint(~CourseAssigned(prop.course, room, term, day, time))
    
    # TODO: The following constraint makes the program crash need to debug
    # Ensure that a program can only be completed if all of its required courses are scheduled
    # for program, years in PROGRAMS.items():
    #     for year, courses in years.items():
    #         # For each term in the year
    #         for term in [f'Fall {year[4:]}', f'Winter {year[4:]}']:
    #             # For each course required in the year
    #             for course in courses:
    #                 # Add a constraint that the course must be scheduled in at least one slot
    #                 E.add_constraint(
    #                     constraint.add_at_least_one(
    #                         E,
    #                         [CourseAssigned(course, room, term, day, time) for room in CLASSROOMS for day in DAYS for time in TIMESLOTS]
    #                     )
    #                 )


    #############################################################################################################
    print("Adding classroom constraints...")
    # Classroom Constraints:
    #############################################################################################################
    # Ensure that a course can't be assigned to a classroom that already has a course scheduled at a specific day and time.
    for room in CLASSROOMS:
        for term in TERMS:
            for day in DAYS:
                for time in TIMESLOTS:
                    #  For each combination of room, term, day, and time, create a list of CourseAssigned propositions
                    # Each proposition represents a course being assigned to the current room at the current term, day, and time
                    courses = [CourseAssigned(course, room, term, day, time) for course in COURSES]
                    # Add a constraint that at most one of these propositions can be true
                    # This ensures that at most one course can be assigned to the current room at the current term, day, and time
                    constraint.add_at_most_one(E, courses)
    #############################################################################################################
    return E
# endregion Add Constraints + Build Theory




# region Compile + Run

# Idea for displaying the solution:
#  I could break the solution down by program, and show that the courses required for each program are scheduled in the correct terms
#  I could also show that the prerequisites are scheduled in the correct terms
#  I could also show that the courses are scheduled in the correct terms

def display_solution(solution):
    # Filter out the propositions that are true in the solution
    true_props = [prop for prop, value in solution.items() if value]

    print(true_props)

    # Create a dictionary mapping from (term, day, time) to professor
    # professor_by_time = {(prop.term, prop.day, prop.time): prop.professor for prop, value in solution.items() if value and isinstance(prop, type(ProfessorAssigned))}

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
    T = schedule_programs()
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


