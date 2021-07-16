"""
Functions that return specialized DataFrame transformations to be used in analysis.
"""

from src.constants import CHALLENGES_LIST

import pandas as pd

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
            for challenge in CHALLENGES_LIST:
                # gets the index of the last time the challenge wasn't reported, i.e., the number of consecutive quarters it was reported
                consecutive_reports = (sorted_df.loc[sorted_df["Goal Name"] == goal].reset_index(drop=True)[challenge] == "Off").idxmax() 
                data.append({
                    "Agency Name": agency, 
                    "Goal Name": goal,
                    "Challenge": challenge,
                    "Count": consecutive_reports
                })

    return pd.DataFrame(data=data)

def get_challenge_count_by_quarter(df):
    """
    Returns a DataFrame with the challenge count by quarter for each agency within the passed DataFrame.

    :param df: A DataFrame that resembles either the raw data storage source or a slice of original source.
    :return: A DataFrame that displays the number of occurrences of a given challenge across each agency in a given quarter and fiscal year.
    """
    challenge_count_df = None

    for challenge in CHALLENGES_LIST:
        data_df = df.astype({challenge:"category"})   # without changing the type of the column, the groupby automatically drops all fields with a count of 0

        data_df = data_df.groupby(["Agency Name", "Fiscal Year", "Quarter", challenge]).size().reset_index().rename(columns={0: "Count"})

        # Error handling: groupby will not create any rows of "Yes" values if the agency never identified the given challenge. Checking to see if data_df only contains unchecked challenges
        if len(data_df.loc[(data_df[challenge] == "Yes")]) == 0 and len(data_df.loc[(data_df[challenge] == "Off")]) == len(data_df):
            # Converts the count of the unchecked challenges to its inverse: a count of all the times the challenge was checked.
            data_df[challenge] = "Yes"
            data_df["Count"] = 0
        else:
            data_df = data_df.loc[(data_df[challenge] == "Yes")]
        
        # Change column with challenge name to general "Challenge" column, filled with the unique challenge name
        data_df[challenge] = challenge
        data_df = data_df.rename(columns={challenge: "Challenge"})
        
        if isinstance(challenge_count_df, pd.core.frame.DataFrame):
            challenge_count_df = challenge_count_df.append(data_df)
        else:
            challenge_count_df = pd.DataFrame(data=data_df)     # initializes the DataFrame if it does not exist yet

    return challenge_count_df.sort_values(["Agency Name", "Fiscal Year", "Quarter"]).reset_index(drop=True)
