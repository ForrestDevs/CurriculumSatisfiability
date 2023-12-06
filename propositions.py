from bauhaus import Encoding, proposition

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

E1 = Encoding()

# Professor Props:
@proposition(E1)
class ProfessorAssigned(Hashable):
    def __init__(self, professor, course, term, day, time) -> None:
        self.professor = professor
        self.course = course
        self.term = term
        self.day = day
        self.time = time

    def __repr__(self) -> str:
        return f"Professor_Assigned(professor={self.professor}, course={self.course}, term={self.term}, day={self.day}, time={self.time})"


