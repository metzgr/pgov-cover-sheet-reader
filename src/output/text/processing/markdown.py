"""
Functions related to rendering string inputs in Markdown formatting (specifically in bolding/italicizing) in alternative formats.
"""
from src.constants import BOLD_REGEX, ITALICS_REGEX

from docxtpl import RichText
import re
