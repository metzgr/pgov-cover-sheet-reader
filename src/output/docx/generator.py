"""
All of the functions related to generating an output document using the template documents. Maps keywords imbedded in template document (keys) to what they will be replaced with in the rendered output document (values). Note that each keyword is identified as "{{keyword_name}}" within the template document.
"""

import src.utility as utility
import src.output.text.templates as text_templates
import src.output.dataframe.transformations as df_transformations
import src.output.viz.viz as viz
import src.output.docx.tables as tables
from src.constants import VIZ_DIRECTORY, SUMMARY_TEMPLATE_PATH, APG_BREAKDOWN_TEMPLATE_PATH, OUTPUT_DIR

import os
from docx.shared import Inches
from docx.enum.text import WD_BREAK
from docxtpl import DocxTemplate, InlineImage

def replace_placeholder_images(tpl, placeholder_map):
    """
    Replaces all of the placeholder images of the passed DocxTemplate object with relevant figures.

    :param tpl: A DocxTemplate containing placeholder images.
    :param placeholder_map: A dictionary object mapping the name of the file that should be replaced in the DocxTemplate file (key) to the location of the locally stored image that should replace it (value).
    """
    for key, value in placeholder_map.items():
        tpl.replace_pic(key, value)
        os.remove(value)    # remove file from local storage after it has been placed in report

def get_summary_page_image_replacement_map():
    """
    Returns a dictionary object mapping the picture within the working DocxTemplate map to the image in local storage that should replace it.
    
    :return: A dictionary object mapping the name of the file that should be replaced in the DocxTemplate file's summary page (key) to the location of the locally stored image that should replace it (value).
    """
    return {
        "Picture 2": f"{VIZ_DIRECTORY}small_multiples_previous.png",
        "Picture 3": f"{VIZ_DIRECTORY}small_multiples_current.png",
        "Picture 5": f"{VIZ_DIRECTORY}challenges_area_chart.png"
    }

def create_visuals(agency):
    """
    Dynamically creates all of the visualizations needed for the summary report.

    :param agency: An Agency object representing the agency that a summary report will be created for.
    """
    viz.create_goal_summary_small_multiples(agency)
    viz.create_challenges_reported_in_quarter(agency)
    viz.create_challenges_area_chart(agency)
    goals = agency.get_goals()
    for i in range(len(goals)):
        goal = goals[i]
        viz.create_goal_status_over_time(agency, goal, name=f"goal_status_over_time_{i}")

def create_summary_document(agency, output_filename, output_dir=OUTPUT_DIR):
    """
    Creates a summary document for the passed agency, year and quarter.

    :param agency: An Agency object representing the agency that a summary report will be created for.
    :param output_filename: The filename to which the output file will be save. Excluding file extension (.docx).
    :param output_dir: The directory to which the output file will be saved to.
    """
    tpl = DocxTemplate(SUMMARY_TEMPLATE_PATH)

    create_visuals(agency)
    replace_placeholder_images(tpl, get_summary_page_image_replacement_map())

    recurring_challenges_df = get_top_recurring_challenges(agency)

    recur_challenge_1_dict = {
        "challenge": recurring_challenges_df.iloc[0]["Challenge"],
        "goal": recurring_challenges_df.iloc[0]["Goal Name"],
        "count": recurring_challenges_df.iloc[0]["Count"]
    }

    recur_challenge_2_dict = {
        "challenge": recurring_challenges_df.iloc[1]["Challenge"],
        "goal": recurring_challenges_df.iloc[1]["Goal Name"],
        "count": recurring_challenges_df.iloc[1]["Count"]
    }

    replacement_map = {
        "previous_quarter_and_year": "{} {}".format(*utility.get_previous_quarter_and_year(agency.get_quarter(), agency.get_year())),
        "current_quarter_and_year": f"{agency.get_quarter()} {agency.get_year()}",
        "agency_name": agency.get_name(),
        "agency_abbreviation": agency.get_abbreviation(),
        "goal_change_summary_sentence": text_templates.get_goal_change_summary_sentence(agency),
        "goal_status_breakdown_bullets": text_templates.get_goal_status_breakdown_bullets(agency),
        "recurring_challenge_1_text": text_templates.get_recurring_challenges_text(recur_challenge_1_dict["challenge"], recur_challenge_1_dict["goal"], recur_challenge_1_dict["count"]),
        "recurring_challenge_2_text": text_templates.get_recurring_challenges_text(recur_challenge_2_dict["challenge"], recur_challenge_2_dict["goal"], recur_challenge_2_dict["count"]),
        "recur_challenge_1_count": recur_challenge_1_dict["count"],
        "recur_challenge_2_count": recur_challenge_2_dict["count"],
        "goal_status_table": tables.get_goal_status_table(agency),
        "challenge_count_table": tables.get_challenge_count_table(agency)
    }

    tpl.render(replacement_map)

    remove_trailing_paragraphs(tpl.docx)    # if there are trailing blank paragraphs at the end of the document, a blank page may be created when the page break is added on the line below
    tpl.docx.add_page_break()   # add page break prior to APG breakdown pages

    apgs_list = agency.get_goals()

    # Loops for every APG that the agency holds
    for i in range(len(apgs_list)):
        apg_template = DocxTemplate(APG_BREAKDOWN_TEMPLATE_PATH)  # renders/re-renders APG summary template
        apg = agency.get_goals()[i]
        apg_df = agency.get_agency_df()
        apg_df = apg_df.loc[apg_df["Goal Name"] == apg]

        # Fills all of the placeholder keywords with APG-specific text
        context = {
            "apg_name": apg,
            "speedometer_text": text_templates.get_speedometer_summary_text(agency, apg),
            "blockers_text": text_templates.get_blockers_text(agency, apg),
            "group_assistance_text": text_templates.get_group_help_text(agency, apg),
            "success_story": text_templates.get_success_story(agency, apg),
            "recs_table": tables.get_recs_table(agency, apg, tpl),
            "theme_challenges_tables": [
                {"challenge": challenge, "table": tables.get_common_challenges_theme_table(agency, apg, challenge)} for challenge in agency.get_challenges(apg)     # creates a dictionary for each challenge that the APG reported this quarter
            ],
            "cap_goals_list": text_templates.get_cap_goals_list(agency, apg),
            "outcomes_list": text_templates.get_outcomes_list(agency, apg)
        }

        # Fill placeholders of image tags
        image_tags = ["speedometer_image", "goal_status_over_time"]
        for tag in image_tags:
            context[tag] = f"{{{{{tag}_{i}}}}}"    

        apg_template.render(context)    # renders the keyword replacements specific to the APG

        # Loops through every element in the APG summary, adds it to the whole agency summary report
        for element in apg_template.element.body:
            tpl.docx.element.body.append(element)

        goal_status = apg_df.loc[(apg_df["Quarter"] == agency.get_quarter()) & (apg_df["Fiscal Year"] == agency.get_year())]["Status"].values[0]    # retrieve goal status for the current fiscal year and quarter
        formatted_goal_status = goal_status.lower().replace(" ", "_")   # format goal status to the naming conventions of the speedometer images

        tpl.render({
            f"speedometer_image_{i}": InlineImage(tpl, image_descriptor=f"src/resources/speedometers/speedometer_{formatted_goal_status}.png", width=Inches(3)),   # width of 3 inches seems to be sweet spot for 2-column table
            f"goal_status_over_time_{i}": InlineImage(tpl, image_descriptor=f"{VIZ_DIRECTORY}goal_status_over_time_{i}.png", width=Inches(3))
        })

        # Adds page break after every APG breakdown except for on final page
        if i != len(apgs_list) - 1:
            run = list(utility.iter_block_items(tpl.docx))[-1].add_run()
            run.add_break(WD_BREAK.PAGE)

    # Creates output directories if they do not already exist
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)  

    try:
        tpl.save(f"{output_dir}{output_filename}.docx")
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
    df = df_transformations.get_recurring_challenges_count(agency.get_agency_df())
    df = df.sort_values("Count", ascending=False)

    return df.reset_index(drop=True).head(num_challenges)

def remove_trailing_paragraphs(docx):
    """
    Removes all of the blank paragraphs at the end of the passed Document object.

    :param docx: A docx Document object.
    """
    # Removes a blank line added after the final table in the template when render() is called, which resulted in a blank page being rendered. Sourced from https://github.com/python-openxml/python-docx/issues/33#issuecomment-77661907
    for p in utility.get_trailing_blank_paragraphs(docx):
        p = p._element
        p.getparent().remove(p)     # removes line
        p._p = p._element = None
