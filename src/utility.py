"""
Holds functions that have use across multiple sections of the project.
"""

from src.constants import STATUS_RANK_MAP

from docx.document import Document as _Document
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from docx.table import _Cell, Table
from docx.text.paragraph import Paragraph

import xml.etree.ElementTree as ET

def iter_block_items(parent):
    """
    Returns a stream of Paragraph and Table objects in the order in which they appear in the passed docx document.

    :param parent: A Document object holding a docx file.
    :return: A stream of Paragraph and Table objects in the order in which they appear on the document passed as a parameter.
    """
    if isinstance(parent, _Document):
        parent_elm = parent.element.body
    elif isinstance(parent, _Cell):
        parent_elm = parent._tc
    else:
        raise ValueError("Parent object is of unknown type")

    for child in parent_elm.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)

def print_table(table):
    """
    Prints out each component of the passed Table object in the order in which it appears.

    :param table: A Table object representing a table that holds text.
    """
    for row in table.rows: 
        for cell in row.cells:
            for paragraph in cell.paragraphs: 
                print(paragraph.text)

def get_previous_quarter_and_year(quarter, year):
    """
    Given a string representing a quarter (e.g., 'Q1'), returns the previous quarter and year.

    :param quarter: A string representing a quarter (e.g., 'Q1').
    :param year: A integer representing a fiscal year.
    :return: Both the quarter and the year.
    """
    quarter_number = int(quarter.replace("Q", ""))

    if quarter_number > 1:
        return f"Q{quarter_number - 1}", year
    else:
        return "Q4", year - 1

def goal_is_progressing(current_status, previous_status):
    """
    Returns TRUE if the passed goal is progressing quarter-over-quarter, FALSE otherwise.

    :param current_status: The current status of the goal being assessed.
    :param previous_status: The previous quarter's status of the goal being assessed.
    :return: TRUE if the goal is progressing in its status, FALSE otherwise.
    """
    try:
        return STATUS_RANK_MAP[current_status] > STATUS_RANK_MAP[previous_status]
    except:
        raise Exception(f"{current_status}, {previous_status}")

def get_picture_names(tpl):
    """
    Returns a list of all of the names of the images held within the passed DocxTemplate object. Holds relevance for mapping which images in the template document are to be replaced by auto-generated figures.

    :param tpl: A DocxTemplate object.
    :return: A list of strings, each of which is a name of a unique picture within the DocxTemplate file.
    """
    picture_names = []

    for elem in ET.fromstring(tpl.docx.element.body.xml).iter():
        if elem.tag == "{http://schemas.openxmlformats.org/drawingml/2006/picture}cNvPr":
            picture_names.append(elem.attrib["name"])

    return picture_names

def richtext_is_empty(rt):
    """
    Returns a boolean indicating whether or not the passed RichText object is empty.

    :param rt: A RichText object.
    :return: TRUE if the RichText object is empty (i.e., does not have any text), FALSE otherwise.
    """
    return rt.xml == ""
