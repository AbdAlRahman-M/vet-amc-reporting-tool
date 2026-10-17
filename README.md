# Veterinary Antimicrobial Use Reporting Tool

An automated Python data pipeline that processes veterinary consumption records to generate descriptive statistical **HTML report files** tracking antimicrobial usage across different veterinary units. The project also includes a tool built using Microsoft Excel to standardize data entry and collection.

## ⚙️ How It Works

1. **Data Entry:** A custom built Microsoft Excel file provides VBA data entry forms with validation rules to minimize errors and the need to clean data.
2. **Data Extraction & Transformation:** [Pandas](https://pandas.pydata.org/) extracts raw consumption records from source files and transforms the data.
3. **Analytics & Aggregation:** The script calculates descriptive statistics (e.g., usage volume, drug classification frequencies) and prepares metrics.
4. **Report Generation:** The pipeline dynamically compiles the aggregated data into standalone HTML reports, generating one tailored file per individual veterinary health unit.

## 🚀 Tech Stack

- **Languages:** Python 3.14.7, VBA 7.1
- **Data Processing:** [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
- **Visualization/Output:** HTML5, CSS3, [Jinja](https://pypi.org/project/Jinja2/)

## 📁 Repository Structure

```text
./
├── data/
│   ├── consumption-files/      # Raw source files (Excel)
│   └── dimensions/             # Descriptive attributes for antimicrobial substances
│       └── substances.xlsx
├── data-entry-tool/            # Provides userforms for data entry with validation rules.
│   └── vet-consumption.xlsm
├── output/                     # Generated per-unit HTML report files
├── src/
│   ├── transform.py            # Pandas data cleaning and transformation
│   └── generate_report.py      # Statistical aggregation and HTML compilation
├── template/                   # HTML/CSS template for the reports
│   ├── styles.css
│   └── template.html
├── main.py                     # Pipeline orchestrator script
├── README.md
└── requirements.txt            # Project dependencies
```

## 🛠️ Prerequisites & Setup

### To Use the Data Entry Tool:
1. Make sure you have MS Excel installed (MS Excel 2010 or a later version).
2. Give permision to the file to run macros.
3. Open the file, click the 'Consumption' tab, then the 'Set Vet. Unit ID' button, and enter the veterinary health unit code.
4. Use the 'Add', 'Edit', 'Delete', and 'View' buttons to manage records.

### To Generate Reports:
#### 1. Clone the Repository

bash

```bash
git clone https://github.com/AbdAlRahman-M/vet-amc-reporting-tool.git
cd vet-amc-reporting-tool
```

#### 2. Set Up a Virtual Environment

```bash
python -m venv .venv
source .venv/Scripts/activate  # On Windows use: .venv\Scripts\activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Prepare Source Data

- Place your raw data Excel sheets (.xlsx) inside the `data/consumption-files/` directory.
- [Download] the veterinary units Excel file (requires access), and place it inside the `data/dimensions/` directory.

#### 5. Run the Pipeline

Execute the main script to process the data and build the reports:

```bash
python main.py
```

Once complete, open the `output/[timestamp of execution]/`, directory to view the generated individual HTML reports. The execution timestamp is the exact date and time when the script was executed.

## 📝 Future Enhancements

- Integrate interactive charting libraries (like [Plotly](https://plotly.com/) or [Chart.js](https://www.chartjs.org/)) directly into the HTML templates.
