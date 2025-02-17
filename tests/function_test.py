"""
This test script demonstrates usage of the nba_injury_report_pdf_to_df package.

Recommended Setup:
    Before running this script, install the package locally in editable mode:
        pip install -e .

That way, you can import nba_injury_report_pdf_to_df directly in your tests.
"""
# %%
from utils import path 
from nba_injury_report_pdf_to_df import pdf_to_df

# Path to example injury report
pdf_path = path('injury_report_pdfs', 'Injury-Report_2025-01-10_05PM.pdf')

# Check dataframe manually to see that it has the same appearance as the pdf.
df = pdf_to_df(pdf_path)