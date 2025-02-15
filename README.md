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
from nba_injury_report_pdf_to_df import pdf_to_df

# Path to your local NBA injury report PDF
pdf_path = "path/to/your/injury_report.pdf"

# Convert PDF to DataFrame
df = pdf_to_df(pdf_path)

# Display the DataFrame
print(df.head())
```

## Important Note

This package is designed to process NBA injury reports that follow the format used in **January 2025**.  
The structure of these reports includes specific columns such as:
- Game Date
- Game Time
- Matchup
- Team
- Player Name
- Current Status
- Reason

If the NBA updates the report format in the future, this package may require modifications to ensure compatibility.

## Dependencies

- pandas
- pdfplumber

These dependencies are automatically installed with the package.

## Contributing

Contributions are welcome!  
If you encounter issues or have suggestions for improvements, please open an issue or submit a pull request on the GitHub repository:  
https://github.com/johngoodhand/nba_injury_report_pdf_to_df

## License

This project is licensed under the MIT License.

---

**Note:** This package is not affiliated with or endorsed by the National Basketball Association (NBA).
