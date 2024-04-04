
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------ Data API Post Functions -----------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

# Functions included here are used to post the data to an api.

# This script is a far too simple proof of concept. It needs to dynamically 
# write the correct data elements to the correct table based on the data model.

# Developed by Brian Sullivan || bcsullivan@guidehouse.com

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# ------------------------- Set-up / Package Imports ---------------------------
# ------------------------------------------------------------------------------


# Standard Library Imports
import os

# Third Party Imports
from pyairtable import Api


# ------------------------------------------------------------------------------
# -------------------------- Function Definition -------------------------------
# ------------------------------------------------------------------------------


# Define function to post to airtable
def airTable_post(data):

    # https://pyairtable.readthedocs.io/en/stable/api.html

    payload = []
    errors = []
    # Checking if the data validation process found errors before writing
    for row in data:
        if len(data[row]['Errors']) == 0:
            # if no errors remove fields and add to payload
            data[row].pop('Errors')
            data[row].pop('Version')
            payload.append(data[row])
        else:
            # if errors add to errors
            errors.append(data[row])

    # this is for testing, delete in prod
    print(payload)

    # Create authenticated API instance
    api = Api(api_key=os.getenv("AIRTABLE_TOKEN"))

    # Define the table that we want to update
    table = api.table(
        base_id=os.getenv("AIRTABLE_BASE_ID"), table_name=os.getenv("AIRTABLE_TABLE")
    )

    # Commented out for testing, uncomment in prod
    # Batch update the table
    # table.batch_create(payload)

    print("--- Posted to AirTable ---")
    return


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------ End Script ------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
