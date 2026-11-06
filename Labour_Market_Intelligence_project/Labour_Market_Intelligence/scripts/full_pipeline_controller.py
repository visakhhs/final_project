"""Central controller for the Labour Market Intelligence prototype."""
from __future__ import annotations
import argparse, os, time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
os.chdir(PROJECT_ROOT)

STAGES = {
    "collection": ["01_adzuna API (3).ipynb", "02_reed API (1).ipynb"],
    "updates": ["01.1_adzuna_updater.ipynb", "02.1_reed_updater.ipynb"],
    "analysis": [
        "03_nlp_preprocessing.py",
        "05_Industry_classifier.ipynb",
        "06_improved_industry_classifier (2).ipynb",
        "07_llm_skill_extraction.ipynb",
        "08_Merge and validation.ipynb",
        "09_skill_normalisation.ipynb",
        "10_labour_market_analysis (1).ipynb",
        "11_refined_labour_market_analysis.ipynb",
    ],
}

def run_notebook(path: Path, stage: str) -> None:
    import nbformat
    from nbconvert.preprocessors import ExecutePreprocessor
    print("\n" + "="*78)
    print(f"RUNNING: {stage} | {path.name}")
    print("="*78)
    with path.open("r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)
    ep = ExecutePreprocessor(timeout=-1, kernel_name="python3", allow_errors=False)
    ep.preprocess(nb, {"metadata": {"path": str(PROJECT_ROOT)}})
    outdir = PROJECT_ROOT / "outputs" / "executed_notebooks"
    outdir.mkdir(parents=True, exist_ok=True)
    with (outdir / path.name).open("w", encoding="utf-8") as f:
        nbformat.write(nb, f)
    print(f"COMPLETED: {path.name}")

def run_stage(name: str) -> None:
    for filename in STAGES[name]:
        path = PROJECT_ROOT / filename
        if not path.exists():
            raise FileNotFoundError(f"Pipeline file not found: {path}")
        run_notebook(path, name)

def validate_outputs() -> None:
    import pandas as pd
    p = PROJECT_ROOT / "data" / "processed"
    required = [
        "master_jobs.csv", "master_jobs_nlp.csv", "master_jobs_industry.csv",
        "master_jobs_industry_improved.csv", "master_jobs_llm.csv",
        "final_labour_market_dataset.csv", "final_labour_market_normalized.csv",
        "final_labour_market_refined.csv", "tableau_technical_skill_pressure.csv",
        "tableau_soft_skill_pressure.csv", "tableau_combined_skill_pressure.csv",
        "tableau_integrated_industry_profile.csv",
    ]
    missing = [str(p / x) for x in required if not (p / x).exists()]
    if missing:
        raise RuntimeError("Required outputs missing:\n" + "\n".join(missing))
    final = pd.read_csv(p / "final_labour_market_refined.csv")
    print("\nPIPELINE VALIDATION")
    print(f"Final rows       : {len(final):,}")
    print(f"Final columns    : {len(final.columns):,}")
    print(f"Missing job IDs  : {final['job_id'].isna().sum():,}")
    print(f"Duplicate IDs    : {final['job_id'].duplicated().sum():,}")
    print("Tableau outputs  : OK")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["existing", "update", "rebuild"], default="existing")
    args = parser.parse_args()
    start = time.time()
    print("LABOUR MARKET INTELLIGENCE — FULL PIPELINE CONTROLLER")
    print(f"Mode: {args.mode}")
    if args.mode == "rebuild":
        run_stage("collection")
    elif args.mode == "update":
        run_stage("updates")
    run_stage("analysis")
    validate_outputs()
    print(f"\nFULL PIPELINE COMPLETED in {(time.time()-start)/60:.1f} minutes.")

if __name__ == "__main__":
    main()
