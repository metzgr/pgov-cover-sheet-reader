"""
Module capable of rendering text sourced from template Excel files.
"""
import src.output.text.processing.markdown as markdown

from src.constants import TEXT_BLOCK_TEMPLATES_DF

def __fill_placeholders(text, placeholders_dict):
    """
    Fills placeholders in the passed string with the values mapped in the passed dictionary. Searches for placeholders in the passed string by searching for contents within {curly braces} and matching them with keys in the passed dictionary.

    :param text: A string in Markdown format (and potentially holding placeholder values).
    :param placeholders_dict: A dictionary mapping the placeholders in the passed string with the values they should be replaced with.
    :return: The string passed as an argument with all of its placeholders replaced with the values mapped in the passed dictionary.
    """
    to_return = text
    
    for placeholder, value in placeholders_dict.items():
        to_return = to_return.replace(f"{{{placeholder}}}", str(value))    # finds variable held within {curly brackets} for replacement
    
    return to_return
