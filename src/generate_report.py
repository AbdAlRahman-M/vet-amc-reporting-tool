import pandas as pd

def calculate_qty_grams(df: pd.DataFrame) -> None:
    """Adds a new column for quantity consumed in metric grams."""

    df["quantity_grams"] = (df["api_str"] * df["pack_size"] * df["quantity_packs"]) / df["api_per_content"]

def format_quantity(quantity_grams: float) -> str:
    """Formats consumption figures in human-readable formats."""

    if quantity_grams < 1:
        return f"{quantity_grams * 1e3:.1f} MG"
    elif quantity_grams >= 1e3:
        return f"{quantity_grams * 1e-3:,.1f} KG"
    else:
        return f"{quantity_grams:.1f} G"

def get_header_data(data_dict: dict, vet_unit_id: str, df_vet_units: pd.DataFrame) -> None:
    """Adds data for the report header to the data dictionary."""

    data_dict.update({
        "vet_unit_id": vet_unit_id,
        "vet_unit_name": df_vet_units.loc[df_vet_units["id"] == vet_unit_id, "name_english"].iloc[0]
    })

def get_most_used_data(data_dict: dict, df_filtered_unit: pd.DataFrame, df_api: pd.DataFrame) -> None:
    """Adds data for the most used antimicrobials to the data dictionary."""
    
    df_most_used = df_filtered_unit.groupby("api")[["quantity_grams"]].sum().rename(columns={"quantity_grams": "amount"}).sort_values(by="amount", ascending=False)

    df_most_used["rank"] = range(1, df_most_used.shape[0] + 1)
    df_most_used["percent"] = df_most_used["amount"] / df_most_used["amount"].sum()
    df_most_used["cumul_percent"] = df_most_used["percent"].cumsum()

    df_most_used["amount"] = df_most_used["amount"].apply(format_quantity)
    df_most_used[["percent", "cumul_percent"]] = df_most_used[["percent", "cumul_percent"]].map("{:.1%}".format)

    df_most_used = pd.merge(
        left=df_most_used, right=df_api.loc[~df_api.duplicated(subset="api_id", keep="first"), ["api_id", "api_name"]],
        left_on="api", right_on="api_id",
        how="left"
    ).drop(columns="api_id").rename(columns={"api_name":"substance"})

    data_dict.update(
        {"most_used_data": df_most_used.to_dict(orient="records")}
    )

def get_kpi_cards_data(data_dict: dict, total_quantity) -> None:
    """Adds data for KPI cards to the data dictionary."""
    
    data_dict.update({
        "total_qty": format_quantity(total_quantity),
        "most_used_am": data_dict["most_used_data"][0]["substance"]
    })

def get_antimicrobial_classes_data(data_dict: dict, df_filtered_unit: pd.DataFrame, df_api: pd.DataFrame) -> None:
    """Adds data for the antimicrobial classes table to the data dictionary."""

    df_classes = pd.merge(
        left=df_filtered_unit, right=df_api.loc[~df_api.duplicated(subset="api_id", keep="first"), ["api_id", "api_class"]],
        left_on="api", right_on="api_id",
        how="left"
    ).groupby("api_class", as_index=False)[["quantity_grams"]].sum()

    df_classes = df_classes.rename(columns={
        "api_class":"class",
        "quantity_grams":"amount"
    }).sort_values(by="amount", ascending=False)
    
    df_classes["rank"] = range(1, df_classes.shape[0] + 1)
    df_classes["percent"] = df_classes["amount"] / df_classes["amount"].sum()
    df_classes["cumul_percent"] = df_classes["percent"].cumsum()

    df_classes["amount"] = df_classes["amount"].apply(format_quantity)
    df_classes[["percent", "cumul_percent"]] = df_classes[["percent", "cumul_percent"]].map("{:.1%}".format)

    data_dict.update(am_class_data = df_classes.to_dict(orient="records"))

def get_routes_data(data_dict: dict, df_filtered_unit: pd.DataFrame) -> None:
    """Adds data for the consumption by routes table to the data dictionary."""

    df_routes = df_filtered_unit.groupby("route", as_index=False)[["quantity_grams"]].sum()
    df_routes = df_routes.rename(columns={"quantity_grams":"amount"}).sort_values(by="amount", ascending=False)

    df_routes["rank"] = range(1, df_routes.shape[0] + 1)
    df_routes["percent"] = df_routes["amount"] / df_routes["amount"].sum()
    df_routes["cumul_percent"] = df_routes["percent"].cumsum()

    df_routes["amount"] = df_routes["amount"].apply(format_quantity)
    df_routes[["percent", "cumul_percent"]] = df_routes[["percent", "cumul_percent"]].map("{:.1%}".format)

    data_dict.update(routes_data = df_routes.to_dict(orient="records"))

def get_species_data(data_dict: dict, df_filtered_unit: pd.DataFrame) -> None:
    """Adds data for consumption by species to the data dictionary."""

    df_species = df_filtered_unit.groupby("species", as_index=False)[["quantity_grams"]].sum()
    df_species = df_species.rename(columns={"quantity_grams":"amount"}).sort_values(by="amount", ascending=False)

    df_species["rank"] = range(1, df_species.shape[0] + 1)
    df_species["percent"] = df_species["amount"] / df_species["amount"].sum()
    df_species["cumul_percent"] = df_species["percent"].cumsum()

    df_species["amount"] = df_species["amount"].apply(format_quantity)
    df_species[["percent", "cumul_percent"]] = df_species[["percent", "cumul_percent"]].map("{:.1%}".format)

    data_dict.update(species_data = df_species.to_dict(orient="records"))
    