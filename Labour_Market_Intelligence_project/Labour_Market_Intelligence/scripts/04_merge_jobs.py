# Merge cleaned Adzuna and Reed datasets into a single master dataset with a common schema.
import uuid
import pandas as pd

from config import (
    ADZUNA_CLEAN,
    REED_CLEAN,
    MASTER_DATASET
)

from logger import logger


def merge_jobs():

    logger.info("=" * 70)
    logger.info("STARTING DATASET MERGE")
    logger.info("=" * 70)

    
# Load datasets
    adzuna = pd.read_csv(ADZUNA_CLEAN)
    reed = pd.read_csv(REED_CLEAN)

    logger.info(f"Loaded Adzuna: {adzuna.shape}")
    logger.info(f"Loaded Reed: {reed.shape}")

    
# Rename Adzuna columns
    adzuna = adzuna.rename(columns={
        "id": "source_id",
        "title": "title",
        "company": "company",
        "location": "location",
        "description": "description",
        "salary_min": "salary_min",
        "salary_max": "salary_max",
        "salary_avg": "salary_avg",
        "created": "created",
        "contract_type": "contract_type",
        "contract_time": "contract_time",
        "redirect_url": "url"
    })

  
# Rename Reed columns
    reed = reed.rename(columns={
        "jobId": "source_id",
        "jobTitle": "title",
        "employerName": "company",
        "locationName": "location",
        "jobDescription": "description",
        "minimumSalary": "salary_min",
        "maximumSalary": "salary_max",
        "date": "created",
        "jobUrl": "url"
    })

# Add missing columns
    reed["contract_type"] = "Unknown"
    reed["contract_time"] = "Unknown"

    
# Standardize datetime
    adzuna["created"] = (
        pd.to_datetime(
            adzuna["created"],
            utc=True,
            errors="coerce"
        )
        .dt.tz_localize(None)
    )

    reed["created"] = pd.to_datetime(
        reed["created"],
        format="%d/%m/%Y",
        errors="coerce"
    )

# Source column
    adzuna["source"] = "Adzuna"
    reed["source"] = "Reed"
 
# Common schema
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
        "source"
    ]

    adzuna = adzuna[columns]
    reed = reed[columns]


# Merge
    master = pd.concat(
        [adzuna, reed],
        ignore_index=True
    )

    logger.info(f"Merged dataset: {master.shape}")


# Remove incomplete rows
    before = len(master)

    master = master.dropna(
        subset=[
            "title",
            "company",
            "location",
            "description",
            "created"
        ]
    )

    logger.info(
        f"Rows removed (missing required fields): {before-len(master)}"
    )


# Remove duplicates
    before = len(master)

    master = master.drop_duplicates(
        subset=[
            "title",
            "company",
            "location",
            "created"
        ]
    )

    duplicates_removed = before - len(master)

    logger.info(f"Duplicate jobs removed: {duplicates_removed}")


# Create internal Job ID
    master.insert(
        0,
        "job_id",
        [str(uuid.uuid4()) for _ in range(len(master))]
    )

    logger.info("Generated internal job IDs.")


 # Sort
    master = master.sort_values(
        by="created",
        ascending=False
    ).reset_index(drop=True)


 # Statistics
    logger.info("-" * 50)
    logger.info("MERGE SUMMARY")
    logger.info("-" * 50)

    logger.info(f"Total Jobs: {len(master):,}")

    logger.info(
        f"Adzuna Jobs: {(master['source']=='Adzuna').sum():,}"
    )

    logger.info(
        f"Reed Jobs: {(master['source']=='Reed').sum():,}"
    )

    logger.info(
        f"Average Salary Available: {master['salary_avg'].notna().sum():,}"
    )

    logger.info(
        f"Jobs without salary: {master['salary_avg'].isna().sum():,}"
    )

    logger.info(
        f"Date Range: {master['created'].min()} -> {master['created'].max()}"
    )

    logger.info("-" * 50)


# Save the dataset
    master.to_csv(
        MASTER_DATASET,
        index=False
    )

    logger.info(f"Master dataset saved to:\n{MASTER_DATASET}")

    logger.info(f"Final Shape: {master.shape}")

    logger.info("=" * 70)
    logger.info("MERGE COMPLETED SUCCESSFULLY")
    logger.info("=" * 70)

    return master


if __name__ == "__main__":
    merge_jobs()