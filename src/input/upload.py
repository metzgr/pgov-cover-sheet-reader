"""
Functions related to updating the central database with the most recently read cover sheets.
"""

import pandas as pd

def update_database(database_path, new_data_df):
    """
    Updates the databased located at the passed path with the new data (read from cover sheets) passed as an argument appended as new rows.

    :param database_path: The path to the central data storage for the project. Only supports .csv files (could be expanded in the future).
    :param new_data_df: A DataFrame holding data to be added to the database, presumably read from cover sheets.
    """
    database = pd.read_csv(database_path)
    different_columns = new_data_df.columns.difference(database.columns).to_list()  # list of columns in the cover sheets but not in database

    # If there are columns in the new data that are not included in the database
    if len(different_columns) > 0:
        added_cols_str = "WARNING: The following three data fields were retrieved from the cover sheet that are not present in the database:\n"
        for column in different_columns:
            added_cols_str += f"\t\"{column}\"\n"

        print(added_cols_str)

    database = database.append(new_data_df)

    database.to_csv(database_path, index=False)
