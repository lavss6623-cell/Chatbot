import pandas as pd

DATA_FILE = "data/2025 cutoff_data_clean.csv"

print("=" * 60)
print("TNEA DATASET VALIDATION")
print("=" * 60)

# Load dataset
df = pd.read_csv(DATA_FILE)
df.columns = df.columns.str.strip()

print("\n1. DATASET SHAPE")
print("-" * 60)
print(f"Rows    : {len(df)}")
print(f"Columns : {len(df.columns)}")

print("\n2. COLUMN NAMES")
print("-" * 60)

expected_columns = [
    "college_code",
    "college_name",
    "branch",
    "oc",
    "bc",
    "bcm",
    "mbc",
    "sc",
    "sca",
    "st"
]

print("Expected:")
print(expected_columns)

print("\nActual:")
print(list(df.columns))

if list(df.columns) == expected_columns:
    print("STATUS: PASS")
else:
    print("STATUS: FAIL")

print("\n3. MISSING VALUES")
print("-" * 60)

missing = df.isna().sum()

print(missing)

print("\n4. DUPLICATE ROWS")
print("-" * 60)

duplicate_rows = df.duplicated().sum()

print(f"Duplicate rows: {duplicate_rows}")

if duplicate_rows == 0:
    print("STATUS: PASS")
else:
    print("STATUS: CHECK")

print("\n5. DUPLICATE COLLEGE + BRANCH")
print("-" * 60)

duplicate_college_branch = df.duplicated(
    subset=["college_code", "branch"]
).sum()

print(
    f"Duplicate college_code + branch records: "
    f"{duplicate_college_branch}"
)

if duplicate_college_branch == 0:
    print("STATUS: PASS")
else:
    print("STATUS: CHECK")

print("\n6. DATA TYPES")
print("-" * 60)

print(df.dtypes)

print("\n7. CUTOFF RANGE")
print("-" * 60)

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

    numeric_values = pd.to_numeric(
        df[column],
        errors="coerce"
    )

    invalid = df[
        numeric_values.notna()
        & (
            (numeric_values < 0)
            | (numeric_values > 200)
        )
    ]

    print(
        f"{column.upper():4} -> "
        f"min={numeric_values.min()} "
        f"max={numeric_values.max()} "
        f"invalid={len(invalid)}"
    )

print("\n8. NON-NUMERIC CUTOFF VALUES")
print("-" * 60)

for column in cutoff_columns:

    converted = pd.to_numeric(
        df[column],
        errors="coerce"
    )

    original_not_null = df[column].notna()

    non_numeric = df[
        original_not_null & converted.isna()
    ]

    print(
        f"{column.upper():4} -> "
        f"{len(non_numeric)} non-numeric values"
    )

print("\n9. COLLEGE CODE CONSISTENCY")
print("-" * 60)

college_code_name_counts = (
    df.groupby("college_code")["college_name"]
    .nunique()
)

inconsistent_codes = (
    college_code_name_counts[
        college_code_name_counts > 1
    ]
)

print(
    f"College codes with multiple names: "
    f"{len(inconsistent_codes)}"
)

if len(inconsistent_codes) == 0:
    print("STATUS: PASS")
else:
    print("STATUS: CHECK")

print("\n10. EMPTY TEXT VALUES")
print("-" * 60)

for column in ["college_name", "branch"]:

    empty = (
        df[column]
        .fillna("")
        .astype(str)
        .str.strip()
        .eq("")
        .sum()
    )

    print(
        f"{column}: {empty} empty values"
    )

print("\n" + "=" * 60)
print("VALIDATION COMPLETE")
print("=" * 60)

print("\n11. COLLEGE CODE VALIDATION")
print("-" * 60)

# Missing college codes
missing_codes = df["college_code"].isna().sum()

print(f"Missing college codes : {missing_codes}")

# Zero codes
zero_codes = (df["college_code"] == 0).sum()

print(f"Zero college codes    : {zero_codes}")

# Negative codes
negative_codes = (df["college_code"] < 0).sum()

print(f"Negative college codes: {negative_codes}")

# Non-integer codes
non_integer_codes = (
    df["college_code"] % 1 != 0
).sum()

print(f"Non-integer codes     : {non_integer_codes}")

# Unique college codes
unique_codes = df["college_code"].nunique()

print(f"Unique college codes  : {unique_codes}")

# Number of rows per college
college_counts = (
    df.groupby("college_code")
    .size()
    .sort_values(ascending=False)
)

print("\nMost branches recorded for a single college:")

print(college_counts.head(10))

print("\nSTATUS:")

if (
    missing_codes == 0
    and zero_codes == 0
    and negative_codes == 0
    and non_integer_codes == 0
):
    print("PASS")
else:
    print("CHECK")
    
print("\n12. BRANCH VALIDATION")
print("-" * 60)

# Get all unique branch names
branches = (
    df["branch"]
    .dropna()
    .astype(str)
    .str.strip()
)

unique_branches = sorted(branches.unique())

print(f"Unique branch names: {len(unique_branches)}")

print("\nAll branch names:")
for i, branch in enumerate(unique_branches, start=1):
    print(f"{i:3}. {branch}")

# Check normalized branch names
normalized = (
    branches
    .str.upper()
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)

branch_groups = {}

for original, normalized_name in zip(branches, normalized):
    branch_groups.setdefault(normalized_name, set()).add(original)

inconsistent_branches = {
    key: values
    for key, values in branch_groups.items()
    if len(values) > 1
}

print("\nCase/whitespace inconsistencies:")
print(f"Groups found: {len(inconsistent_branches)}")

for normalized_name, variants in inconsistent_branches.items():
    print(f"\nNormalized: {normalized_name}")
    for variant in sorted(variants):
        print(f"  - {variant}")

# Check obvious spelling
typo_keywords = [
    "BUSSINESS",
    "BUSSINESS SYSTEM"
]

print("\nPossible spelling issues:")

found_typo = False

for keyword in typo_keywords:

    matches = [
        branch
        for branch in unique_branches
        if keyword.lower() in branch.lower()
    ]

    if matches:
        found_typo = True

        for branch in matches:
            print(f"  - {branch}")

if not found_typo:
    print("  None found")