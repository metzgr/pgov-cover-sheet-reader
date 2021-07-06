"""
Maps keywords imbedded in template document (keys) to what they will be replaced with in the rendered output document (values). Note that each keyword is identified as "{{keyword_name}}" within the template document.
"""

import utility
import agency
import text_templates

from docx.text.paragraph import Paragraph
from docxtpl import DocxTemplate

# Maps keywords within the template document to the values that they will be replaced by.
REPLACEMENT_MAP = {
    "example string adjective": "incredibly",
    "blocking text": "These are some blockers that were custom-placed into the document. Nice job!"
}

def replace_placeholder_images(tpl):
    """
    Replaces all of the placeholder images of the passed DocxTemplate object with relevant figures.

    :param tpl: A DocxTemplate containing placeholder images.
    """
    placeholder_figure_map = {
        "Picture 6": "viz/goal_status_q4_2020.png",
        "Picture 7": "viz/goal_status_q3_2020.png",
    }

    for key, value in placeholder_figure_map.items():
        tpl.replace_pic(key, value)

def create_summary_document(template_path, agency):
    """
    Creates a summary document for the passed agency, year and quarter.

    :param template_path: The path to the template docx file from which a copy will be made containing relevant data.
    """
    tpl = DocxTemplate(template_path)

    replace_placeholder_images(tpl)

    replacement_map = {
        "previous_quarter_and_year": "{} {}".format(*utility.get_previous_quarter_and_year(agency.get_quarter(), agency.get_year())),
        "current_quarter_and_year": f"{agency.get_quarter()} {agency.get_year()}",
        "agency_name": agency.get_name(),
        "agency_abbreviation": "SBA",   # NOTE: this is temporarily hard-coded, should be changed to `agency.get_abbreviation()` once the agency name mapping is implemented
        "goal_change_summary_sentence": text_templates.get_goal_change_summary_sentence(agency)
    }

    tpl.render(replacement_map)
    tpl.save("output.docx")
