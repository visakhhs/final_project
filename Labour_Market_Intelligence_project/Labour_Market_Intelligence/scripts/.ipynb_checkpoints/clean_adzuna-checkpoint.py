# determine the structure of the dataset
import pandas as pd
from config import ADZUNA_CSV

df = pd.read_csv(ADZUNA_CSV)

print(df.shape)
print(df.columns.tolist())
print(df.dtypes)


# Clean the historical Adzuna dataset.
from config import ADZUNA_CSV, ADZUNA_CLEAN
from logger import logger

# Clean the Adzuna historical dataset and save it to the processed data folder.
def clean_adzuna():
    
    logger.info("=" * 60)
    logger.info("Starting Adzuna data cleaning...")

# Load dataset
    logger.info(f"Loading dataset from: {ADZUNA_CSV}")

    df = pd.read_csv(ADZUNA_CSV)

    logger.info(f"Original dataset shape: {df.shape}")


# Remove duplicate jobs
    before = len(df)

    df = df.drop_duplicates(subset="id")

    duplicates_removed = before - len(df)

    logger.info(f"Duplicate jobs removed: {duplicates_removed}")
    logger.info(f"Shape after duplicate removal: {df.shape}")


# Remove rows with missing title or description
    before = len(df)

    df = df.dropna(subset=["title", "description"])

    removed = before - len(df)

    logger.info(f"Rows removed (missing title/description): {removed}")
    logger.info(f"Shape after removing missing values: {df.shape}")


# Convert created column to datetime
    df["created"] = pd.to_datetime(
        df["created"],
        errors="coerce"
    )

    before = len(df)

    df = df.dropna(subset=["created"])

    removed = before - len(df)

    logger.info(f"Rows removed (invalid dates): {removed}")

    
# Create average salary
    df["salary_avg"] = df[
        ["salary_min", "salary_max"]
    ].mean(axis=1)

    logger.info("Created salary_avg column.")


# Fill missing contract information
    df["contract_type"] = df["contract_type"].fillna("Unknown")
    df["contract_time"] = df["contract_time"].fillna("Unknown")

    logger.info("Filled missing contract information.")


# Clean text columns
    text_columns = [
        "title",
        "description",
        "company",
        "category"
    ]

    for column in text_columns:
        df[column] = (
            df[column]
            .fillna("")
            .astype(str)
            .str.strip()
        )

    logger.info("Standardized text columns.")

   
# Sort by date
    df = df.sort_values("created")


# Reset index
    df = df.reset_index(drop=True)


# Save cleaned dataset
    df.to_csv(ADZUNA_CLEAN, index=False)

    logger.info(f"Clean dataset saved to: {ADZUNA_CLEAN}")
    logger.info(f"Final dataset shape: {df.shape}")
    logger.info("Adzuna data cleaning completed successfully.")
    logger.info("=" * 60)

    return df


if __name__ == "__main__":
    clean_adzuna()

