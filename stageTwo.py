from bauhaus import Encoding, proposition

E1 = Encoding()

class Hashable:
    def __hash__(self):
        return hash(str(self))

    def __eq__(self, __value: object) -> bool:
        return hash(self) == hash(__value)

    def __repr__(self):
        return str(self)

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

@proposition(E1)
class ProfessorQualified(Hashable): 
    def __init__(self, professor, course)-> None:
        self.professor = professor
        self.course = course

    def __repr__(self) -> str:
        return f"ProfessorQualifiedForCourse(professor={self.professor}, course={self.course})"