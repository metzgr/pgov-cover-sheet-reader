import output_creation
import agency
import pandas as pd

sba = agency.Agency(pd.read_csv("../dummy_cover_sheet_data.csv"), "SBA", "Q4", 2020)
output_creation.create_summary_document("../Summary_Report_Template.docx", sba)
