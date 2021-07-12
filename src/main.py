import output_creation
import agency
import pandas as pd

if __name__ == "__main__":
    sba = agency.Agency(pd.read_csv("../dummy_cover_sheet_data.csv"), "SBA", "Q4", 2020)    # created for debugging in development
    output_creation.create_summary_document("../Summary_Report_Template.docx", sba)
