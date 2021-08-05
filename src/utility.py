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
from datetime import date
import math

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

def get_trailing_blank_paragraphs(docx):
    """
    Returns a list of Paragraph objects representing the blank lines at the end of the passed Document object.

    :param docx: A docx Document object.
    :return: A list of Paragraph objects that are at the end of the the passed document. Returns an empty list if no blank lines were found at the end of the document.
    """
    reversed_block_items = list(iter_block_items(docx))  # converts generator to list
    reversed_block_items.reverse()  # reverses the order of the list of block items, i.e., placing the final blocks at the beginning of the list
    lines_to_remove = []

    # Checks if the last line of the template document is empty, adds to list of lines to remove if it is. This prevents extra blank lines at the end of the document, potentially creating a blank page when a page break is added.
    while len(reversed_block_items) != 0 and isinstance(reversed_block_items[0], Paragraph) and reversed_block_items[0].text == "":
        lines_to_remove.append(reversed_block_items.pop(0))

    return lines_to_remove

def get_current_fiscal_year():
    """
    Returns the current fiscal year. Note that the new fiscal year starts on October 1 of a calendar year: for instance, fiscal year 2021 started on October 1, 2020.

    :return: The current fiscal year.
    """
    fiscal_year = date.today().year
    
    if date.today().month < 10:
        fiscal_year = fiscal_year - 1

    return fiscal_year

def get_current_fiscal_quarter():
    """
    Returns the current fiscal month. Note that the first fiscal quarter begins on October 1 - the start of a new fiscal year.

    :return: The current fiscal quarter.
    """
    month = date.today().month

    if month >= 10:
        return 1
    else:
        return math.ceil(month / 3) + 1 
