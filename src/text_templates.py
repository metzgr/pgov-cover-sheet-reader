"""
Includes functions that take key information and format it in a client-friendly string that can be used in summary reports.
"""

import agency
import utility

from docxtpl import RichText

def get_goal_change_summary_sentence(agency):
    """
    Given a passed agency, returns a sentence summarizing the change in total goal status across the agency from quarter to quarter.

    :param agency: An Agency object representing a CFO Act agency at a given point in time.
    :return: A string summarizing the quarter-over-quarter goal status change of the passed agency in the format "{number of occurrences} goals {goal status} last quarter to {number of occurrences} goals {goal status} this quarter."
    """
    previous_quarter, previous_year = utility.get_previous_quarter_and_year(agency.get_quarter(), agency.get_year())

    current_goal_statuses = agency.get_goal_status_df()["Status"]
    previous_goal_statuses = agency.get_goal_status_df(quarter=previous_quarter, year=previous_year)["Status"]
    
    to_return = ""
    
    # loops through each the previous and current goal status lists, accompanying string based on which list is being used
    for status_list, last_or_this_quarter in zip([previous_goal_statuses, current_goal_statuses], ["last quarter", "this quarter"]):
        status_strs = []    # list to hold each string uniquely describing goal status
    
        for status in status_list.unique():
            num_status = (status_list == status).sum()  # number of occurrences of given status
            status_strs.append(f"{num_status} goals {status.lower()}")

        to_return += f"{' and '.join(status_strs)} {last_or_this_quarter} quarter"  # joins each string together with "and" keyword
        to_return += ' to ' if last_or_this_quarter == 'last quarter' else ''   # adds a connecting word if in the first loop
        
    return to_return

def get_goal_status_breakdown_bullets(agency):
    """
    Returns a RichText object representing the change in each goal status quarter-over-quarter, which is capable of being represented as a bulleted list. NOTE: The returned RichText object itself does not return a bulleted list, but each paragraph renders as a bullet when placed in a bulleted list in a template document.

    :param agency: An Agency object representing a CFO Act agency at a given point in time.
    :return: A RichText object describing the change in each agency goal quarter-over-quarter that is capable of being represented as a bulleted list.
    """
    rt = RichText()

    goals_list = agency.get_goals()

    # each loop creates a new paragraph for a unique agency goal
    for i in range(len(goals_list)):
        goal_name = goals_list[i]

        current_goal_status = agency.get_goal_status(goal_name)
        previous_goal_status = agency.get_goal_status(goal_name, quarter="previous")

        rt.add(str(goal_name), bold=True)   # bolds the goal name at the beginning of the line
        rt.add(f"'s team identified the status of the goal as {current_goal_status.lower()} this quarter, ")

        # the next section of the line is conditional based on whether the goal status has stayed the same, progressed or regressed
        if current_goal_status == previous_goal_status:
            rt.add(f"remaining at the same status as its report of {current_goal_status.lower()} last quarter.")
        elif utility.goal_is_progressing(current_goal_status, previous_goal_status):
            rt.add(f"progressing from a status of {previous_goal_status.lower()} last quarter.")
        else:   # goal is regressing
            rt.add(f"dropping from a status of {previous_goal_status.lower()} reported last quarter.")
        
        if i != len(goals_list) - 1:
            rt.add("\a")    # adds a paragraph break following each goal status statement (except for the final one)

    return rt
