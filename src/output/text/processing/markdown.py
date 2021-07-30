"""
Functions related to rendering string inputs in Markdown formatting (specifically in bolding/italicizing) in alternative formats.
"""
from src.constants import BOLD_REGEX, ITALICS_REGEX

from docxtpl import RichText
import re

def string_to_richtext(text):
    """
    Converts a passed string in Markdown format to a RichText object of equivalent formatting.

    :param text: A string in Markdown format.
    :return: A RichText object formatted in the manner indicated by the passed Markdown-formatted string.
    """
    rt = RichText()
    
    # Splits text into a list where each entry a string of characters of the same formatting. re.split() returns some empty strings/None values, which are filtered out of the list.
    split_text = list(filter(None, re.split(f"{BOLD_REGEX}|{ITALICS_REGEX}", text)))
    
    # Retrieving character spans that are intended to be bolded or italicized
    bold_items = __get_bold_items(text)
    italics_items = __get_italics_items(text)
    
    # Loops through each block of characters, applies appropriate formatting
    for text_snippet in split_text:
        bold = False
        italic = False
        
        if text_snippet in bold_items:
            bold = True
        if text_snippet in italics_items: 
            italic = True
            
        rt.add(text_snippet, bold=bold, italic=italic, font="Roboto")
    
    return rt

def __get_bold_items(text):
    """
    Returns a list of all the portions of the passed string that are desired to be bolded according to Markdown formatting standards (**between two sets of double asterisks**).

    :return: A list of items of the passed string to be bolded according to Markdown formatting standards.
    """
    return list(filter(None, re.findall(BOLD_REGEX, text)))

def __get_italics_items(text):
    """
    Returns a list of all the portions of the passed string that are desired to be italicized according to Markdown formatting standards (*between two sets of asterisks*).

    :return: A list of items of the passed string to be italicized according to Markdown formatting standards.
    """
    return list(filter(None, re.findall(ITALICS_REGEX, text)))
