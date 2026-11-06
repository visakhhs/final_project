import os
from pathlib import Path

# PROJECT ROOT

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# FOLDERS

DATA_FOLDER = PROJECT_ROOT / "data"

RAW_FOLDER = DATA_FOLDER / "raw"
PROCESSED_FOLDER = DATA_FOLDER / "processed"

RAW_FOLDER.mkdir(parents=True, exist_ok=True)
PROCESSED_FOLDER.mkdir(parents=True, exist_ok=True)

ADZUNA_FOLDER = RAW_FOLDER / "adzuna"
REED_FOLDER = RAW_FOLDER / "reed"

LOG_FOLDER = PROJECT_ROOT / "logs"

OUTPUT_FOLDER = PROJECT_ROOT / "outputs"
REPORT_FOLDER = OUTPUT_FOLDER / "reports"
FIGURE_FOLDER = OUTPUT_FOLDER / "figures"

MODEL_FOLDER = PROJECT_ROOT / "models"

# CREATE FOLDERS IF THEY DON'T EXIST

FOLDERS = [
    DATA_FOLDER,
    RAW_FOLDER,
    PROCESSED_FOLDER,
    ADZUNA_FOLDER,
    REED_FOLDER,
    LOG_FOLDER,
    OUTPUT_FOLDER,
    REPORT_FOLDER,
    FIGURE_FOLDER,
    MODEL_FOLDER,
]

for folder in FOLDERS:
    folder.mkdir(parents=True, exist_ok=True)

# RAW DATA FILES

ADZUNA_CSV = ADZUNA_FOLDER / "adzuna_jobs.csv"

REED_CSV = REED_FOLDER / "reed_jobs.csv"

ADZUNA_FOLDER.mkdir(parents=True, exist_ok=True)
REED_FOLDER.mkdir(parents=True, exist_ok=True)

# Incoming data downloaded by updater scripts

LATEST_ADZUNA = ADZUNA_FOLDER / "incoming_adzuna.csv"
LATEST_REED = REED_FOLDER / "incoming_reed.csv"

MASTER_FILE = PROCESSED_FOLDER / "master_jobs.csv"

# PROCESSED FILES

ADZUNA_CLEAN = PROCESSED_FOLDER / "adzuna_clean.csv"

REED_CLEAN = PROCESSED_FOLDER / "reed_clean.csv"

MASTER_DATASET = PROCESSED_FOLDER / "master_jobs.csv"

# OUTPUT FILES

SKILLS_DATASET = OUTPUT_FOLDER / "skills.csv"

ENTITIES_DATASET = OUTPUT_FOLDER / "entities.csv"


# LOG FILE

LOG_FILE = LOG_FOLDER / "project.log"

# ADZUNA API SETTINGS

APP_ID = "ff1db3d5"

APP_KEY = "8f82686b308b995e71896278c8ec5884"

COUNTRY = "gb"

RESULTS_PER_PAGE = 50
UPDATE_PAGES = 5

REQUEST_TIMEOUT = 30
COUNTRY = "gb"

RESULTS_PER_PAGE = 50

UPDATE_PAGES = 5

REQUEST_TIMEOUT = 30

# REED API SETTINGS

REED_API_KEY = "5ca6123b-b48b-4d3f-9f75-2b34e8aa2217"

# PROJECT SETTINGS

RANDOM_STATE = 42

SCHEDULER_TIME = "08:00"