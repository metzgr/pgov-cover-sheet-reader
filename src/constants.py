"""
Stores all of the constants that are needed for project-wide use.
"""

import pandas as pd

"""
PATHS
"""
SUMMARY_TEMPLATE_PATH = "src/resources/templates/docx/Summary_Report_Template.docx"
APG_BREAKDOWN_TEMPLATE_PATH = "src/resources/templates/docx/APG_Summary_Template.docx"
TEXT_BLOCK_TEMPLATES_PATH = "src/resources/templates/excel/text_block_templates.xlsx"
CHALLENGES_RECOMMENDATIONS_MAP_PATH = "src/resources/templates/excel/challenges_recommendations_map.xlsx"

"""
DIRECTORIES
"""
VIZ_DIRECTORY = "src/output/viz/images/"

# A path to the directory in which cover sheets are stored (relative to the location of the project's root).
COVER_SHEET_DIRECTORY = "../cover_sheet/cover_sheets/"

"""
COLUMN NAME LISTS
"""
CHALLENGES_LIST = ["Hiring technical staff", "Inadequate technical solutions", "Challenge 3", "Challenge 4", "Challenge 5", "Challenge 6"]

# List containing administration goals, which are also used as column names.
THEMES_LIST = ["Climate", "Equity", "Recovery"]

"""
GOAL STATUSES
"""
# A dictionary mapping each goal status to a rank
STATUS_RANK_MAP = {
    "Ahead": 3,
    "On track": 2,
    "Nearly on track": 1,
    "Blocked": 0
}

"""
STYLING
"""
# Maps each goal status to a hex color
STATUS_COLOR_MAP = {
    "Ahead": "#156966",
    "On track": "#319C98",
    "Nearly on track": "#67B5CE",
    "Blocked": "#FA935B"
}

"""
AGENCY NAMES/ABBREVIATIONS
"""
AGENCY_NAME_TO_ABBREVIATION = {
    "Department of Agriculture": "USDA", 
    "Department of Commerce": "DOC",
    "Department of Defense": "DOD",
    "Department of Education": "ED",
    "Department of Energy": "DOE",
    "Department of Health and Human Services": "HHS",
    "Department of Homeland Security": "DHS",
    "Department of Housing and Urban Development": "HUD",
    "Department of Interior": "DOI",
    "Department of Justice": "DOJ",
    "Department of Labor": "DOL",
    "Department of State": "DOS",
    "Department of Transportation": "DOT",
    "Department of Treasury": "USDT",
    "Department of Veterans Affairs": "VA",
    "Environmental Protection Agency": "EPA",
    "National Aeronautics and Space Administration": "NASA",
    "Agency for International Development": "USAID",
    "Social Security Administration": "SSA",
    "General Services Administration": "GSA",
    "National Science Foundation": "NSF",
    "Office of Personnel Management": "OPM",
    "Small Business Administration": "SBA"
}

AGENCY_ABBREVIATION_TO_NAME = {value: key for key, value in AGENCY_NAME_TO_ABBREVIATION.items()}

"""
MARKDOWN REGEX
"""
BOLD_REGEX = "\*\*(.*?)\*\*"
ITALICS_REGEX = "\*(.*?)\*"
BOLD_ITALICS_REGEX = ""

"""
NO-CODE SPREADSHEETS
"""
TEXT_BLOCK_TEMPLATES_DF = pd.read_excel(TEXT_BLOCK_TEMPLATES_PATH, skiprows=1)
CHALLENGES_RECOMMENDATIONS_MAP_DF = pd.read_excel(CHALLENGES_RECOMMENDATIONS_MAP_PATH)
