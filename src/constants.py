"""
A dictionary mapping each goal status to a rank
"""
STATUS_RANK_MAP = {
    "Ahead": 4,
    "On track": 3,
    "Nearly on track": 2,
    "Blocked": 1
}

CHALLENGES_LIST = ["Hiring", "Competing deadlines", "Legislation", "Lack of research", "Unclear guidance", "Unavailable data"]

SUMMARY_TEMPLATE_PATH = "src/resources/templates/Summary_Report_Template.docx"
APG_BREAKDOWN_TEMPLATE_PATH = "src/resources/templates/APG_Summary_Template.docx"
