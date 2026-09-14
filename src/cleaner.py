import re
from pathlib import Path

import pandas as pd

from src.paths import EXTRACTED_DIR, PROCESSED_DIR, create_data_folders


AMOUNT_WORDS = ["amount", "cost", "price", "value", "allocation"]


GRANTS_COLUMNS = [
    "record_number",
    "group_name",
    "group_type",
    "district",
    "constituency",
    "ward",
    "zone",
    "contact_person",
    "venture_type",
    "sector",
    "source_id",
    "year",
    "cdf_category",
]

COMMUNITY_PROJECT_COLUMNS = [
    "record_number",
    "project_name",
    "project_description",
    "sector",
    "type_of_project",
    "district",
    "constituency",
    "ward",
    "zone",
    "project_site_location",
    "distance_km",
    "year_funded",
    "work_package",
    "scope_of_works",
    "status",
    "comments",
    "source_id",
    "year",
    "cdf_category",
]

SKILLS_BURSARY_COLUMNS = [
    "record_number",
    "student_name",
    "nrc_no",
    "province",
    "district",
    "constituency",
    "ward",
    "zone",
    "gender",
    "course_or_skill",
    "skill_level",
    "programme_duration",
    "institution",
    "source_id",
    "year",
    "cdf_category",
]

SECONDARY_BURSARY_COLUMNS = [
    "record_number",
    "pupil_name",
    "province",
    "district",
    "constituency",
    "ward",
    "zone",
    "gender",
    "date_of_birth",
    "grade",
    "grade_started_on_bursary",
    "new_grade_2025",
    "school_name",
    "school_location",
    "status",
    "source_id",
    "year",
    "cdf_category",
]


def first_existing(df, columns):
    combined_values = pd.Series(pd.NA, index=df.index, dtype=object)

    for column in columns:
        if column in df.columns:
            combined_values = combined_values.combine_first(df[column])

    return combined_values


def normalize_columns(df, column_map, final_columns):
    df = df.copy()
    normalized = pd.DataFrame(index=df.index, dtype=object)

    for final_column, possible_columns in column_map.items():
        normalized[final_column] = first_existing(df, possible_columns)

    for column in final_columns:
        if column not in normalized.columns:
            normalized[column] = pd.NA

    return normalized[final_columns]


def clean_column_names(df):
    """Make column names easier to use in Python."""
    df = df.copy()
    new_columns = []
    used_columns = {}

    for index, column in enumerate(df.columns):
        clean_name = str(column).strip().lower()
        clean_name = re.sub(r"[^a-z0-9]+", "_", clean_name)
        clean_name = clean_name.strip("_")

        if not clean_name:
            clean_name = f"column_{index + 1}"

        if clean_name in used_columns:
            used_columns[clean_name] += 1
            clean_name = f"{clean_name}_{used_columns[clean_name]}"
        else:
            used_columns[clean_name] = 1

        new_columns.append(clean_name)

    df.columns = new_columns
    return df


def clean_text(value):
    """Remove extra spaces and line breaks but keep missing values."""
    if pd.isna(value):
        return value

    text = str(value)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def clean_amount(value):
    """Change money values like K 50,000.00 into 50000.00."""
    if pd.isna(value):
        return pd.NA

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)

    text = clean_text(value)
    if text == "":
        return pd.NA

    text = re.sub(r"(?i)\b(zmw|kwacha|k)\b", "", text)
    text = text.replace(",", "")
    text = text.replace(" ", "")

    match = re.search(r"-?\d+(\.\d+)?", text)
    if not match:
        return pd.NA

    return float(match.group())


def remove_empty_rows(df):
    """Remove rows where every cell is empty."""
    df = df.copy()
    df = df.replace(r"^\s*$", pd.NA, regex=True)
    return df.dropna(how="all")


def remove_duplicates(df):
    """Remove exact duplicate rows."""
    return df.drop_duplicates()


def _amount_columns(df):
    columns = []

    for column in df.columns:
        column_text = str(column).lower()
        if any(word in column_text for word in AMOUNT_WORDS):
            columns.append(column)

    return columns


def _clean_amount_columns(df):
    df = df.copy()

    for column in _amount_columns(df):
        df[column] = df[column].apply(clean_amount)

    return df


def basic_clean(df):
    """Run the basic cleaning steps used by all CDF datasets."""
    df_clean = df.copy()
    df_clean = clean_column_names(df_clean)

    for column in df_clean.columns:
        if pd.api.types.is_object_dtype(df_clean[column]):
            df_clean[column] = df_clean[column].apply(clean_text)

    df_clean = remove_empty_rows(df_clean)
    df_clean = remove_duplicates(df_clean)
    df_clean = _clean_amount_columns(df_clean)
    return df_clean.reset_index(drop=True)


def clean_grants(df):
    df_clean = basic_clean(df)
    column_map = {
        "record_number": ["no", "s_n", "sn"],
        "group_name": ["name_of_group"],
        "group_type": ["type", "type_of_grou", "type_of_group"],
        "district": ["district"],
        "constituency": ["constituency", "constitues"],
        "ward": ["ward"],
        "zone": ["zone"],
        "contact_person": ["contact_person", "contact_person_name"],
        "venture_type": ["type_of_venture", "type_of_venture_spec"],
        "sector": ["sector"],
        "source_id": ["source_id"],
        "year": ["year"],
        "cdf_category": ["cdf_category"],
    }
    return normalize_columns(df_clean, column_map, GRANTS_COLUMNS)


def clean_community_projects(df):
    df_clean = basic_clean(df)
    column_map = {
        "record_number": ["no", "s_n", "sn"],
        "project_name": ["project_name", "name_of_roads"],
        "project_description": ["project_description"],
        "sector": ["sector"],
        "type_of_project": ["type_of_project"],
        "district": ["district"],
        "constituency": ["constituency"],
        "ward": ["ward"],
        "zone": ["zone"],
        "project_site_location": ["project_site_location"],
        "distance_km": ["distance_km", "distance"],
        "year_funded": ["year_funded"],
        "work_package": ["work_package_inclusive_of_cdf_branding"],
        "scope_of_works": ["scope_of_works", "scope_of_work"],
        "status": ["status", "comments_remarks"],
        "comments": ["comments"],
        "source_id": ["source_id"],
        "year": ["year"],
        "cdf_category": ["cdf_category"],
    }
    normalized = normalize_columns(df_clean, column_map, COMMUNITY_PROJECT_COLUMNS)

    # Some Mumbwa road rows place the distance in the district column.
    has_road_distance = normalized["district"].astype(str).str.contains("km", case=False, na=False)
    if has_road_distance.any():
        missing_distance = has_road_distance & normalized["distance_km"].isna()
        normalized.loc[missing_distance, "distance_km"] = normalized.loc[missing_distance, "district"]
        normalized.loc[has_road_distance, "district"] = "Mumbwa"

    return normalized


def clean_skills_bursaries(df):
    df_clean = basic_clean(df)
    column_map = {
        "record_number": ["no", "s_n", "sn"],
        "student_name": ["name_of_student"],
        "nrc_no": ["nrc_no"],
        "province": ["province"],
        "district": ["district"],
        "constituency": ["constituency"],
        "ward": ["ward"],
        "zone": ["zone"],
        "gender": ["gender_m_f", "gender"],
        "course_or_skill": ["name_of_skill", "name_of_course", "name_of_skill_programme"],
        "skill_level": ["level_of_skill"],
        "programme_duration": ["programme_duration", "programme_months", "course_duration"],
        "institution": ["training_institute_tevet_zns", "name_of_institution"],
        "source_id": ["source_id"],
        "year": ["year"],
        "cdf_category": ["cdf_category"],
    }
    return normalize_columns(df_clean, column_map, SKILLS_BURSARY_COLUMNS)


def clean_secondary_bursaries(df):
    df_clean = basic_clean(df)
    column_map = {
        "record_number": ["no", "s_n", "sn"],
        "pupil_name": ["name_of_pupil"],
        "province": ["province"],
        "district": ["district"],
        "constituency": ["constituency"],
        "ward": ["ward"],
        "zone": ["zone"],
        "gender": ["gender_m_f", "gender"],
        "date_of_birth": ["date_of_birth"],
        "grade": ["grade"],
        "grade_started_on_bursary": ["grade_started_on_bursary"],
        "new_grade_2025": ["new_grade_2025"],
        "school_name": ["name_of_school"],
        "school_location": ["school_location_district", "school_location"],
        "status": ["status"],
        "source_id": ["source_id"],
        "year": ["year"],
        "cdf_category": ["cdf_category"],
    }
    return normalize_columns(df_clean, column_map, SECONDARY_BURSARY_COLUMNS)


def add_source_info(
    df,
    source_document=None,
    constituency=None,
    year=None,
    cdf_category=None,
    extraction_method=None,
):
    """Add simple source information when it is known."""
    df = df.copy()

    source_values = {
        "source_document": source_document,
        "constituency": constituency,
        "year": year,
        "cdf_category": cdf_category,
        "extraction_method": extraction_method,
    }

    for column, value in source_values.items():
        if value is not None and column not in df.columns:
            df[column] = value

    return df


def choose_cleaning_function(file_name):
    """Pick a cleaning function using the CSV file name."""
    name = file_name.lower()

    if "grant" in name:
        return clean_grants
    if "community" in name or "project" in name:
        return clean_community_projects
    if "skill" in name:
        return clean_skills_bursaries
    if "secondary" in name or "boarding" in name:
        return clean_secondary_bursaries

    return basic_clean


def source_id_from_file_name(file_name):
    name = file_name.lower()

    if "mumbwa" in name:
        constituency = "mumbwa"
    elif "nangoma" in name:
        constituency = "nangoma"
    else:
        return None

    if "not_approved" in name:
        category = "not_approved_projects"
    elif "community" in name or "project" in name:
        category = "community_projects"
    elif "grant" in name:
        category = "grants"
    elif "skill" in name:
        category = "skills_bursaries"
    elif "secondary" in name or "boarding" in name:
        category = "secondary_bursaries"
    else:
        return None

    return f"cdf_{category}_{constituency}_2025"


def _next_output_path(input_file, output_dir):
    clean_name = f"{input_file.stem}_clean.csv"
    output_file = output_dir / clean_name

    number = 2
    while output_file.exists():
        output_file = output_dir / f"{input_file.stem}_clean_{number}.csv"
        number += 1

    return output_file


def clean_csv_file(input_file, output_dir=PROCESSED_DIR):
    """Clean one extracted CSV file and save a new processed CSV."""
    input_file = Path(input_file)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Cleaning: {input_file.name}")
    df = pd.read_csv(input_file, sep="|")
    if "source_id" not in df.columns:
        source_id = source_id_from_file_name(input_file.name)
        if source_id is not None:
            df["source_id"] = source_id
    rows_before = len(df)

    cleaning_function = choose_cleaning_function(input_file.name)
    df_clean = cleaning_function(df)
    rows_after = len(df_clean)

    first_output_file = output_dir / f"{input_file.stem}_clean.csv"
    if first_output_file.exists():
        print(f"Already exists, skipping: {first_output_file}")
        print()
        return first_output_file

    output_file = first_output_file
    df_clean.to_csv(output_file, index=False, sep="|")

    print(f"Rows before: {rows_before}")
    print(f"Rows after: {rows_after}")
    print(f"Saved to: {output_file}")
    print()

    return output_file


def clean_all_extracted_csv_files(input_dir=EXTRACTED_DIR, output_dir=PROCESSED_DIR):
    """Clean every CSV file in data/extracted."""
    create_data_folders()
    input_dir = Path(input_dir)
    csv_files = sorted(input_dir.glob("*.csv"))

    if not csv_files:
        print(f"No CSV files found in {input_dir}")
        return []

    cleaned_files = []
    for input_file in csv_files:
        cleaned_files.append(clean_csv_file(input_file, output_dir))

    return cleaned_files


if __name__ == "__main__":
    clean_all_extracted_csv_files()
