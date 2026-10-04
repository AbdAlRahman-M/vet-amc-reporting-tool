# Veterinary Antimicrobial Use Reporting Tool

An automated Python data pipeline that processes veterinary consumption records to generate descriptive statistical **HTML report files** tracking antimicrobial usage across different veterinary units.

## ⚙️ How It Works

1. **Data Extraction & Transformation:** [Pandas](https://pandas.pydata.org/) extracts raw consumption records from source files and transforms the data.
2. **Analytics & Aggregation:** The script calculates descriptive statistics (e.g., usage volume, drug classification frequencies) and prepares metrics.
3. **Report Generation:** The pipeline dynamically compiles the aggregated data into standalone HTML reports, generating one tailored file per individual veterinary health unit.

## 🚀 Tech Stack

- **Languages:** Python 3.14.7
- **Data Processing:** [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
- **Visualization/Output:** HTML5, CSS3, [Jinja](https://pypi.org/project/Jinja2/)

## 📁 Repository Structure

```text
./
├── data/
│   ├── consumption-files/  # Raw source files (Excel)
│   └── dimensions/
│       └── substances.xlsx # Descriptive attributes for antimicrobial substances
├── output/                 # Generated per-unit HTML report files
├── src/
│   ├── transform.py        # Pandas data cleaning and transformation
│   └── generate_report.py  # Statistical aggregation and HTML compilation
├── template/               # HTML/CSS template for the reports
│   ├── styles.css
│   └── template.html
├── main.py                 # Pipeline orchestrator script
├── README.md
└── requirements.txt        # Project dependencies
```

## 🛠️ Prerequisites & Setup

### 1. Clone the Repository

bash

```bash
git clone
cd vet-amc-reporting-tool
```

### 2. Set Up a Virtual Environment

```bash
python -m venv .venv
source .venv/Scripts/activate  # On Windows use: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Prepare Source Data

- Place your raw data Excel sheets (.xlsx) inside the `data/consumption-files/` directory.
- [Download] the veterinary units Excel file (requires access), and place it inside the `data/dimensions/` directory.

### 5. Run the Pipeline

Execute the main script to process the data and build the reports:

```bash
python main.py
```

Once complete, open the `output/[timestamp of execution]/`, directory to view the generated individual HTML reports. The execution timestamp is the exact date and time when the script was executed.

## 📝 Future Enhancements

- Integrate interactive charting libraries (like [Plotly](https://plotly.com/) or [Chart.js](https://www.chartjs.org/)) directly into the HTML templates.
