import pandas as pd
from pathlib import Path

def pascal_to_snake(text: str) -> str:
    """Converts names from Pascal to Snake case."""

    out = text[0].lower()
    for i in range(1, len(text) - 1):
        if text[i].isupper() and text[i + 1].islower():
            out += "_"
        out += text[i].lower()
    return out + text[-1].lower()

def combine_data(dir_path, sheet_name) -> pd.DataFrame:
    """Reads from all Excel sheets in a given directory, standardizes columns names, and combines all the files into a single data frame."""

    # Validate input
    root_path = Path(dir_path)
    if not root_path.is_dir():
        raise ValueError("This folder does not exist!")

    file_paths = [str(f) for f in root_path.glob("*.xlsx") if f.is_file()]

    if not file_paths:
        raise ValueError("The sepcified folder must contain at least one Excel file!")
        
    # Combine files
    df_list = [pd.read_excel(p, sheet_name=sheet_name) for p in file_paths]
    df_combined = pd.concat(df_list, ignore_index=True)
    num_cols = df_combined.select_dtypes(include=["number"]).columns
    df_combined[num_cols] = df_combined[num_cols].astype(float)

    return df_combined

def standardize_col_names(df: pd.DataFrame) -> None:
    """Standardizes column names in the data frame."""

    df.rename(columns=pascal_to_snake, inplace=True)

def remove_irrelevant_cols(
        df: pd.DataFrame,
        irrelevant=["sn", "date_created", "product_reg_num", "product_name"]
    ) -> pd.DataFrame:

    """Drops columns that are not relevant to the analysis."""

    df.drop(columns=irrelevant, inplace=True)

def unpivot_active_subst(df: pd.DataFrame) -> pd.DataFrame:
    """Transforms data to long format by unpivoting active substance columns."""

    return pd.wide_to_long(
        df,
        stubnames=["api", "api_str", "api_str_unit"],
        i=["vet_unit_id", "cons_id"],
        j="api_num",
        suffix=r"\d+"
    ).dropna(subset=["api", "api_str", "api_str_unit"]).reset_index()

def standardize_units(df: pd.DataFrame, measure_col: str, unit_col: str) -> None:
    """Standardize measurements to one unit to allow calculations."""

    unit_mapper = {
        "MG": {"factor":1e-3, "family":"G"},
        "KG": {"factor":1e3, "family":"G"},
        "ML": {"factor":1e-3, "family":"L"},
    }

    for k,v in unit_mapper.items():
        mask = df[unit_col].str.upper() == k
        df.loc[mask, measure_col] *=  v["factor"]
        df.loc[mask, unit_col] = v["family"]

def get_metric_amounts(df: pd.DataFrame, strength_col, unit_col, df_dim: pd.DataFrame) -> None:
    """Uses factors from the substances dimension talbe to extract weights of active drugs from prodrugs, and converts international units to metric units."""

    right_cols = ["api_id", "iu_factor", "prodrug_factor"]
    df = pd.merge(
        left=df, left_on="api",
        right=df_dim[right_cols], right_on="api_id",
        how="left"
    )

    if df["api_id"].isna().sum() > 0:
        raise Exception("Failed to retrieve substance attributes! One or more substances cannot be found in the reference table.")

    # Amounts in IU point to base drug so no need for extraction
    mask = df[unit_col] == "IU"
    df.loc[~mask, strength_col] *= df.loc[~mask, "prodrug_factor"]

    df[strength_col] *= df["iu_factor"]
    df.loc[mask, unit_col] = "MG"

    df.drop(columns=right_cols, inplace=True)
