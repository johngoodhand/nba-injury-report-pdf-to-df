# NBA Injury Report PDF to DataFrame Converter

This Python package provides a function, `pdf_to_df`, that converts NBA injury reports in PDF format into a pandas DataFrame for easy analysis and manipulation.

## Features

- PDF to DataFrame Conversion: Extracts data from NBA injury report PDFs and structures it into a pandas DataFrame.
- Data Cleaning: Handles multi-row entries and corrects common formatting issues in the reports.

## Installation

Install the package using pip:

```bash
pip install nba_injury_report
```

## Usage

Here's how you can use the pdf_to_df function:

```python
from nba_injury_report import pdf_to_df

# Path to your local NBA injury report PDF
pdf_path = "path/to/your/injury_report.pdf"

# Convert PDF to DataFrame
df = pdf_to_df(pdf_path)

# Display the DataFrame
print(df.head())
```