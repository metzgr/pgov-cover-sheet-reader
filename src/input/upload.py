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

        # Console prompt asking user whether or not they want to add new columns to database
        added_cols_str += "Would you like to add all of these columns to the database? Enter Y/N: "
        
        create_new_columns = handle_yes_no_input(added_cols_str)

        if create_new_columns:
            database = database.append(new_data_df)     # appends new data with new columns, which are set at values of NaN for all previous entries
        else:
            common_cols = (new_data_df.columns & database.columns).tolist()
            common_slice = new_data_df.loc[:, common_cols]  # only selects columns from new data DataFrame that are in database, no new columns added
            
            database = database.append(common_slice)
    else:   # if all columns in new data are in database
        database = database.append(new_data_df)

    database.to_csv(database_path, index=False)

def handle_yes_no_input(prompt):
    """
    Error checks yes/no input, returns true or false depending on the input of the user.

    :param prompt: The prompt used to retrieve a Y/N answer from the user.
    :return: TRUE if the user enters "Y", FALSE if the user enters "N".
    """
    user_input = input(prompt).upper()

    # Handling bad input
    while user_input not in ["Y", "N"]:
        user_input = input(f"\"{user_input}\" is not a valid input. Please enter \"Y\" or \"N\": ")

    return user_input == "Y"
