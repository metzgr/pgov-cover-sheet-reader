"""
File to be run to generate summary reports for the most recent quarter
"""
import src.output.docx.generator as docx_generator
from src.objects.agency import Agency
import pandas as pd

from src.constants import DATABASE_PATH

if __name__ == "__main__":
    sba = Agency(pd.read_csv(DATABASE_PATH), "SBA", "Q4", 2020)
    docx_generator.create_summary_document(sba, "SBA_output")
