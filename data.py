# List of classrooms available to schedule lectures in
CLASSROOMS = [
    'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17', 'A18', 'A19', 'A20', 'A21', 'A22', 'A23', 'A24',
    'A25', 'A26', 'A27', 'A28', 'A29', 'A30', 'A31', 'A32', 'A33', 'A34', 'A35', 'A36', 'A37', 'A38', 'A39', 'A40', 'A41', 'A42', 'A43', 'A44', 'A45', 'A46', 
    'A47', 'A48', 'A49', 'A50', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11', 'B12', 'B13', 'B14', 'B15', 'B16', 'B17', 'B18', 'B19',
    'B20', 'B21', 'B22', 'B23', 'B24', 'B25', 'B26', 'B27', 'B28', 'B29', 'B30', 'B31', 'B32', 'B33', 'B34', 'B35', 'B36', 'B37', 'B38', 'B39', 'B40', 
    'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17', 'C18', 'C19', 'C20', 'C21', 'C22', 
    'C23', 'C24', 'C25', 'C26', 'C27', 'C28', 'C29', 'C30', 'C31', 'C32', 'C33', 'C34', 'C35', 'C36', 'C37', 'C38', 'C39', 'C40'
]

# List of days that lectures can be scheduled
DAYS = [
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"
]

# List of times that a lecture can be scheduled on
TIMESLOTS = [
    "8AM-930AM", "930AM-11AM", "11AM-1230PM", "1230PM-2PM",
    "2PM-330PM", "330PM-5PM", "5PM-630PM", "630PM-8PM",
    "8PM-930PM", "8AM-10AM", "10AM-12PM", "12PM-2PM", "2PM-4PM",
    "4PM-6PM", "6PM-8PM", "8:30AM-10AM", "10AM-11:30AM", "11:30AM-1PM", "1PM-2:30PM",
    "2:30PM-4PM", "4PM-5:30PM", "5:30PM-7PM", "7PM-8:30PM",
    "8:30PM-10PM",
]

# List of the 2 different terms
TERMS = [
    "T-1", "T-2",
]
# Dict of all the Courses with the prerequisites required
COURSE_REQS = {
    "E 1": [],
    "E 2": [],
    "E 3": [],
    "E 4": [],
    "COGS 100": [],
    "COGS 201": [],
    "COGS 400": [],
    "CISC 121": [],
    "CISC 124": [],
    "CISC 102": [],
    "MATH 112": [],
    "MATH 111": [],
    "MATH 110": [],
    "MATH 120": [],
    "MATH 121": [],
    "MATH 123": [],
    "MATH 124": [],
    "STAT 263": [],
    "STAT 268": [],
    "STAT 351": [],
    "CISC 203": [],
    "CISC 204": [],
    "CISC 220": [],
    "CISC 221": [],
    "CISC 223": [],
    "CISC 235": [],
    "CISC 324": [],
    "CISC 360": [],
    "CISC 365": [],
    "CISC 325": [],
    "CISC 327": [],
    "CISC 422": [],
    "CISC 423": [],
    "CISC 497": [],
    "CIS 498": [],
    "CISC 322": [],
    "CISC 326": [],
    "CISC 226": [],
    "CISC 271": [],
    "CISC 282": [],
    "CISC 320": [],
    "CISC 332": [],
    "CISC 335": [],
    "CISC 340": [],
    "CISC 352": [],
    "CISC 425": [],
    "CISC 434": [],
    "CISC 437": [],
    "CISC 448": [],
    "CISC 452": [],
    "CISC 453": [],
    "CISC 458": [],
    "CISC 486": [],
    "ELEC 470": [],
    "PHIL 259": [],
    "WRIT 125": [],
    "WRIT 175": [],
    "APSC 221": [],
    "COMM 200": [],
    "COMM 251": [],
    "CISC 495": [], 
    "CISC 500": [], 
    "COGS 499": [],
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
            "CISC 121", "CISC 124", "CISC 102", "MATH 112", "MATH 111", "MATH 110", "COGS 100", "COGS 201", "CISC 203", "CISC 204", "CISC 221", "CISC 235", "STAT 263", "STAT 268", "STAT 351",
            "CISC 360", "CISC 352", "COGS 400", "CISC 497", "CISC 495", "CISC 500", "COGS 499",
        ],
        "options": [""],
        "electives": [],
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
