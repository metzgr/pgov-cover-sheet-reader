"""
File to be run to generate summary reports for the most recent quarter
"""
import output_creation
import agency
import pandas as pd

# NOTE: The current implementation below is for development purposes. When this project is in production, the implementation below should create summary report documents for each CFO act agency with the most updated cover sheet data.
if __name__ == "__main__":
    sba = agency.Agency(pd.read_csv("../dummy_cover_sheet_data.csv"), "SBA", "Q4", 2020)    # created for debugging in development
    output_creation.create_summary_document(sba)
