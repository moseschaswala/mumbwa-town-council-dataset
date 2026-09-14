import csv
import re
from pathlib import Path

import numpy as np
import pandas as pd

from src.paths import DATA_DIR


PIPE = "|"
ROOT = DATA_DIR / "council_structure_management_data"
SOURCE_PAGES_FILE = ROOT / "processed" / "website_pages_clean.csv"


def clean_dataframe(df):
    df = df.copy()

    if df.empty:
        return df

    for column in df.columns:
        if pd.api.types.is_object_dtype(df[column]):
            df[column] = df[column].map(lambda value: re.sub(r"\s+", " ", value).strip() if isinstance(value, str) else value)

    df = df.replace(r"^\s*$", np.nan, regex=True)
    df = df.dropna(how="all")
    df = df.dropna(axis=1, how="all")
    df = df.drop_duplicates()
    return df.reset_index(drop=True)


def save_csv(df, output_file):
    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    df = clean_dataframe(df)
    df.to_csv(output_file, index=False, sep=PIPE, quoting=csv.QUOTE_MINIMAL)
    return df


def load_pages():
    if not SOURCE_PAGES_FILE.exists():
        raise FileNotFoundError(f"Missing source page data: {SOURCE_PAGES_FILE}")

    return pd.read_csv(SOURCE_PAGES_FILE, sep=PIPE)


def page_row(pages, page_id):
    rows = pages[pages["Page ID"].eq(page_id)]
    if rows.empty:
        return None
    return rows.iloc[0]


def source_details(row):
    return {
        "Source Page ID": row["Page ID"],
        "Source Page Title": row["Page Title"],
        "Source URL": row["Page URL"],
    }


def build_officials(pages):
    rows = []

    senior = page_row(pages, "senior_management")
    if senior is not None:
        senior_officials = [
            ("Mr. John Machai", "COUNCIL SECRETARY"),
            ("Mr. Gabriel Akayombokwa", "Director Human Resource and Administration"),
            ("Mr. Oblly Banda", "Director of Finance"),
            ("Mr. Andy Kabwe", "Director of Planning"),
            ("Eng. Innocent Chirwa", "Director of Engineering Services"),
            ("Truddy Mukosha/Inness Luyako", "Director of Community and Social Services"),
            ("Dr. Katherine Kalumba", "Director of Health Services"),
            ("Dr. Penelope Kasanga", "Director of Livestock, Fisheries and Veterinary"),
            ("Mr. Gershom Kalumba", "Director of Agriculture"),
        ]
        for name, position in senior_officials:
            rows.append({"Name": name, "Position": position, **source_details(senior)})

    chairman = page_row(pages, "council_chairman")
    if chairman is not None:
        rows.append({"Name": "Charlie Masumo", "Position": "COUNCIL CHAIRPERSON", **source_details(chairman)})

    home = page_row(pages, "home")
    if home is not None:
        rows.extend(
            [
                {"Name": "Mr. Charlie Masumo", "Position": "Council Chairperson", **source_details(home)},
                {"Name": "Carol .C. Mkandawire", "Position": "Council Secretary", **source_details(home)},
            ]
        )

    return pd.DataFrame(rows)


def build_councillors(pages):
    rows = []

    councillors = [
        ("Nangoma", "Survoy Hichintu Nalubanda", np.nan, "Councilor", "nangoma_constituency"),
        ("Nangoma", "Fines Shimbwambwa", "Keezwa", "Ward Councillor", "nangoma_constituency"),
        ("Nangoma", "Debby Chilombe", "Chooma", "Ward Councillor", "nangoma_constituency"),
        ("Nangoma", "Clive Hamooya", "Chisalu", "Ward Councillor", "nangoma_constituency"),
        ("Nangoma", "Clifford Himaluwani", "Matala", "Ward Councilor", "nangoma_constituency"),
        ("Nangoma", "Aubrine Mulela", "Sichanzu", "Ward Councillor", "nangoma_constituency"),
        ("Mumbwa Central", "Shamaindi Zambwe", "Naluvwi", "Ward Councillor", "mumbwa_central_constituency"),
        ("Mumbwa Central", "Oscar Susik", "Lutale", "Ward Councillor", "mumbwa_central_constituency"),
        ("Mumbwa Central", "Joseph Chinyama", "Nalusanga", "Ward Councillor", "mumbwa_central_constituency"),
        ("Mumbwa Central", "Jamila .M. Suleman", "Shimbizhi", "Ward Councillor", "mumbwa_central_constituency"),
        ("Mumbwa Central", "Geoffrey .L.Lubinda-", "Mupona", "Ward Councillor", "mumbwa_central_constituency"),
        ("Mumbwa Central", "Enerst Muumpuka", "Mpusu", "Ward Councillor", "mumbwa_central_constituency"),
        ("Mumbwa Central", "Chebo Mulowa", "Kalwanyembe", "Ward Councillor", "mumbwa_central_constituency"),
        ("Mumbwa Central", "Moven Chasemena", "Mumba", "Deputy Council Chairperson-Ward Councillor", "mumbwa_central_constituency"),
        ("Mumbwa Central", "Audrey Chikwamba", "Makebo", "Ward Councillor", "mumbwa_central_constituency"),
        ("Mumbwa Central", np.nan, "Kamilambo", "Ward Councillor", "mumbwa_central_constituency"),
    ]

    for constituency, name, ward, position, page_id in councillors:
        row = page_row(pages, page_id)
        if row is None:
            continue
        rows.append(
            {
                "Constituency": constituency,
                "Name": name,
                "Ward": ward,
                "Position": position,
                **source_details(row),
            }
        )

    return pd.DataFrame(rows)


def build_departments(pages):
    row = page_row(pages, "departments")
    if row is None:
        return pd.DataFrame()

    departments = [
        (
            "Institutional Management",
            "Consists of the principle officer who in this regard is the Council Secretary, as well as procurement and audit sections.",
        ),
        (
            "Planning",
            "The role of planning department is to plan the overall layout of the district, upgrading of shanty areas to modern standards, setting up of township boundaries, coming up with standard building plans which have to be adopted by everyone building, land distribution, processing of title deeds, HIV/AIDS, gender and human rights sensitisation, and community development activities. Through the section of public health, ensure a clean, healthy and green environment.",
        ),
        (
            "Engineering Services",
            "The role of this department is to facilitate engineering services such as; feeder roads, borehole drilling, inspection of buildings, scrutinizing building plans to make sure it is the required standard, providing burial site, fire brigade services, maintenance of plant and machinery.",
        ),
        (
            "Finance",
            "Collection of revenue, preparation of statutory obligation, preparation of books of accounts.",
        ),
        (
            "Human Resource and Administration",
            "Staff establishment, management of assets, records keeping, training and development, recruitment, staff appraisals, minutes and report writing, discipline, explanation of conditions of service to staff, Public relations services.",
        ),
        ("Fisheries, Livestock and Veterinary Services", np.nan),
        ("Agriculture", np.nan),
    ]

    return pd.DataFrame(
        [{"Department": department, "Description": description, **source_details(row)} for department, description in departments]
    )


def build_contacts(pages):
    rows = []

    for page_id in ["home", "senior_management", "departments", "contact_us"]:
        row = page_row(pages, page_id)
        if row is None:
            continue

        text = row["Page Text"]
        telephone = re.search(r"Tel:\s*([0-9]+)", text)
        email = re.search(r"Email;\s*([^\s]+)", text)
        po_box = re.search(r"P\.O\. Box:\s*([0-9]+)", text)

        rows.append(
            {
                "Institution": "Mumbwa Town Council",
                "District": "Mumbwa District",
                "Province": "Central Province",
                "Telephone": telephone.group(1) if telephone else np.nan,
                "P.O. Box": po_box.group(1) if po_box else np.nan,
                "Email": email.group(1) if email else np.nan,
                **source_details(row),
            }
        )

    return pd.DataFrame(rows)


def build_mandate_functions(pages):
    row = page_row(pages, "mandate")
    if row is None:
        return pd.DataFrame()

    text = row["Page Text"]
    start = text.find("overall functions of Local Authorities:")
    end = text.find("Contact Information")
    mandate_text = text[start:end] if start >= 0 and end > start else text

    parts = [part.strip(" ;.") for part in re.split(r"\s+[•�]\s+", mandate_text) if part.strip()]
    if parts and "overall functions" in parts[0]:
        parts = parts[1:]

    cleaned_parts = []
    for part in parts:
        part = re.split(r"\s+HAVE THE COUNCILS", part)[0].strip(" ;.")
        if part:
            cleaned_parts.append(part)

    return pd.DataFrame(
        [
            {"Function Number": index, "Function": function, **source_details(row)}
            for index, function in enumerate(cleaned_parts, start=1)
        ]
    )


def create_council_structure_management_datasets():
    pages = load_pages()

    outputs = {
        "officials": build_officials(pages),
        "councillors": build_councillors(pages),
        "departments": build_departments(pages),
        "contacts": build_contacts(pages),
        "mandate_functions": build_mandate_functions(pages),
    }

    for dataset_name, df in outputs.items():
        save_csv(df, ROOT / "intermediate" / f"{dataset_name}_raw.csv")
        save_csv(df, ROOT / "extracted" / f"{dataset_name}.csv")
        clean_df = save_csv(df, ROOT / "processed" / f"{dataset_name}_clean.csv")
        final_name = f"db-unza26-csc4792-mumbwa_town_council_council_structure_management_data_{dataset_name}.csv"
        final_df = save_csv(clean_df, ROOT / "final" / final_name)
        print(f"Created {final_name}: {len(final_df)} rows")

    return outputs


if __name__ == "__main__":
    create_council_structure_management_datasets()
