"""
Module capable of rendering text sourced from template Excel files.
"""
import src.output.text.processing.markdown as markdown

from src.constants import TEXT_BLOCK_TEMPLATES_DF, CHALLENGES_RECOMMENDATIONS_MAP_DF

def get_richtext_from_variable(variable_name, placeholders_dict, tone="neutral"):
    """
    Given a variable name, a dictionary of values to be replaced in the template, and a tone, returns a RichText object holding the text from the template document.

    :param variable_name: The variable name in the template document that will be rendered with the returned RichText object.
    :param placeholders_dict: A dictionary mapping the placeholders in the desired text template with the values they should be replaced with.
    :param tone: The tone that the RichText object should be delivered in. Acceptable inputs are: "neutral", "progressing", "regressing" or "plural". "neutral" by default.
    :return: A RichText object of the text template indicated by the arguments of the function.
    """
    text_block_row = TEXT_BLOCK_TEMPLATES_DF.loc[TEXT_BLOCK_TEMPLATES_DF["Variable Name"] == variable_name] 
    col_name = f"Sentence Template {tone.capitalize()}"

    # Retrieve text block from template, fill placeholders based on passed dictionary
    text = text_block_row[col_name].values[0]
    text = __fill_placeholders(text, placeholders_dict)

    return markdown.string_to_richtext(text)

def get_recommendations_for_challenge(challenge_name):
    """
    Returns a list of dictionaries including the challenge name, recommendation, URL and explanation for all of the recommendations for the passed challenge.

    :param challenge_name: The name of the challenge from which challenges will be retrieved.
    :return: A list of dictionaries, which hold the following keys:
        - Challenge Name: The name of the challenge that is connected to the recommendation.
        - Recommended Action: The recommendation based on the challenge identified.
        - URL: A URL linking to a page that provides more information on the recommended action.
        - Explanation: An explanation of why the recommended action was recommended for the challenge.
    """
    recommendations_df = CHALLENGES_RECOMMENDATIONS_MAP_DF.loc[CHALLENGES_RECOMMENDATIONS_MAP_DF["Challenge Name"] == challenge_name]
    return recommendations_df.to_dict("records")

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
