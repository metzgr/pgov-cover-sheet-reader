"""
File to be run to generate summary reports for the most recent quarter
"""
import output_creation
from agency import Agency
import pandas as pd

from constants import AGENCY_ABBREVIATION_TO_NAME

if __name__ == "__main__":
    for agency_abbreviation in AGENCY_ABBREVIATION_TO_NAME.keys():
        file_name = f"{agency_abbreviation}_Summary"
        agency = Agency(pd.read_csv("../dummy_cover_sheet_data.csv"), agency_abbreviation, "Q4", 2020)
        output_creation.create_summary_document(agency, file_name)
        print(file_name, "created")
