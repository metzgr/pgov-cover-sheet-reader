"""
Maps keywords imbedded in template document (keys) to what they will be replaced with in the rendered output document (values). Note that each keyword is identified as "{{keyword_name}}" within the template document.
"""

import utility
import agency
import text_templates
import df_creator
import viz

from docx.text.paragraph import Paragraph
from docxtpl import DocxTemplate
import pandas as pd

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
        "Picture 2": "viz/small_multiples_previous.png",
        "Picture 3": "viz/small_multiples_current.png",
        "Picture 4": "viz/challenges_reported_bar_chart.png",
        "Picture 5": "viz/challenges_area_chart.png"
    }

    for key, value in placeholder_figure_map.items():
        tpl.replace_pic(key, value)

def create_visuals(agency):
    """
    Dynamically creates all of the visualizations needed for the summary report.

    :param agency: An Agency object representing the agency that a summary report will be created for.
    """
    viz.create_goal_summary_small_multiples(agency)
    viz.create_challenges_reported_in_quarter(agency)
    viz.create_challenges_area_chart(agency)

def create_summary_document(template_path, agency, output_dir="../"):
    """
    Creates a summary document for the passed agency, year and quarter.

    :param template_path: The path to the template docx file from which a copy will be made containing relevant data.
    :param agency: An Agency object representing the agency that a summary report will be created for.
    :param output_dir: The directory to which the output file will be saved to.
    """
    tpl = DocxTemplate(template_path)

    create_visuals(agency)
    replace_placeholder_images(tpl)

    recurring_challenges_df = get_top_recurring_challenges(agency)

    replacement_map = {
        "previous_quarter_and_year": "{} {}".format(*utility.get_previous_quarter_and_year(agency.get_quarter(), agency.get_year())),
        "current_quarter_and_year": f"{agency.get_quarter()} {agency.get_year()}",
        "agency_name": agency.get_name(),
        "agency_abbreviation": "SBA",   # NOTE: this is temporarily hard-coded, should be changed to `agency.get_abbreviation()` once the agency name mapping is implemented
        "goal_change_summary_sentence": text_templates.get_goal_change_summary_sentence(agency),
        "goal_status_breakdown_bullets": text_templates.get_goal_status_breakdown_bullets(agency),
        "recur_challenge_1": recurring_challenges_df.iloc[0]["Challenge"].lower(),
        "recur_challenge_2": recurring_challenges_df.iloc[1]["Challenge"].lower(),
        "recur_challenge_1_count": recurring_challenges_df.iloc[0]["Count"],
        "recur_challenge_2_count": recurring_challenges_df.iloc[1]["Count"],
        "recur_challenge_1_goal": recurring_challenges_df.iloc[0]["Goal Name"],
        "recur_challenge_2_goal": recurring_challenges_df.iloc[1]["Goal Name"],
        "challenge_summary_text": text_templates.get_challenge_summary_text(agency)
    }

    tpl.render(replacement_map)

    try:
        tpl.save(f"{output_dir}output.docx")
    except ValueError as e:
        if all(keyword in str(e) for keyword in ["Picture", "not found in the docx template"]):    # checking to see if error message contains two keywords indicating picture not found in the docx template
            raise ValueError(f"{e}. Pictures present in the document are as follows: {', '.join(utility.get_picture_names(tpl))}")
        else:
            raise ValueError(e)     # raise raw ValueError

def get_top_recurring_challenges(agency, num_challenges=2):
    """
    Returns a DataFrame with the most frequent recurring challenges for the passed agency.

    :param agency: An Agency object representing the agency for which the top recurring challenges will be retrieved.
    :param num_challenges: The number of top recurring challenges that should be returned. 2 by default.
    :return: A DataFrame with the most frequent recurring challenges for the passed agency.
    """
    df = df_creator.get_recurring_challenges_count(agency.get_agency_df())
    df = df.sort_values("Count", ascending=False)

    return df.reset_index(drop=True).head(num_challenges)
