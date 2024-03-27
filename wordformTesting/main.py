
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------ Word Form Data Extraction ---------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

# This script scrapes data from word forms into a json file and optionally posts
# to an airtable.

# Note: This program was left in development status, it is not production-ready

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
import sys
import json

# Third Party Imports
#import pandas as pd

# Local Imports
from src.globals import DIRECTORY
from src.functions.data_extraction import *
from src.functions.write_data import airTable_post


# ------------------------------------------------------------------------------
# -------------------------- Function Definition -------------------------------
# ------------------------------------------------------------------------------


# Define the main function
def main():
    
    # Extract and validate data from all word files in directory
    data = get_data(DIRECTORY)
    
    # Write the data to output.json file -- for testing/debugging
    with open("src/output/output.json", "w") as output:
        json.dump(data, output)
    
    # Print success message
    print("--- JSON output file created. ---\n")

    # This doesn't work as cleanly with the newer, nested dictionary output
    # A more robust function will be needed to produce csv output
    """ 
    # Write the data to a csv
    pd.DataFrame.from_dict(data, orient="index")\
                .reset_index()\
                .rename(columns={"index": "file_name"})\
                .to_csv("src/output/output.csv", index=False)    
    # Print success message
    print('--- CSV output file created. ---\n') 
    """
    
    # Post the results to airtable if command line arg exists
    if len(sys.argv) > 1 and sys.argv[1] == "-p":
        airTable_post(data)
    else:
        # Print usage message
        print("--- Usage: python main.py [-p] to post to to AirTable. ---")
    return


# ------------------------------------------------------------------------------
# ----------------------------- Function Call ----------------------------------
# ------------------------------------------------------------------------------


# Run the main function
if __name__ == "__main__":
    main()


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ----------------------------- End Script -------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
