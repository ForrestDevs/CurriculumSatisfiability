# List of classrooms available to schedule lectures in
CLASSROOMS = [
    'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 
]
#  'A8', 'A9', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17', 'A18', 'A19', 'A20', 'A21', 'A22', 'A23', 'A24',
#  'A25', 'A26', 'A27', 'A28', 'A29', 'A30', 'A31', 'A32', 'A33', 'A34', 'A35', 'A36', 'A37', 'A38', 'A39', 'A40', 'A41', 'A42', 'A43', 'A44', 'A45', 'A46', 
#  'A47', 'A48', 'A49', 'A50', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11', 'B12', 'B13', 'B14', 'B15', 'B16', 'B17', 'B18', 'B19',
#  'B20', 'B21', 'B22', 'B23', 'B24', 'B25', 'B26', 'B27', 'B28', 'B29', 'B30', 'B31', 'B32', 'B33', 'B34', 'B35', 'B36', 'B37', 'B38', 'B39', 'B40', 
#  'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17', 'C18', 'C19', 'C20', 'C21', 'C22', 
#  'C23', 'C24', 'C25', 'C26', 'C27', 'C28', 'C29', 'C30', 'C31', 'C32', 'C33', 'C34', 'C35', 'C36', 'C37', 'C38', 'C39', 'C40'

# List of days that lectures can be scheduled
DAYS = [
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"
]

# List of times that a lecture can be scheduled on
TIMESLOTS = [
    "8AM-930AM", "930AM-11AM", "11AM-1230PM", "1230PM-2PM",
    "2PM-330PM", "330PM-5PM", "5PM-630PM", "630PM-8PM",
]
# "8PM-930PM", "8AM-10AM", "10AM-12PM", "12PM-2PM", "2PM-4PM",
#     "4PM-6PM", "6PM-8PM", "8:30AM-10AM", "10AM-11:30AM", "11:30AM-1PM", "1PM-2:30PM",
#     "2:30PM-4PM", "4PM-5:30PM", "5:30PM-7PM", "7PM-8:30PM",
#     "8:30PM-10PM",

# List of the 2 different terms
TERMS = [
    "T-1", "T-2",
]
# Dict of all the Courses with the prerequisites required
COURSES = {
    # 'E 1': {'credits': 3, 'reqs': []}, 
    # 'E 2': {'credits': 3, 'reqs': []}, 
    # 'E 3': {'credits': 3, 'reqs': []}, 
    # 'E 4': {'credits': 3, 'reqs': []}, 
    # 'BIOM 300': {'credits': 3, 'reqs': []}, 
    # 'CISC 330': {'credits': 3, 'reqs': []}, 
    # 'MATH 210': {'credits': 3, 'reqs': []}, 
    # 'MATH 311': {'credits': 3, 'reqs': []}, 
    # 'MATH 413': {'credits': 3, 'reqs': []}, 
    # 'MATH 414': {'credits': 3, 'reqs': []}, 
    # 'MATH 221': {'credits': 3, 'reqs': []}, 
    # 'MATH 280': {'credits': 3, 'reqs': []}, 
    # 'STAT 269': {'credits': 3, 'reqs': []}, 
    # 'MATH 401': {'credits': 3, 'reqs': []}, 
    # 'MATH 402': {'credits': 3, 'reqs': []}, 
    # 'MATH 406': {'credits': 3, 'reqs': []}, 
    # 'MATH 418': {'credits': 3, 'reqs': []}, 
    # 'MATH 474': {'credits': 3, 'reqs': []}, 
    # 'MATH 477': {'credits': 3, 'reqs': []}, 
    # 'STAT 456': {'credits': 3, 'reqs': []},
    # 'STAT 457': {'credits': 3, 'reqs': []}, 
    # 'STAT 462': {'credits': 3, 'reqs': []}, 
    # 'STAT 464': {'credits': 3, 'reqs': []}, 
    # 'STAT 471': {'credits': 3, 'reqs': []},
    # 'STAT 473': {'credits': 3, 'reqs': []}, 
    # 'STAT 486': {'credits': 3, 'reqs': []}, 
    # 'STAT 361': {'credits': 3, 'reqs': []}, 
    # 'STAT 463': {'credits': 3, 'reqs': []}, 
    # 'STAT 252': {'credits': 3, 'reqs': []}, 
    # 'STAT 268': {'credits': 3, 'reqs': ['']}, 
    # 'STAT 351': {'credits': 3, 'reqs': ['']}, 
    # 'CISC 371': {'credits': 3, 'reqs': []}, 
    # 'CISC 372': {'credits': 3, 'reqs': []}, 
    # 'CISC 455': {'credits': 3, 'reqs': []}, 
    # 'CISC 457': {'credits': 3, 'reqs': []}, 
    # 'CISC 462': {'credits': 3, 'reqs': []}, 
    # 'CISC 465': {'credits': 3, 'reqs': []}, 
    # 'CISC 467': {'credits': 3, 'reqs': []}, 
    # 'CISC 472': {'credits': 3, 'reqs': []},
    # 'CISC 473': {'credits': 3, 'reqs': []},
    # 'MATH 337': {'credits': 3, 'reqs': []},
    # 'MATH 339': {'credits': 3, 'reqs': []}, 
    # 'COGS 100': {'credits': 3, 'reqs': ['']}, 
    'CISC 121': {'credits': 3, 'reqs': []}, 
    'CISC 124': {'credits': 3, 'reqs': ['CISC 121']}, 
    # 'CISC 102': {'credits': 3, 'reqs': ['']}, 
    # 'MATH 112': {'credits': 3, 'reqs': ['']}, 
    # 'MATH 111': {'credits': 6, 'reqs': ['']}, 
    # 'MATH 110': {'credits': 6, 'reqs': ['']}, 
    'MATH 120': {'credits': 6, 'reqs': []}, 
    'MATH 121': {'credits': 6, 'reqs': []}, 
    # 'MATH 123': {'credits': 3, 'reqs': ['']}, 
    # 'MATH 124': {'credits': 3, 'reqs': ['']}, 
    # 'WRIT 125': {'credits': 3, 'reqs': ['']}, 
    # 'WRIT 175': {'credits': 3, 'reqs': ['']}, 
    # 'STAT 263': {'credits': 3, 'reqs': ['']}, 
    # 'PHIL 259': {'credits': 3, 'reqs': ['']}, 
    # 'APSC 221': {'credits': 3, 'reqs': ['']}, 
    # 'COMM 200': {'credits': 3, 'reqs': ['']}, 
    # 'COMM 251': {'credits': 3, 'reqs': ['']}, 
    # 'COGS 201': {'credits': 3, 'reqs': ['COGS 100', 'PSYC 100']}, 
    # 'CISC 226': {'credits': 3, 'reqs': ['CISC 124']}, 
    # 'CISC 271': {'credits': 3, 'reqs': ['CISC 101', 'CISC 110', 'CISC 151', 'CISC 121', 'MATH 110', 'MATH 111', 'MATH 112', 'MATH 120', 'MATH 121', 'MATH 123', 'MATH 124', 'MATH 126']}, 
    # 'CISC 203': {'credits': 3, 'reqs': ['CISC 121', 'CISC 102', 'MATH 110']}, 
    # 'CISC 204': {'credits': 3, 'reqs': ['CISC 121', 'CISC 102', 'MATH 110']}, 

    # 'CISC 220': {'credits': 3, 'reqs': ['CISC 121']}, 
    # 'CISC 221': {'credits': 3, 'reqs': ['CISC 124']}, 

    # 'CISC 223': {'credits': 3, 'reqs': ['CISC 124', 'CISC 204']}, 
    # 'CISC 235': {'credits': 3, 'reqs': ['CISC 124', 'CISC 203']}, 
    # 'CISC 324': {'credits': 3, 'reqs': ['CISC 221', 'CISC 235']}, 
    # 'CISC 360': {'credits': 3, 'reqs': ['CISC 124', 'CISC 204']}, 
    # 'CISC 365': {'credits': 3, 'reqs': ['CISC 203', 'CISC 204', 'CISC 235']}, 
    # 'CISC 325': {'credits': 3, 'reqs': ['CISC 124', 'CISC 235']}, 
    # 'CISC 327': {'credits': 3, 'reqs': ['CISC 220', 'CISC 124']}, 
    # 'CISC 322': {'credits': 3, 'reqs': ['CISC 223', 'CISC 235']}, 
    # 'CISC 326': {'credits': 3, 'reqs': ['CISC 223', 'CISC 235']}, 
    # 'CISC 282': {'credits': 3, 'reqs': ['CISC 124']}, 
    # 'CISC 320': {'credits': 3, 'reqs': ['CISC 235']}, 
    # 'CISC 332': {'credits': 3, 'reqs': ['CISC 102', 'CISC 124']}, 
    # 'CISC 335': {'credits': 3, 'reqs': ['CISC 324']},
    # 'CISC 340': {'credits': 3, 'reqs': ['CISC 221']}, 
    # 'CISC 352': {'credits': 3, 'reqs': ['CISC 235']},
    # 'CISC 425': {'credits': 3, 'reqs': ['CISC 325']}, 
    # 'CISC 434': {'credits': 3, 'reqs': ['CISC 324']}, 
    # 'CISC 437': {'credits': 3, 'reqs': ['CISC 324', 'CISC 327']},    
    # 'CISC 448': {'credits': 3, 'reqs': ['CISC 327']}, 
    # 'CISC 452': {'credits': 3, 'reqs': ['CISC 235']}, 
    # 'CISC 453': {'credits': 3, 'reqs': ['CISC 352']}, 
    # 'CISC 458': {'credits': 3, 'reqs': ['CISC 121', 'CISC 221', 'CISC 223']}, 
    # 'CISC 486': {'credits': 3, 'reqs': ['CISC 226', 'CISC 322', 'CISC 326', 'CISC 324', 'MATH 110', 'MATH 111', 'MATH 112']}, 
    # 'ELEC 470': {'credits': 3, 'reqs': ['']}, 
    # 'CISC 495': {'credits': 3, 'reqs': ['']}, 
    # 'CISC 422': {'credits': 3, 'reqs': ['CISC 223']}, 
    # 'CISC 423': {'credits': 3, 'reqs': ['CISC 223', 'CISC 235']}, 
    # 'CISC 497': {'credits': 3, 'reqs': ['CISC 352', 'CISC 365']}, 
    # 'CISC 498': {'credits': 3, 'reqs': ['']}, 
    # 'CISC 500': {'credits': 3, 'reqs': ['']}, 
    # 'COGS 400': {'credits': 3, 'reqs': ['CISC 235']}, 
    # 'COGS 499': {'credits': 3, 'reqs': ['']}
}

# Nested Dict of All the Programs, with the requirements 
PROGRAMS = {
    "Soft Design": {
        "reqs": [
            "CISC 121", "CISC 124", "CISC 102", "MATH 112", "MATH 111", "MATH 110", "MATH 120", "MATH 121", "MATH 123", "MATH 124", 
            "STAT 263", "STAT 268", "STAT 351", "CISC 203", "CISC 204", "CISC 220", "CISC 221", "CISC 223", "CISC 235", "CISC 324", 
            "CISC 360", "CISC 365", "CISC 325", "CISC 327", "CISC 422", "CISC 423", "CISC 497", "CIS 498",
        ],
        "options": [
            "CISC 322", "CISC 326", 
            "CISC 226", "CISC 271", "CISC 282", "CISC 320", "CISC 332", "CISC 335", "CISC 340", "CISC 352", "CISC 425", "CISC 434", 
            "CISC 437", "CISC 448", "CISC 452", "CISC 453", "CISC 458", "CISC 486", "ELEC 470", "PHIL 259", "WRIT 125", "WRIT 175", 
            "APSC 221", "COMM 200", "COMM 251",
        ],
        "electives": ["E 1", "E 2", "E 3", "E 4"],
    },
    "Cog Sci": {
        "req": [
            "CISC 121", "CISC 124", "CISC 102", "MATH 112", "MATH 111", "MATH 110", "COGS 100", "COGS 201", "CISC 203",
            "CISC 204", "CISC 221", "CISC 235", "STAT 263", "STAT 268", "STAT 351", "CISC 360", "CISC 352", "COGS 400", 
            "CISC 497", "CISC 495", "CISC 500", "COGS 499",
        ],
        "options": [
            "CISC 351", "CISC 371", "CISC 372", "CISC 451", "CISC 452", "CISC 453", "CISC 455", "CISC 467", 
            "CISC 473", "CISC 474", "CISC 220", "CISC 223", "CISC 226", "CISC 271", "CISC 325", "CISC 332", 
            "CISC 340", "CISC 365", "CISC 425", "CISC 454", "CISC 457", "CISC 465", "CISC 486", "CISC 496", 
            "CISC 500", "COGS 300", "LING 100", "LING 310", "LING 320", "LING 330", "LING 340", "LING 415", 
            "PHIL 111", "PHIL 115", "PHIL 250", "PHIL 261", "PHIL 270", "PHIL 311", "PHIL 351", "PHIL 359", 
            "PHIL 381", "PHIL 451", "PHIL 452", "PHIL 464", "PSYC 100", "PSYC 203", "PSYC 251", "PSYC 271", 
            "PSYC 305", "PSYC 320", "PSYC 321", "PSYC 323", "PSYC 350", "PSYC 352", "PSYC 353", "PSYC 355", 
            "PSYC 365", "PSYC 370", "PSYC 420", "PSYC 422", "PSYC 423", "PSYC 442", "PSYC 452"
        ],
        "electives": ["E 1", "E 2", "E 3", "E 4"],
    },
    "COMA": {
        "req": [
            "CISC 121", "CISC 124", "CISC 203", "CISC 204", "CISC 223", "CISC 235", "CISC 332", 
            "CISC 324", "CISC 360", "CISC 365", "CISC 326", "CISC 497", "CISC 495", "CISC 499", "CISC 500",
            "MATH 110", "CISC 102", "MATH 111", "MATH 120", "MATH 121", "MATH 123", "MATH 124", "MATH 210", 
            "MATH 211", "MATH 310", "MATH 311", "MATH 413", "MATH 414", "MATH 221", "MATH 280", "STAT 269", 
            "STAT 361", "STAT 463", "STAT 252", "STAT 268", "STAT 351"
            ],
        "options": [
            "BIOM 300", "CISC 271", "CISC 330", "CISC 371", "CISC 372", "CISC 422", 
            "CISC 455", "CISC 457", "CISC 462", "CISC 465", "CISC 467", "CISC 472", 
            "CISC 473", "CISC 500", "MATH 337", "MATH 339", "MATH 401", "MATH 402", 
            "MATH 406", "MATH 413", "MATH 414", "MATH 418", "MATH 474", "MATH 477", 
            "STAT 361", "STAT 456", "STAT 457", "STAT 462", "STAT 463", "STAT 464", 
            "STAT 471", "STAT 473", "STAT 486"
        ],
        "electives": ["E 1", "E 2", "E 3", "E 4"],
    },
    "AI": {
        "req": [
            "CISC 121", "CISC 124", "CISC 102", "MATH 112", "MATH 111", "MATH 110", "MATH 120", "MATH 121", "MATH 123", "MATH 124",
            "STAT 263", "STAT 268", "STAT 351", "CISC 203", "CISC 204", "CISC 220", "CISC 221", "CISC 223", "CISC 235", "CISC 324",
            "CISC 360", "CISC 365", "CISC 325", "CISC 327", "CISC 422", "CISC 423", "CISC 497", "CIS 498",
        ],
        "options": [
            "CISC 322", "CISC 326", 
            "CISC 226", "CISC 271", "CISC 282", "CISC 320", "CISC 332", "CISC 335", "CISC 340", "CISC 352", "CISC 425", "CISC 434", 
            "CISC 437", "CISC 448", "CISC 452", "CISC 453", "CISC 458", "CISC 486", "ELEC 470", "PHIL 259", "WRIT 125", "WRIT 175", 
            "APSC 221", "COMM 200", "COMM 251",
        ],
        "electives": ["E 1", "E 2", "E 3", "E 4"],
    },
}


# }
# # Nested Dict of All the Programs, with the requirements broken down by Year
# PROGRAMS = {
#     "AI": {
#         "Year1": ["AI101", "AI102", "AI103"],
#         "Year2": ["AI201", "AI202", "AI203"],
#         "Year3": ["AI301", "AI302", "AI303"],
#         "Year4": ["AI401", "AI402", "AI403"],
#     },
#     "Bio Med": {
#         "Year1": [],
#         "Year2": [],
#         "Year3": [],
#         "Year4": [],
#     },
#     "Data Analytics": {
#         "Year1": [],
#         "Year2": [],
#         "Year3": [],
#         "Year4": [],
#     },
#     "Game Dev": {
#         "Year1": [],
#         "Year2": [],
#         "Year3": [],
#         "Year4": [],
#     },
#     "Security": {
#         "Year1": [],
#         "Year2": [],
#         "Year3": [],
#         "Year4": [],
#     },
#     "Fundamental": {
#         "Year1": [],
#         "Year2": [],
#         "Year3": [],
#         "Year4": [],
#     },
#     "Cog Sci": {
#         "Year1": [],
#         "Year2": [],
#         "Year3": [],
#         "Year4": [],
#     },
#     "Comp Sci": {
#         "Year1": [],
#         "Year2": [],
#         "Year3": [],
#         "Year4": [],
#     },
#     "Soft Design": {
#         "Year1": [],
#         "Year2": [],
#         "Year3": [],
#         "Year4": [],
#     },
#     "BioMed": {
#         "Year1": [],
#         "Year2": [],
#         "Year3": [],
#         "Year4": [],
#     },
#     "COMA": {
#         "Year1": [],
#         "Year2": [],
#         "Year3": [],
#         "Year4": [],
#     },
#     "Creative Arts": {
#         "Year1": [],
#         "Year2": [],
#         "Year3": [],
#         "Year4": [],
#     }
# }


#############################################################################################################
# Test Data:
#############################################################################################################
# # List of classrooms available to schedule lectures in
# CLASSROOMS = [
#     "A101", "A102", "A103", "A104", "A105",
# ]

# # List of days that lectures can be scheduled
# DAYS = [
#     "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"
# ]

# # List of times that a lecture can be scheduled on
# TIMESLOTS = [
#     "8AM-930AM", "930AM-11AM", "11AM-1230PM", "1230PM-2PM",
# ]

# # List of the 8 different terms
# TERMS = [
#     'Fall 1', 'Winter 1', 'Fall 2', 'Winter 2', 'Fall 3', 'Winter 3', 'Fall 4', 'Winter 4',
# ]


# # List of all the Professors
# PROFS = [

#     "Dr. Smith", "Dr. Johnson", "Dr. Williams", "Dr. Jones",
# ]

# # Dict of all the Professors with the courses they're qualified to teach
# PROFS_QUAL = {
#     "Dr. Burton Ma": ["Cisc 124", "Cisc 220"],

#     "Dr. Johnson": ["Math124", "Math125", "Math126"],
#     "Dr. Williams": ["Math127", "Math128", "Math129"],
#     "Dr. Jones": ["Math130"],
# }

# # List of all the Courses
# COURSES = [
#     "Math121", "Math122", "Math123", "Math124", "Math125", "Math126", "Math127", "Math128", "Math129", "Math130",
# ]

# Dict of all the Courses with the prerequisites required
# COURSE_REQS = {
#     "Math121": [],
#     "Math122": ["Math121"],
#     "Math123": ["Math121", "Math122"],
#     "Math124": [],
#     "Math125": ["Math123"],
#     "Math126": [],
#     "Math127": ["Math125", "Math126"],
#     "Math128": ["Math124"],
#     "Math129": ["Math127", "Math128"],
#     "Math130": ["Math129"],
# }

# # Nested Dict of All the Programs, with the requirements broken down by Year
# PROGRAMS = {
#     "AI": {
#         "Year1": ["Math121", "Math122", "Math123"],
#         "Year2": ["Math124", "Math125", "Math126"],
#         "Year3": ["Math127", "Math128", "Math129"],
#         "Year4": ["Math130"],
#     },
#     "Data Analytics": {
#         "Year1": ["Math121", "Math122"],
#         "Year2": ["Math123", "Math124"],
#         "Year3": ["Math125", "Math126"],
#         "Year4": ["Math127", "Math128"],
#     },
#     "Comp Sci": {
#         "Year1": ["Math121", "Math122"],
#         "Year2": ["Math123", "Math124"],
#         "Year3": ["Math125", "Math126"],
#         "Year4": ["Math127", "Math128"],
#     },
# }

# PROGRAMS = {
#     "CogSci": {
#         "Year 1": [
#             "Cisc 121", "Cisc 124", "Cogs 100", "Math 110", "Cisc 102", "Math 111"
#         ],
#             "Math 111": [],
#             "Cisc 102": [],
#             "Math 112": [],
#             "Math 120": [],
#         },
#         "Year 2": {
#             "Cisc 203": [],
#             "Cisc 204": [],
#             "Cisc 221": [],
#             "Cisc 223": [],
#             "Cisc 235": [],
#             "Stat 263": [],
#             "Stat 268": []
#         },
#         "Year 3": {
#             "Cisc 322": [],
#             "Cisc 326": [],
#             "Cisc 324": [],
#             "Cisc 360": [],
#             "Cisc 365": []
#         },
#         "Year 4": {
#             "Cisc 497": []
#         }
#     },
#     "CompSci": {
#         "Year 1": {
#             "Cisc 121": [],
#             "Cisc 124": [],
#             "Math 110": [],
#             "Cisc 102": [],
#             "Math 111": [],
#             "Cisc 102": [],
#             "Math 112": [],
#             "Math 120": [],
#             "Math 121": [],
#             "Math 123": [],
#             "Math 124": []
#         },
#         "Year 2": {
#             "Cisc 203": {},
#             "Cisc 204": {},
#             "Cisc 221": {},
#             "Cisc 223": {},
#             "Cisc 235": {},
#             "Stat 263": {},
#             "Stat 268": {},
#         },
#         "Year 3": {
#             "Cisc 322": {},
#             "Cisc 326": {},
#             "Cisc 324": {},
#             "Cisc 360": {},
#             "Cisc 365": {}
#         },
#         "Year 4": {
#             "Cogs 400": {},
#             "Cisc 497": {}
#         }
#     },

# }


#############################################################################################################
# Test Data:
#############################################################################################################
# COURSES = {
#     'E 1': {'credits': 3, 'reqs': []}, 
#     'E 2': {'credits': 3, 'reqs': []}, 
#     'E 3': {'credits': 3, 'reqs': []}, 
#     'E 4': {'credits': 3, 'reqs': []}, 
#     'BIOM 300': {'credits': 3, 'reqs': []}, 
#     'CISC 330': {'credits': 3, 'reqs': []}, 
#     'MATH 210': {'credits': 3, 'reqs': []}, 
#     'MATH 311': {'credits': 3, 'reqs': []}, 
#     'MATH 413': {'credits': 3, 'reqs': []}, 
#     'MATH 414': {'credits': 3, 'reqs': []}, 
#     'MATH 221': {'credits': 3, 'reqs': []}, 
#     'MATH 280': {'credits': 3, 'reqs': []}, 
#     'STAT 269': {'credits': 3, 'reqs': []}, 
#     'MATH 401': {'credits': 3, 'reqs': []}, 
#     'MATH 402': {'credits': 3, 'reqs': []}, 
#     'MATH 406': {'credits': 3, 'reqs': []}, 
#     'MATH 418': {'credits': 3, 'reqs': []}, 
#     'MATH 474': {'credits': 3, 'reqs': []}, 
#     'MATH 477': {'credits': 3, 'reqs': []}, 
#     'STAT 456': {'credits': 3, 'reqs': []},
#     'STAT 457': {'credits': 3, 'reqs': []}, 
#     'STAT 462': {'credits': 3, 'reqs': []}, 
#     'STAT 464': {'credits': 3, 'reqs': []}, 
#     'STAT 471': {'credits': 3, 'reqs': []},
#     'STAT 473': {'credits': 3, 'reqs': []}, 
#     'STAT 486': {'credits': 3, 'reqs': []}, 
#     'STAT 361': {'credits': 3, 'reqs': []}, 
#     'STAT 463': {'credits': 3, 'reqs': []}, 
#     'STAT 252': {'credits': 3, 'reqs': []}, 
#     'STAT 268': {'credits': 3, 'reqs': ['']}, 
#     'STAT 351': {'credits': 3, 'reqs': ['']}, 
#     'CISC 371': {'credits': 3, 'reqs': []}, 
#     'CISC 372': {'credits': 3, 'reqs': []}, 
#     'CISC 455': {'credits': 3, 'reqs': []}, 
#     'CISC 457': {'credits': 3, 'reqs': []}, 
#     'CISC 462': {'credits': 3, 'reqs': []}, 
#     'CISC 465': {'credits': 3, 'reqs': []}, 
#     'CISC 467': {'credits': 3, 'reqs': []}, 
#     'CISC 472': {'credits': 3, 'reqs': []},
#     'CISC 473': {'credits': 3, 'reqs': []},
#     'MATH 337': {'credits': 3, 'reqs': []},
#     'MATH 339': {'credits': 3, 'reqs': []}, 
#     'COGS 100': {'credits': 3, 'reqs': ['']}, 
#     'CISC 121': {'credits': 3, 'reqs': ['']}, 
#     'CISC 124': {'credits': 3, 'reqs': ['CISC 121']}, 
#     'CISC 102': {'credits': 3, 'reqs': ['']}, 
#     'MATH 112': {'credits': 3, 'reqs': ['']}, 
#     'MATH 111': {'credits': 6, 'reqs': ['']}, 
#     'MATH 110': {'credits': 6, 'reqs': ['']}, 
#     'MATH 120': {'credits': 6, 'reqs': ['']}, 
#     'MATH 121': {'credits': 6, 'reqs': ['']}, 
#     'MATH 123': {'credits': 3, 'reqs': ['']}, 
#     'MATH 124': {'credits': 3, 'reqs': ['']}, 
#     'WRIT 125': {'credits': 3, 'reqs': ['']}, 
#     'WRIT 175': {'credits': 3, 'reqs': ['']}, 
#     'STAT 263': {'credits': 3, 'reqs': ['']}, 
#     'PHIL 259': {'credits': 3, 'reqs': ['']}, 
#     'APSC 221': {'credits': 3, 'reqs': ['']}, 
#     'COMM 200': {'credits': 3, 'reqs': ['']}, 
#     'COMM 251': {'credits': 3, 'reqs': ['']}, 
#     'COGS 201': {'credits': 3, 'reqs': [['COGS 100', 'PSYC 100']]}, 
#     'CISC 226': {'credits': 3, 'reqs': ['CISC 124']}, 
#     'CISC 271': {'credits': 3, 'reqs': [['CISC 101', 'CISC 110', 'CISC 151', 'CISC 121'], ['MATH 110', 'MATH 111', 'MATH 112'], ['MATH 120', 'MATH 121', ['MATH 123', 'MATH 124'], 'MATH 126']]}, 
#     'CISC 203': {'credits': 3, 'reqs': ['CISC 121', ['CISC 102', 'MATH 110']]}, 
#     'CISC 204': {'credits': 3, 'reqs': ['CISC 121', ['CISC 102', 'MATH 110']]}, 
#     'CISC 220': {'credits': 3, 'reqs': ['CISC 121']}, 
#     'CISC 221': {'credits': 3, 'reqs': ['CISC 124']}, 
#     'CISC 223': {'credits': 3, 'reqs': ['CISC 124', 'CISC 204']}, 
#     'CISC 235': {'credits': 3, 'reqs': ['CISC 124', 'CISC 203']}, 
#     'CISC 324': {'credits': 3, 'reqs': ['CISC 221', 'CISC 235']}, 
#     'CISC 360': {'credits': 3, 'reqs': ['CISC 124', 'CISC 204']}, 
#     'CISC 365': {'credits': 3, 'reqs': ['CISC 203', 'CISC 204', 'CISC 235']}, 
#     'CISC 325': {'credits': 3, 'reqs': ['CISC 124', 'CISC 235']}, 
#     'CISC 327': {'credits': 3, 'reqs': ['CISC 220', 'CISC 124']}, 
#     'CISC 322': {'credits': 3, 'reqs': ['CISC 223', 'CISC 235']}, 
#     'CISC 326': {'credits': 3, 'reqs': ['CISC 223', 'CISC 235']}, 
#     'CISC 282': {'credits': 3, 'reqs': ['CISC 124']}, 
#     'CISC 320': {'credits': 3, 'reqs': ['CISC 235']}, 
#     'CISC 332': {'credits': 3, 'reqs': ['CISC 102', 'CISC 124']}, 
#     'CISC 335': {'credits': 3, 'reqs': ['CISC 324']},
#     'CISC 340': {'credits': 3, 'reqs': ['CISC 221']}, 
#     'CISC 352': {'credits': 3, 'reqs': ['CISC 235']},
#     'CISC 425': {'credits': 3, 'reqs': ['CISC 325']}, 
#     'CISC 434': {'credits': 3, 'reqs': ['CISC 324']}, 
#     'CISC 437': {'credits': 3, 'reqs': ['CISC 324', 'CISC 327']},    
#     'CISC 448': {'credits': 3, 'reqs': ['CISC 327']}, 
#     'CISC 452': {'credits': 3, 'reqs': ['CISC 235']}, 
#     'CISC 453': {'credits': 3, 'reqs': ['CISC 352']}, 
#     'CISC 458': {'credits': 3, 'reqs': ['CISC 121', 'CISC 221', 'CISC 223']}, 
#     'CISC 486': {'credits': 3, 'reqs': ['CISC 226', ['CISC 322', 'CISC 326'], 
#     'CISC 324', ['MATH 110', 'MATH 111', 'MATH 112']]}, 
#     'ELEC 470': {'credits': 3, 'reqs': ['']}, 'CISC 495': {'credits': 3, 'reqs': ['']}, 
#     'CISC 422': {'credits': 3, 'reqs': ['CISC 223']}, 'CISC 423': {'credits': 3, 'reqs': ['CISC 223', 'CISC 235']}, 
#     'CISC 497': {'credits': 3, 'reqs': [['CISC 352', 'CISC 365']]}, 
#     'CISC 498': {'credits': 3, 'reqs': ['']}, 
#     'CISC 500': {'credits': 3, 'reqs': ['']}, 
#     'COGS 400': {'credits': 3, 'reqs': ['CISC 235']}, 
#     'COGS 499': {'credits': 3, 'reqs': ['']}
# }