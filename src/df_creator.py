"""
Functions that return specialized DataFrame transformations to be used in analysis.
"""

import pandas as pd
import utility

def get_status_count_groupby_agency_year_quarter(df):
    """
    Given a DataFrame in the format of the raw goal status storage, returns a DataFrame that breaks down the amount of occurrences of each goal status for every agency, broken down by quarter. I.e., each row contains a unique combination of agency name, fiscal year and quarter, with the number of occurrences of a certain goal status in the given combination displayed in the "Count" column.

    :param df: A DataFrame that resembles either the raw data storage source or a slice of original source.
    :return: A DataFrame displaying the count of each goal status in every unique combination of agency name, fiscal year and quarter.
    """
    return df.groupby(["Agency Name", "Status", "Fiscal Year", "Quarter"]).size().reset_index().rename(columns={0: "Count"})

def get_recurring_challenges_count(df):
    """
    Returns a DataFrame representing the number of times each challenge has been consecutively reported to date for each APG. For instance, if a  challenge has been reported for an APG each of the last 4 quarters, it would have a count of 4. If a goal was not reported last quarter for an APG, but was reported each of the 3 quarters before that, it would have a count of 0.

    :param df: A DataFrame that resembles either the raw data storage source or a slice of original source.
    :return: A DataFrame with each row displaying a unique combination of an APG and a challenge and the number of times the challenge has been consecutively reported for the APG.
    """
    sorted_df = df.sort_values(["Fiscal Year", "Quarter"], ascending=False)     # sorting df such that the most recently reported quarter is in top row

    data = []

    for agency in df["Agency Name"].unique():
        agency_goals = df.loc[df["Agency Name"] == agency, "Goal Name"].unique()
        
        # loops for every combination of goal and challenges
        for goal in agency_goals:
            for challenge in utility.CHALLENGES_LIST:
                # gets the index of the last time the challenge wasn't reported, i.e., the number of consecutive quarters it was reported
                consecutive_reports = (sorted_df.loc[sorted_df["Goal Name"] == goal].reset_index(drop=True)[challenge] == "Off").idxmax() 
                data.append({
                    "Agency Name": agency, 
                    "Goal Name": goal,
                    "Challenge": challenge,
                    "Count": consecutive_reports
                })

    return pd.DataFrame(data=data)
