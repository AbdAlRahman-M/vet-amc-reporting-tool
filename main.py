import argparse
import calendar
from datetime import date, datetime
from jinja2 import Environment, FileSystemLoader
import pandas as pd
from pathlib import Path
import re
import src.generate_report as report
import src.transform_data as transform
import sys

def parse_period_date(d: str) -> tuple[int, int]:
    """Validates and returns year and month from the passed date."""

    try:
        y, m = re.split(r"[-\/,;]", d)
    except ValueError as e:
        sys.exit(f"Invalid value passed: '{d}! Valid example: 2026-01.")

    # Validate
    try:
        y = int(y)
    except ValueError:
        sys.exit(f"Invalid value passed for year in '{d}'! This value must be an integer!")

    try:
        m = int(m)
    except ValueError:
        sys.exit(f"Invalid value passed for month in '{d}'! This value msut be an integer!")

    try:
        date(y, m, 1)
    except ValueError:
        sys.exit(f"Invalid value passed for year or month in {d}.")

    return y, m

if __name__ == "__main__":
    # Parse and validate arguments
    arg_parser = argparse.ArgumentParser(
        description="A script that process vet consumption data from vet healthcare units, and generates 1 HTML report for every vet unit."
    )

    arg_parser.add_argument(
        "period_start",
        help="Year and month marking the start of the reporting period e.g., 2026-01."
    )

    arg_parser.add_argument(
        "period_end",
        help="Year and month marking the end of the reporting period e.g., 2026-03."
    )

    args = arg_parser.parse_args()
    period_start = date(*parse_period_date(args.period_start), 1)
    end_y, end_m = parse_period_date(args.period_end)
    period_end = date(end_y, end_m, calendar.monthrange(end_y, end_m)[1])

    if period_start > period_end:
        sys.exit(f"Invalid input for reporting period: from '{period_start}' to '{period_end}'")

    # Load and transform data
    print("Loading data...")

    DATA_PATH = "./data/consumption-files/"
    SHEET_NAME = "Consumption"

    try:
        df_combined = transform.combine_data(dir_path=DATA_PATH, sheet_name=SHEET_NAME)
        transform.standardize_col_names(df_combined)
        transform.remove_irrelevant_cols(df_combined)
        df_combined["vet_unit_id"] = df_combined["vet_unit_id"].str.strip().str.upper()
        df_combined = transform.unpivot_active_subst(df_combined)
        transform.standardize_units(df_combined, "api_per_content", "api_per_content_unit")
        transform.standardize_units(df_combined, "pack_size", "pack_size_unit")
        df_api = pd.read_excel("./data/dimensions/substances.xlsx", sheet_name="API")
        transform.get_metric_amounts(df_combined, "api_str", "api_str_unit", df_api)
        transform.standardize_units(df_combined, "api_str", "api_str_unit")
    except Exception as e:
        print("Data transformation failed!")
        sys.exit(e)

    print("Data loaded and transformed successfully...")

    # Validate unit codes
    print("Checking veterinary unit codes...")
    try:
        df_vet_units = pd.read_excel("./data/dimensions/vet-units.xlsx", sheet_name="Vet. Units")
    except FileNotFoundError:
        sys.exit("The veterinary units file could not be found! Place it in './data/dimensions/' before running the script.")
    
    df_vet_units.rename(columns=lambda col: col.replace(" ", "_").lower(), inplace=True)
    df_vet_units["id"] = df_vet_units["id"].str.strip().str.upper()

    vet_unit_ids = set(df_combined["vet_unit_id"])
    diff = vet_unit_ids - set(df_vet_units["id"])
    if diff:  # if any reported unit codes are not in the reference sheet
        sys.exit(f"Invalid veterinary units codes '{','.join(diff)}' found in the data!")

    # Load template
    env = Environment(loader=FileSystemLoader("./template"))
    template = env.get_template("template.html")
    exec_time = datetime.now()
    out_path = Path("./output/" + exec_time.strftime("%y%m%d%H%M%S"))
    out_path.mkdir()

    # Generate reports
    print("Generating reports...")
    report.calculate_qty_grams(df_combined)
    
    df_filtered_period = df_combined[
        (df_combined["week_start"].dt.date >= period_start) &
        (df_combined["week_end"].dt.date <= period_end)
    ]
    
    data = {
        "reporting_period": f"{period_start.strftime("%B %Y")} - {period_end.strftime("%B %Y")}",
        "date_generated": date.today().strftime("%d %B %Y")
    }

    generated_count = 0
    vet_units_count = len(vet_unit_ids)
    for vet_unit_id in vet_unit_ids:
        # Generate data
        df_filtered_unit = df_filtered_period[df_filtered_period["vet_unit_id"] == vet_unit_id]

        report.get_header_data(data, vet_unit_id, df_vet_units)
        report.get_most_used_data(data, df_filtered_unit, df_api)
        report.get_kpi_cards_data(data, df_filtered_unit["quantity_grams"].sum())
        report.get_antimicrobial_classes_data(data, df_filtered_unit, df_api)
        report.get_routes_data(data, df_filtered_unit)
        report.get_species_data(data, df_filtered_unit)
        
        # Render report html
        html = template.render(data)
        file_name = "-".join([vet_unit_id, data["vet_unit_name"].replace(" ", "_").lower()]) + ".html"
        with open(out_path / file_name, "w", encoding="utf-8") as f:
            f.write(html)

        generated_count += 1
        print(f"Generated: {generated_count}/{vet_units_count} files, Remaining: {vet_units_count - generated_count} files...")
        
    with open(out_path / "_summary.txt", "w") as f:
        f.writelines([
            f"Execution time: {exec_time.strftime("%Y-%m-%d %H:%M:%S")}\n",
            f"Reporting period: from '{period_start}' to '{period_end}'\n",
            f"Number of reports generated: {vet_units_count}"
        ])

    print(f"Reports generated and saved in '{out_path}'")
