import pandas as pd

INPUT_FILE = "data/2025 cutoff data.xlsx"
OUTPUT_FILE = "data/2025 cutoff_data_clean.csv"


def clean_dataset():
    # Read Excel without assuming the first row is the header
    df = pd.read_excel(INPUT_FILE, header=None)

    # Find the actual header row
    header_index = df[
        df.apply(
            lambda row: row.astype(str).str.contains(
                "College Name",
                case=False,
                na=False
            ).any(),
            axis=1
        )
    ].index[0]

    # Use that row as the header
    df.columns = df.iloc[header_index]

    # Remove rows above the header
    df = df.iloc[header_index + 1:].copy()

    # Remove completely empty rows
    df = df.dropna(how="all")

    # Rename columns
    df = df.rename(columns={
        "Code": "college_code",
        "College Name": "college_name",
        "Branch": "branch",
        "OC": "oc",
        "BC": "bc",
        "BCM": "bcm",
        "MBC": "mbc",
        "SC": "sc",
        "SCA": "sca",
        "ST": "st"
    })

    # Clean text columns
    text_columns = [
        "college_name",
        "branch"
    ]

    for column in text_columns:
        df[column] = df[column].astype(str).str.strip()

    # Convert cutoff columns to numeric
    cutoff_columns = [
        "oc",
        "bc",
        "bcm",
        "mbc",
        "sc",
        "sca",
        "st"
    ]

    for column in cutoff_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # Remove rows without college or branch
    df = df.dropna(
        subset=["college_name", "branch"]
    )

    # Reset index
    df = df.reset_index(drop=True)

    # Save cleaned dataset
    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("Dataset cleaned successfully.")
    print(f"Rows: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    print()
    print(df.head())


if __name__ == "__main__":
    clean_dataset()