import pandas as pd


def check_missing_values(df):
    """Show columns that have missing values."""
    missing_values = df.isna().sum()
    missing_values = missing_values[missing_values > 0]

    if missing_values.empty:
        print("No missing values found.")
    else:
        print("WARNING: Missing values found.")
        print(missing_values)

    return missing_values


def check_duplicates(df):
    """Show the number of exact duplicate rows."""
    duplicate_count = df.duplicated().sum()

    if duplicate_count == 0:
        print("No duplicate rows found.")
    else:
        print(f"WARNING: {duplicate_count} duplicate rows found.")

    return duplicate_count


def check_required_columns(df, required_columns):
    """Check if important columns are present."""
    missing_columns = []

    for column in required_columns:
        if column not in df.columns:
            missing_columns.append(column)

    if not missing_columns:
        print("All required columns are present.")
    else:
        print("WARNING: Missing required columns:")
        print(missing_columns)

    return missing_columns


def check_amount_column(df, column_name):
    """Check if an amount column contains values that are not numbers."""
    if column_name not in df.columns:
        print(f"WARNING: '{column_name}' column was not found.")
        return pd.Series(dtype=object)

    amount_values = pd.to_numeric(df[column_name], errors="coerce")
    invalid_rows = df[df[column_name].notna() & amount_values.isna()]

    if invalid_rows.empty:
        print(f"No invalid values found in '{column_name}'.")
    else:
        print(f"WARNING: {len(invalid_rows)} invalid amount values found in '{column_name}'.")

    return invalid_rows
