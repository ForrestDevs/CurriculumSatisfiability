from data import courses, semesters, students, professors

from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood

# These two lines make sure a faster SAT solver is used.
from nnf import config
config.sat_backend = "kissat"

# Encoding that will store all of your constraints
E = Encoding()

class Hashable:
    def __hash__(self):
        return hash(str(self))

    def __eq__(self, __value: object) -> bool:
        return hash(self) == hash(__value)

    def __repr__(self):
        return str(self)

# region Propositions
#############################################################################################################
# EXAMPLES:
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
# Define your propositions here:
#############################################################################################################

@proposition(E)
class Professor_Available(Hashable):
    def __init__(self, professor, term):
        self.professor = professor
        self.term = term

    def __repr__(self):
        return f"Professor_Available(professor={self.professor}, term={self.term})"


@proposition(E)
class Professor_Assigned:
    def __init__(self, professor, course, term):
        self.professor = professor
        self.course = course
        self.term = term

    def __repr__(self):
        return f"Professor_Assigned(professor={self.professor}, course={self.course}, term={self.term})"


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


@proposition(E)
class Course_Prerequisite:
    def __init__(self, course, prerequisite):
        self.course = course
        self.prerequisite = prerequisite

    def __repr__(self):
        return f"Course_Prerequisite(course={self.course}, prerequisite={self.prerequisite})"


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


@proposition(E)
class Classroom_Free:
    def __init__(self, room, term):
        self.room = room
        self.term = term

    def __repr__(self):
        return f"Classroom_Free(room={self.room}, term={self.term})"


@proposition(E)
class Course_Assigned_Room:
    def __init__(self, course, room, term):
        self.course = course
        self.room = room
        self.term = term

    def __repr__(self):
        return f"Course_Assigned_Room(course={self.course}, room={self.room}, term={self.term})"
# endregion


# Call your variables whatever you want
a = BasicPropositions("a")
b = BasicPropositions("b")
c = BasicPropositions("c")
d = BasicPropositions("d")
e = BasicPropositions("e")
# At least one of these will be true
x = FancyPropositions("x")
y = FancyPropositions("y")
z = FancyPropositions("z")



# E.add_constraint(Course_Assigned_Room(course, room, term) >> Course_Offered(course, term))
# E.add_constraint(Course_Assigned_Room(course, room, term) >> Classroom_Free(professor, course, term))


# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.
def example_theory():
    # Add custom constraints by creating formulas with the variables you created.
    E.add_constraint((a | b) & ~x)
    # Implication
    E.add_constraint(y >> z)
    # Negate a formula
    E.add_constraint(~(x & y))
    # You can also add more customized "fancy" constraints. Use case: you don't want to enforce "exactly one"
    # for every instance of BasicPropositions, but you want to enforce it for a, b, and c.:
    constraint.add_exactly_one(E, a, b, c)

    return E


if __name__ == "__main__":

    T = example_theory()
    # Don't compile until you're finished adding all your constraints!
    T = T.compile()
    # After compilation (and only after), you can check some of the properties
    # of your model:
    print("\nSatisfiable: %s" % T.satisfiable())
    print("# Solutions: %d" % count_solutions(T))
    print("   Solution: %s" % T.solve())

    print("\nVariable likelihoods:")
    for v, vn in zip([a, b, c, x, y, z], 'abcxyz'):
        # Ensure that you only send these functions NNF formulas
        # Literals are compiled to NNF here
        print(" %s: %.2f" % (vn, likelihood(T, v)))
    print()
