from pathlib import Path

import pandas as pd

from src.paths import FINAL_DIR, PROCESSED_DIR, create_data_folders


FINAL_FILE_NAMES = {
    "grants": "db-unza26-csc4792-mumbwa_town_council_cdf_grants.csv",
    "community_projects": "db-unza26-csc4792-mumbwa_town_council_cdf_community_projects.csv",
    "not_approved_community_projects": "db-unza26-csc4792-mumbwa_town_council_cdf_not_approved_community_projects.csv",
    "skills_bursaries": "db-unza26-csc4792-mumbwa_town_council_cdf_skills_bursaries.csv",
    "secondary_bursaries": "db-unza26-csc4792-mumbwa_town_council_cdf_secondary_bursaries.csv",
}


def _read_processed_files(category, input_dir):
    files = sorted(Path(input_dir).glob(f"*_{category}_clean.csv"))

    if category == "community_projects":
        files = [file for file in files if "not_approved" not in file.name]

    if not files:
        return pd.DataFrame()

    datasets = [pd.read_csv(file, sep="|") for file in files]
    return pd.concat(datasets, ignore_index=True)


def create_final_datasets(input_dir=PROCESSED_DIR, output_dir=FINAL_DIR):
    create_data_folders()
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_files = []

    for category, file_name in FINAL_FILE_NAMES.items():
        df = _read_processed_files(category, input_dir)

        if df.empty:
            print(f"No processed files found for {category}")
            continue

        output_file = output_dir / file_name
        try:
            df.to_csv(output_file, index=False, sep="|")
        except PermissionError:
            print(f"Could not update because the file is open: {output_file}")
            print("Close the CSV file and run python -m src.integrator again.")
            print()
            continue

        print(f"Created: {output_file}")
        print(f"Rows: {len(df)}")
        print()
        output_files.append(output_file)

    return output_files


if __name__ == "__main__":
    create_final_datasets()
