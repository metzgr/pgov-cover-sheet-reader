import pandas as pd

"""
A dictionary mapping each goal status to a rank
"""
STATUS_RANK_MAP = {
    "Ahead": 3,
    "On track": 2,
    "Nearly on track": 1,
    "Blocked": 0
}

"""
Maps each goal status to a hex color
"""
STATUS_COLOR_MAP = {
    "Ahead": "#156966",
    "On track": "#319C98",
    "Nearly on track": "#67B5CE",
    "Blocked": "#FA935B"
}

CHALLENGES_LIST = ["Hiring", "Competing deadlines", "Legislation", "Lack of research", "Unclear guidance", "Unavailable data"]

SUMMARY_TEMPLATE_PATH = "src/resources/templates/Summary_Report_Template.docx"
APG_BREAKDOWN_TEMPLATE_PATH = "src/resources/templates/APG_Summary_Template.docx"

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

VIZ_DIRECTORY = "src/output/viz/images/"

"""
A path to the directory in which cover sheets are stored (relative to the location of the project's root).
"""
COVER_SHEET_DIRECTORY = "../cover_sheet/cover_sheets/"

"""
Text block template constants
"""
BOLD_REGEX = "\*\*(.*?)\*\*"
ITALICS_REGEX = "\*(.*?)\*"
BOLD_ITALICS_REGEX = ""
TEXT_BLOCK_TEMPLATES_DF = pd.read_excel("src/resources/templates/text_block_templates.xlsx")
