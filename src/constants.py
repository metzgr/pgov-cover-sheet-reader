"""
Stores all of the constants that are needed for project-wide use.
"""

import pandas as pd

"""
CENTRAL DATABASE
"""
DATABASE_PATH = "../dummy_cover_sheet_data.csv"

"""
OUTPUT PATH
"""
OUTPUT_DIR = "src/output/docx/summary_reports/"

"""
TEMPLATE PATHS
"""
# .docx templates
SUMMARY_TEMPLATE_PATH = "src/templates/docx/Summary_Report_Template.docx"
APG_BREAKDOWN_TEMPLATE_PATH = "src/templates/docx/APG_Summary_Template.docx"

# No-code spreadsheets
TEXT_BLOCK_TEMPLATES_PATH = "src/templates/excel/text_block_templates.xlsx"
CHALLENGES_RECOMMENDATIONS_MAP_PATH = "src/templates/excel/challenges_recommendations_map.xlsx"

"""
DIRECTORIES
"""
# Directory where visualizations are stored as they are created for the output document
VIZ_DIRECTORY = "src/output/viz/images/"

# A path to the directory in which cover sheets are stored (relative to the location of the project's root)
COVER_SHEET_DIRECTORY = "../cover_sheet/cover_sheets/"

"""
COVER SHEET READING
"""
# Maps headers on cover sheet to columns in the data - i.e., when the cover sheet reader comes across the header in the key, the data is stored to a column with the value as the column name
HEADER_MAP = {
    "What is blocking you?": "Blockers",
    "Add your own tags": "Tags",
    "How can the White House help?": "White House help",
    "How can other agencies help?": "Other agencies help",
    "How can Congress help?": "Congress help",
    "How can industry help?": "Industry help",
    "How can the third sector (non-profits and non-governmental organizations) help?": "Third sector help",
    "How can academia help?": "Academia help"
}

"""
COLUMN NAME LISTS: List including the names of related columns in the central data source
"""
# List of challenges that can be reported in the cover sheet, correspond to column names in the data
CHALLENGES_LIST = ["Hiring technical staff in-house", "Inadequate technology", "Challenge 3", "Challenge 4", "Challenge 5", "Challenge 6"]

# List containing administration themes/priorities, which are also used as column names in the data
THEMES_LIST = ["Climate", "Equity", "Recovery"]

"""
GOAL STATUSES
"""
# A dictionary mapping each goal status to a numeric rank
STATUS_RANK_MAP = {
    "Ahead": 3,
    "On track": 2,
    "Nearly on track": 1,
    "Blocked": 0
}

"""
STYLING: Constants related to styling figures and output documents
"""
# Maps each goal status to a hex color
STATUS_COLOR_MAP = {
    "Ahead": "#156966",
    "On track": "#319C98",
    "Nearly on track": "#67B5CE",
    "Blocked": "#FA935B"
}

# The default font used in the output document
DEFAULT_FONT = "Roboto"

"""
AGENCY NAMES/ABBREVIATIONS
"""
# Maps agency full name to its abbreviation
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

# Maps agency abbreviation to its full name
AGENCY_ABBREVIATION_TO_NAME = {value: key for key, value in AGENCY_NAME_TO_ABBREVIATION.items()}

"""
MARKDOWN REGEX: Regular expressions used to interpret Markdown-formatted strings as bolded/italicized
"""
BOLD_REGEX = "\*\*(.*?)\*\*"
ITALICS_REGEX = "\*(.*?)\*"
BOLD_ITALICS_REGEX = ""

"""
NO-CODE DATAFRAMES: DataFrames sourced from the no-code spreadsheets that are used to populate text fields in the output document
"""
TEXT_BLOCK_TEMPLATES_DF = pd.read_excel(TEXT_BLOCK_TEMPLATES_PATH, skiprows=1)
CHALLENGES_RECOMMENDATIONS_MAP_DF = pd.read_excel(CHALLENGES_RECOMMENDATIONS_MAP_PATH)
