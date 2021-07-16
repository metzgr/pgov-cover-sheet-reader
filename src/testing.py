"""
File to be run to generate summary reports for the most recent quarter
"""
import output_creation
import agency
import pandas as pd

if __name__ == "__main__":
    sba = agency.Agency(pd.read_csv("../dummy_cover_sheet_data.csv"), "SBA", "Q4", 2020)
    output_creation.create_summary_document(sba, "SBA_output")
