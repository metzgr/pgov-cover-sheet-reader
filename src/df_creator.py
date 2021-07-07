"""
Functions that return specialized DataFrame transformations to be used in analysis.
"""

import pandas as pd

def get_status_count_groupby_agency_year_quarter(df):
    """
    Given a DataFrame in the format of the raw goal status storage, returns a DataFrame that breaks down the amount of occurrences of each goal status for every agency, broken down by quarter. I.e., each row contains a unique combination of agency name, fiscal year and quarter, with the number of occurrences of a certain goal status in the given combination displayed in the "Count" column.

    :param df: A DataFrame that resembles either the raw data storage source or a slice of original source.
    :return: A DataFrame displaying the count of each goal status in every unique combination of agency name, fiscal year and quarter.
    """
    return df.groupby(["Agency Name", "Status", "Fiscal Year", "Quarter"]).size().reset_index().rename(columns={0: "Count"})
