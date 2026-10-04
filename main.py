import argparse
import calendar
from datetime import date
import re
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

    # Load and transform data

    # Generate reports