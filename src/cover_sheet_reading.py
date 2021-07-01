"""
Functions realted to scraping the data from an incoming cover sheet.
"""

import utility

from docx.text.paragraph import Paragraph

# Maps headers on cover sheet to columns in the data
HEADER_MAP = {
    "What is blocking you?": "blockers_description",
    "Add your own tags": "tags",
    "How can the White House help?": "help_white_house",
    "How can other agencies help?": "help_other_agencies",
    "How can Congress help?": "help_congress",
    "How can industry help?": "help_industry",
    "How can the third sector (non-profits and non-governmental organizations) help?": "help_third_sector",
    "How can academia help?": "help_academia"
}


def read_cover_sheet(document):
    """
    Returns a dictionary containing the data collected from the passed word document
    
    :param document: A Document object holding a performance cover sheet from a .docx file
    :return: A dictionary containing all of the relevant data scraped from the passed cover sheet document
    """
    data = {}
    header = None

    for block in utility.iter_block_items(document):
        if isinstance(block, Paragraph):
            if block.text in HEADER_MAP.keys():     # if the paragraph holds one of the headers used to indicate that text can be inputted from user
                header = block.text
        else:   # if block is Table object
            if header:  # if table comes directly after a header
                text_input = None
                for row in block.rows: 
                    for cell in row.cells:
                        for paragraph in cell.paragraphs: 
                            if text_input:  # allows for multiple paragraphs in input
                                text_input = "{} {}".format(text_input, paragraph.text)
                            else:
                                text_input = paragraph.text
                data[HEADER_MAP[header]] = text_input
                header = None
            else:
                for row in block.rows:
                    row_text = []
                    for cell in row.cells:
                        for paragraph in cell.paragraphs: 
                            row_text.append(paragraph.text)     # collects all paragraphs in a given cell into a list
    
    return data
