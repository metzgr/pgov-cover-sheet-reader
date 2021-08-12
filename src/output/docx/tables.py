"""
Stores all of the function that enable the dynamic filling of tables in the summary report document
"""

import src.utility as utility
import src.output.data.df_creator as df_creator
import src.output.text.templates as text_templates
from src.output.text.processing.excel import get_recommendations_for_challenge

from docxtpl import RichText

def get_goal_status_table(agency):
    """
    Returns a list with nested dictionaries (representing rows of the the table) to fill the goal status table in the template document.

    :param agency: An Agency object representing the agency for which the top recurring challenges will be retrieved.
    :return: A list of dictionaries used to render the goal status table.
    """
    table = []
    previous_quarter, previous_year = utility.get_previous_quarter_and_year(agency.get_quarter(), agency.get_year())
    quarters = [previous_quarter, agency.get_quarter()]
    years = [previous_year, agency.get_year()]

    for goal in agency.get_goals():
        row = [goal]    # first column is filled with the goal name

        # Loops first through the previous quarter/year, then the current quarter/year
        for quarter, year in zip(quarters, years):
            status = agency.get_goal_status(goal, quarter=quarter, year=year)

            row.append(status)  # appends goal status as a new column

        table.append({"cols": row})     # appends row to the table object

    return table

def get_challenge_count_table(agency):
    """
    Returns a list of dictionaries (representing rows of the the table) to fill the challenge count table in the template document.

    :param agency: An Agency object representing the agency for which the top recurring challenges will be retrieved.
    :return: A list of dictionaries used to render the challenge count table.
    """
    table = []

    challenge_count_df = df_creator.get_challenge_count_by_quarter(agency.get_agency_df())
    challenge_count_df = challenge_count_df.loc[(challenge_count_df["Quarter"] == agency.get_quarter()) & (challenge_count_df["Fiscal Year"] == agency.get_year())].sort_values(by="Count", ascending=False)

    for challenge in challenge_count_df["Challenge"].unique():
        count = challenge_count_df.loc[challenge_count_df["Challenge"] == challenge, "Count"].values[0]
        
        table.append({
            "col": {
                "name": challenge,
                "count": count
            }
        })

    return table

def get_recs_table(agency, goal_name, tpl):
    """
    Returns a list of dictionaries (representing rows of the table) to fill the recommendations table in the APG breakdown template.

    :param agency: An Agency object representing the agency for which challenge mitigation recommendations will be made.
    :param goal_name: The goal from which suggestions will be made based on their challenges.
    :return: A list of dictionaries used to render the recommendations table.
    """
    table = []

    # Adds row based on every challenge the agency is facing in the current quarter
    for challenge in agency.get_challenges(goal_name):
        recs_df = get_recommendations_for_challenge(challenge)

        rt = RichText()

        for index, row in recs_df.iterrows():   # NOTE: this is not implemented in the text template spreadsheet because the hyperlink needs to be added to the recommendations
            rec = row["Recommended Action"]
            explanation = row['Explanation']
            url = tpl.build_url_id(row["URL"])

            rt.add(text_templates.get_rec_text_block(rec, explanation, url))
            
            if index != len(recs_df) - 1:   # add line breaks between all recommendations except for the last
                rt.add("\n\n")
        
        table_row = {
            "challenge": challenge,
            "recs": rt
        }

        table.append(table_row)

    return table

def get_common_challenges_theme_table(agency, apg, challenge):
    """
    Returns a list of dictionaries to populate a table showing agencies working on a common challenge across related themes for the passed agency.

    :param agency: An Agency object representing the agency for which APG teams with common themes and challenges will be shown.
    :param apg: The agency's APG for which for which common APG teams will be rendered.
    :return: A list of dictionaries used to render the common challenges/themes table.
    """
    table = []

    for theme in agency.get_themes(apg):
        common_teams_df = agency.get_common_apgs_theme_challenge(theme, challenge)
        common_teams_df = common_teams_df.loc[:, ["Agency Name", "Goal Name"]].rename(columns={"Agency Name": "agency", "Goal Name": "apg"})    # rename columns in prepartion for insertion in table
        common_teams_dicts = common_teams_df.to_dict("records")     # converts DataFrame to list of dictionaries for instertion into table

        table.append({
            "theme": theme,
            "common_teams": common_teams_dicts
        })

    return table
