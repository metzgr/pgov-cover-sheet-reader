"""
Includes functions that take key information and format it in a client-friendly string that can be used in summary reports.
"""

import agency
import utility

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
