# List of classrooms available to schedule lectures in 
CLASSROOMS = [
    "A101", "A102", "A103", "A104", "A105", "A106", "A107", "A108", "A109", "A110",
    "B101", "B102", "B103", "B104", "B105", "B106", "B107", "B108", "B109", "B110",
]
# List of days that lectures can be scheduled
DAYS = [
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"
]
# List of times that a lecture can be scheduled on
TIMESLOTS = [
    "8AM-930AM", "930AM-11AM", "11AM-1230PM", "1230PM-2PM", ""
]
# List of the 8 different terms
TERMS = [
    'Fall 1', 'Winter 1', 'Fall 2', 'Winter 2', 'Fall 3', 'Winter 3', 'Fall 4', 'Winter 4',
]
# List of all the Professors
PROFS = [
    "Dr. Smith", "Dr. Johnson", "Dr. Williams", "Dr. Jones", "Dr. Brown", "Dr. Davis", "Dr. Miller", "Dr. Wilson",
]
# Dict of all the Professors with the courses they're qualified to teach
PROFS_QUAL = {
    "Dr. Smith": [], 
    "Dr. Johnson": [], 
    "Dr. Williams": [], 
    "Dr. Jones": [],
    "Dr. Brown": [], 
    "Dr. Davis": [], 
    "Dr. Miller": [], 
    "Dr. Wilson": [],
}
# List of all the Courses
COURSES = [
    "Math121", "Math122", "Math123", "Math124", "Math125", "Math126", "Math127", "Math128", "Math129", "Math130",
]
# Dict of all the Courses with the prerequisites required
COURSE_REQS = {
    "C1": [],
    "C2": ["C1"],
    "C3": ["C1", "C2"],
    "C4": [],
    "C5": ["C3"],
    "C6": [], 
    "C7": ["C5", "C6"],
    "C8": ["C4"],
    "C9": ["C7", "C8"],
    "C10": ["C9"],
    "C11": ["C10"],
    "C12": ["C11"],
    "C13": ["C12"],
    "C14": ["C13"],
    "C15": ["C14"],
    "C16": ["C15"],
    
    
}
# Nested Dict of All the Programs, with the requirements broken down by Year 
PROGRAMS = {
    "AI": {
        "Year1": ["AI101", "AI102", "AI103"],
        "Year2": ["AI201", "AI202", "AI203"],
        "Year3": ["AI301", "AI302", "AI303"],
        "Year4": ["AI401", "AI402", "AI403"],
    },
    "Bio Med": {
        "Year1": [],
        "Year2": [],
        "Year3": [],
        "Year4": [],
    },
    "Data Analytics": {
        "Year1": [],
        "Year2": [],
        "Year3": [],
        "Year4": [],
    }, 
    "Game Dev": {
        "Year1": [],
        "Year2": [],
        "Year3": [],
        "Year4": [],
    }, 
    "Security": {
        "Year1": [],
        "Year2": [],
        "Year3": [],
        "Year4": [],
    }, 
    "Fundamental": {
        "Year1": [],
        "Year2": [],
        "Year3": [],
        "Year4": [],
    }, 
    "Cog Sci": {
        "Year1": [],
        "Year2": [],
        "Year3": [],
        "Year4": [],
    }, 
    "Comp Sci": {
        "Year1": [],
        "Year2": [],
        "Year3": [],
        "Year4": [],
    }, 
    "Soft Design": {
        "Year1": [],
        "Year2": [],
        "Year3": [],
        "Year4": [],
    }, 
    "BioMed": {
        "Year1": [],
        "Year2": [],
        "Year3": [],
        "Year4": [],
    }, 
    "COMA": {
        "Year1": [],
        "Year2": [],
        "Year3": [],
        "Year4": [],
    }, 
    "Creative Arts": {
        "Year1": [],
        "Year2": [],
        "Year3": [],
        "Year4": [],
    }
}




