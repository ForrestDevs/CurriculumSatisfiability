# region SETUP
# Import necessary modules
from data import *
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


# region EXAMPLES
#############################################################################################################
# To create propositions, create classes for them first, annotated with "@proposition" and the Encoding
@proposition(E)
class BasicPropositions:

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"A.{self.data}"

# Different classes for propositions are useful because this allows for more dynamic constraint creation
# for propositions within that class. For example, you can enforce that "at least one" of the propositions
# that are instances of this class must be true by using a @constraint decorator.
# other options include: at most one, exactly one, at most k, and implies all.
# For a complete module reference, see https://bauhaus.readthedocs.io/en/latest/bauhaus.html
@constraint.at_least_one(E)
@proposition(E)
class FancyPropositions:

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"A.{self.data}"
    
#############################################################################################################  
# endregion EXAMPLES
  

# region Propositions
#############################################################################################################
# Professor Props:
#############################################################################################################
@proposition(E)
class Professor_Available(Hashable):
    def __init__(self, professor, term, day, time):
        self.professor = professor
        self.term = term
        self.day = day
        self.time = time

    def __repr__(self):
        return f"Professor_Available(professor={self.professor}, term={self.term}, day={self.day}, time={self.time})"

@proposition(E)
class Professor_Assigned(Hashable):
    def __init__(self, professor, course, term):
        self.professor = professor
        self.course = course
        self.term = term

    def __repr__(self):
        return f"Professor_Assigned(professor={self.professor}, course={self.course}, term={self.term})"
#############################################################################################################
# Course Props:
#############################################################################################################
@proposition(E)
class Course_Assigned_DT(Hashable):
    def __init__(self, course, term, day, time):
        self.course = course
        self.term = term
        self.day = day
        self.time = time

    def __repr__(self):
        return f"Course_Assigned_DT(course={self.course}, term={self.term}, day={self.day}, time={self.time})"
    
@proposition(E)
class CourseAssigned:
    def __init__(self, course, room, term, day, time) -> None:
        self.course = course
        self.room = room
        self.term = term
        self.day = day
        self.time = time

    def __repr__(self) -> str:
        return f"CourseAssigned(course={self.course}, room={self.room}, term={self.term}, day={self.day}, time={self.time})"
    
@proposition(E)
class Course_Prerequisite:
    def __init__(self, course, prerequisite):
        self.course = course
        self.prerequisite = prerequisite

    def __repr__(self):
        return f"Course_Prerequisite(course={self.course}, prerequisite={self.prerequisite})"

@proposition(E)
class Course_Offered:
    def __init__(self, course, term):
        self.course = course
        self.term = term

    def __repr__(self):
        return f"Course_Offered(course={self.course}, term={self.term})"


@proposition(E)
class Course_Can_Be_Scheduled:
    def __init__(self, course, term):
        self.course = course
        self.term = term

    def __repr__(self):
        return f"Course_Can_Be_Scheduled(course={self.course}, term={self.term})"
#############################################################################################################
# Program Props:
#############################################################################################################
@proposition(E)
class Program_Req_Course:
    def __init__(self, course, program):
        self.course = course
        self.program = program

    def __repr__(self):
        return f"Program_Req_Course(course={self.course}, program={self.program})"


@proposition(E)
class Program_Shares_PreReq:
    def __init__(self, program1, program2, course):
        self.program1 = program1
        self.program2 = program2
        self.course = course

    def __repr__(self):
        return f"Program_Shares_PreReq(program1={self.program1}, program2={self.program2}, course={self.course})"


@proposition(E)
class Program_Can_Complete:
    def __init__(self, program, term):
        self.program = program
        self.term = term
        
    def __repr__(self):
        return f"Program_Can_Complete(program={self.program}, term={self.term})"
#############################################################################################################
# Classroom Props:
#############################################################################################################
@proposition(E)
class Classroom_Available(Hashable):
    def __init__(self, room, term, day, time) -> None:
        self.room = room
        self.term = term
        self.day = day
        self.time = time

    def __repr__(self) -> str:
        return f"Classroom_Free(room={self.room}, term={self.term}, day={self.day}, time={self.time})"
# endregion


# region INIT Props
# Define program requirements using Program_Req_Course propositions
# prog_req_props = []
# for program in PROGRAMS:
#     for course in program.requirements: 
#         prog_req_props.append(Program_Req_Course(course, program))


# Define professor and classroom availability using Professor_Available and Classroom_Available propositions
prof_avail_props = []
for professor in PROFS:
    for term in TERMS:
        for day in DAYS:
            for time in TIMESLOTS:
                prof_avail_props.append(Professor_Available(professor, term, day, time))

room_avail_props = []                
for room in CLASSROOMS:
    for term in TERMS:
        for day in DAYS:
            for time in TIMESLOTS:
                room_avail_props.append(Classroom_Available(room, term, day, time))
                
# Define course prerequisites using Course_Prerequisite propositions


# Define course scheduling using Course_Assigned_DT and Course_Assigned_Room propositions
course_assigned_props = []
for course in COURSES:
    for term in TERMS:
        for room in CLASSROOMS:
            for day in DAYS:
                for time in TIMESLOTS:
                    course_assigned_props.append(CourseAssigned(course, room, term, day, time))
# endregion INIT Props


# region Add Constraints + Build Theory
#  Build the theory
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.
def schedule_programs():

    # Let's ensure that a course can't be assigned to a classroom that already has a course scheduled at a specific day and time.
    classroom_assignments = {}
    for assignment in course_assigned_props:
        classroom = assignment.room
        day = assignment.day
        time = assignment.time

        if classroom not in classroom_assignments:
            classroom_assignments[classroom] = {}

        if day not in classroom_assignments[classroom]:
            classroom_assignments[classroom][day] = {}

        if time not in classroom_assignments[classroom][day]:
            classroom_assignments[classroom][day][time] = []
        
        classroom_assignments[classroom][day][time].append(assignment.course)

    for classroom, days in classroom_assignments.items():
        for day, times in days.items():
            for time, courses in times.items():
                if len(courses) > 1:
                    for i in range(len(courses)):
                        for j in range(i + 1, len(courses)):
                            # Ensure that no two courses are assigned to the same classroom at the same day and time
                            constraint.add_exactly_one(E, courses[i], courses[j])


    # Create a dictionary to keep track of professor assignments for each day and time
    professor_assignments = {}
    # Assume you have propositions for Professor_Assigned and Course_Assigned_DT
    # Replace these with your actual propositions
    # For each course assigned to a professor, add it to the professor_assignments list
    for assignment in Professor_Assigned.instances:
        professor = assignment.professor
        day = assignment.day
        time = assignment.time

        if professor not in professor_assignments:
            professor_assignments[professor] = {}

        if day not in professor_assignments[professor]:
            professor_assignments[professor][day] = {}

        if time not in professor_assignments[professor][day]:
            professor_assignments[professor][day][time] = []

        professor_assignments[professor][day][time].append(assignment.course)
    # Now, create a constraint to ensure a professor is not assigned to more than one place at the same time
    for professor, days in professor_assignments.items():
        for day, times in days.items():
            for time, courses in times.items():
                if len(courses) > 1:
                    for i in range(len(courses)):
                        for j in range(i + 1, len(courses)):
                            # Ensure that no two courses are assigned to the same professor at the same day and time
                            constraint.add_exactly_one(E, courses[i], courses[j])

    return E
# endregion Add Constraints + Build Theory


# region Compile + Run
if __name__ == "__main__":
    T = schedule_programs()
    T = T.compile()
    print("\nSatisfiable: %s" % T.satisfiable())
    print("# Solutions: %d" % count_solutions(T))
    print("   Solution: %s" % T.solve())
# endregion Compile + Run