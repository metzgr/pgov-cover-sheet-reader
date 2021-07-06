"""
Maps keywords imbedded in template document (keys) to what they will be replaced with in the rendered output document (values). Note that each keyword is identified as "{{keyword_name}}" within the template document.
"""

import utility

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

    }

    for key, value in placeholder_figure_map.items():
        tpl.replace_pic(key, value)

def create_summary_document(template_path, df=None, agency=None, year=None, quarter=None):
    """
    Creates a summary document for the passed agency, year and quarter.

    :param template_path: The path to the template docx file from which a copy will be made containing relevant data.
    """
    tpl = DocxTemplate(template_path)

    replace_placeholder_images(tpl)

    replacement_map = {
        "previous_quarter_and_year": "{} {}".format(*utility.get_previous_quarter_and_year("Q1", 2020)),
        "current_quarter_and_year": f"{quarter} {year}",
        "agency_name": agency
    }

    tpl.render(replacement_map)
    tpl.save("output.docx")
