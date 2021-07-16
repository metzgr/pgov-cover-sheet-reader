"""
File to be run to generate summary reports for the most recent quarter
"""
import src.output.docx.output_creation as output_creation
from src.objects.agency import Agency
import pandas as pd

if __name__ == "__main__":
    sba = Agency(pd.read_csv("../dummy_cover_sheet_data.csv"), "SBA", "Q4", 2020)
    output_creation.create_summary_document(sba, "SBA_output")
