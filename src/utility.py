"""
Holds functions that have use across multiple sections of the project.
"""

from docx.document import Document as _Document
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from docx.table import _Cell, Table
from docx.text.paragraph import Paragraph

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
