import pandas as pd

from logger import logger
from config import (
    REED_CSV,
    REED_CLEAN,
)


def clean_reed():

    logger.info("=" * 60)
    logger.info("Cleaning Reed dataset...")
    logger.info("=" * 60)


# Load dataset
    df = pd.read_csv(REED_CSV)

    logger.info(f"Loaded {len(df)} Reed jobs.")


# Remove duplicate jobs
    before = len(df)

    df.drop_duplicates(
        subset="jobId",
        inplace=True
    )

    logger.info(
        f"Removed {before - len(df)} duplicate jobs."
    )


# Rename columns to match Adzuna schema
    df.rename(
    columns={
        "locationName": "location",
        "date": "created",
        "jobId": "source_id",
        "minimumSalary": "salary_min",
        "maximumSalary": "salary_max",
        "jobDescription": "description",
        "jobTitle": "title",
        "employerName": "company",
        "jobUrl": "url",
    },
    inplace=True,
)

# Convert salary columns to numeric
    df["salary_min"] = pd.to_numeric(
        df["salary_min"],
        errors="coerce"
    )

    df["salary_max"] = pd.to_numeric(
        df["salary_max"],
        errors="coerce"
    )


# Calculate average salary
    df["salary_avg"] = (
        df["salary_min"] +
        df["salary_max"]
    ) / 2


# Create missing Adzuna columns
    df["longitude"] = None
    df["latitude"] = None
    df["adref"] = None
    df["salary_is_predicted"] = None

# Use Reed as the source label
    df["source"] = "Reed"
    
# Reed Search API doesn't provide these fields
    df["contract_type"] = None
    df["contract_time"] = None
    df["category"] = None


# Fill missing text values
    text_columns = [
    "location",
    "description",
    "title",
    "company",
    "url",
]
    
    for column in text_columns:
        df[column] = df[column].fillna("Unknown")


# Reorder columns
    columns = [
    "source_id",
    "title",
    "company",
    "location",
    "description",
    "salary_min",
    "salary_max",
    "salary_avg",
    "created",
    "contract_type",
    "contract_time",
    "url",
    "source",
]
    df = df[columns]


# Save cleaned dataset
    df.to_csv(REED_CLEAN, index=False)

    logger.info(
        f"Saved {len(df)} cleaned Reed jobs to {REED_CLEAN}"
    )

    logger.info("=" * 60)
    logger.info("Reed cleaning completed.")
    logger.info("=" * 60)


if __name__ == "__main__":
    clean_reed()