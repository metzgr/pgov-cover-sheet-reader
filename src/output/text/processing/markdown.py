"""
Functions related to rendering string inputs in Markdown formatting (specifically in bolding/italicizing) in alternative formats.
"""
from src.constants import BOLD_REGEX, ITALICS_REGEX

from docxtpl import RichText
import re

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
