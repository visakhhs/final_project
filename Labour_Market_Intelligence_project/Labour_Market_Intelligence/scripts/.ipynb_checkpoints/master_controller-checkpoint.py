from pathlib import Path
import subprocess
import sys
import importlib.util


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

SCRIPTS_DIR = PROJECT_ROOT / "scripts"
DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DIR = DATA_DIR / "processed"
OUTPUTS_DIR = PROJECT_ROOT / "scripts" / "outputs"
DEMO_CONTROLLER = SCRIPTS_DIR / "demo_controller.py"


# ============================================================
# DEMO CONTROLLER
# ============================================================

def run_demo():
    print("\nStarting random job demonstration...\n")

    if not DEMO_CONTROLLER.exists():
        print(f"ERROR: Demo controller not found:")
        print(DEMO_CONTROLLER)
        return

    cmd = [
        sys.executable,
        str(DEMO_CONTROLLER),
        "--mode", "DEMO",
        "--n", "10"
    ]

    result = subprocess.run(cmd, cwd=PROJECT_ROOT)

    if result.returncode != 0:
        print(
            f"\nDemo controller exited with code "
            f"{result.returncode}."
        )


# ============================================================
# LIVE LLM DEMONSTRATION
# ============================================================

def run_live():
    print("\nStarting live LLM demonstration...\n")
    print("This requires Ollama and Qwen to be running.\n")

    if not DEMO_CONTROLLER.exists():
        print(f"ERROR: Demo controller not found:")
        print(DEMO_CONTROLLER)
        return

    cmd = [
        sys.executable,
        str(DEMO_CONTROLLER),
        "--mode", "LIVE",
        "--n", "1"
    ]

    result = subprocess.run(cmd, cwd=PROJECT_ROOT)

    if result.returncode != 0:
        print(
            f"\nLive LLM demonstration exited with code "
            f"{result.returncode}."
        )


# ============================================================
# FIND NOTEBOOK
# ============================================================

def find_notebook(filename):
    direct_path = PROJECT_ROOT / filename

    if direct_path.exists():
        return direct_path

    matches = list(PROJECT_ROOT.rglob(filename))

    if matches:
        return matches[0]

    return None


# ============================================================
# CHECK N BCONVERT
# ============================================================

def nbconvert_available():
    return importlib.util.find_spec("nbconvert") is not None


# ============================================================
# EXECUTE NOTEBOOK
# ============================================================

def execute_notebook(notebook_path):

    if not nbconvert_available():
        print("\nERROR: nbconvert is not installed")
        print("\nInstall it using:")
        print()
        print(f'"{sys.executable}" -m pip install nbconvert')
        print()
        return False

    print("\n" + "=" * 60)
    print("EXECUTING NOTEBOOK")
    print("=" * 60)
    print()
    print(notebook_path)
    print()

    cmd = [
        sys.executable,
        "-m",
        "jupyter",
        "nbconvert",
        "--to", "notebook",
        "--execute",
        "--inplace",
        str(notebook_path)
    ]

    result = subprocess.run(
        cmd,
        cwd=PROJECT_ROOT
    )

    if result.returncode != 0:
        print()
        print(
            f"ERROR: Notebook failed with exit code "
            f"{result.returncode}"
        )
        return False

    print()
    print(f"Completed: {notebook_path.name}")

    return True

# ============================================================
# CREATE FINAL EXCEL WORKBOOK
# ============================================================

def create_final_excel_workbook():

    try:
        import pandas as pd
    except ImportError:
        print("\nERROR: pandas is not available.")
        return False

    try:
        from openpyxl import load_workbook
    except ImportError:
        print("\nERROR: openpyxl is not available.")
        print("\nInstall it using:")
        print(f'"{sys.executable}" -m pip install openpyxl')
        return False

    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    ANALYSIS_OUTPUTS_DIR = PROJECT_ROOT / "scripts" / "outputs"

    output_file = (
        OUTPUTS_DIR /
        "Labour_Market_Intelligence_Final_Results.xlsx"
    )

    # CSV outputs produced by the analysis stage
    csv_files = {
        "Industry Demand":
            OUTPUTS_DIR / "industry_demand.csv",

        "Salary Analysis":
            OUTPUTS_DIR / "adjusted_salary_by_industry.csv",

        "Experience Analysis":
            OUTPUTS_DIR / "experience_numeric_by_industry.csv",

        "Education Coverage":
            OUTPUTS_DIR / "education_coverage_by_industry.csv",

        "Technical Skills":
            OUTPUTS_DIR / "priority_technical_skills.csv",

        "Soft Skills":
            OUTPUTS_DIR / "priority_soft_skills.csv",

        "Skill Profile":
            OUTPUTS_DIR / "industry_skill_profile.csv",

        "Integrated Profile":
            OUTPUTS_DIR / "integrated_industry_profile.csv",

        "Validation":
            OUTPUTS_DIR / "key_findings_summary.csv"
    }

    print("\n" + "=" * 60)
    print("CREATING FINAL EXCEL WORKBOOK")
    print("=" * 60)

    written_sheets = 0

    with pd.ExcelWriter(
        output_file,
        engine="openpyxl"
    ) as writer:

        for sheet_name, csv_path in csv_files.items():

            if not csv_path.exists():
                print(
                    f"WARNING: Missing CSV - "
                    f"{csv_path.name}"
                )
                continue

            try:
                df = pd.read_csv(csv_path)

                df.to_excel(
                    writer,
                    sheet_name=sheet_name[:31],
                    index=False
                )

                print(
                    f"OK   | {sheet_name:<22} "
                    f"| {len(df):,} rows"
                )

                written_sheets += 1

            except Exception as exc:

                print(
                    f"ERROR | {sheet_name:<22} "
                    f"| {exc}"
                )

    if written_sheets == 0:

        print("\nERROR: No analysis CSV files were found.")
        return False

    print()
    print(
        f"Workbook created successfully:"
    )
    print(output_file)

    return True

    
# ============================================================
# ANALYTICS PIPELINE
# ============================================================

def run_analytics_pipeline():

    print("\n" + "=" * 60)
    print("STARTING ANALYTICS PIPELINE")
    print("=" * 60)

    print()
    print("Using existing processed labour-market data.")
    print()
    print("API collection will NOT be rerun.")
    print("Full 19,207-job LLM extraction will NOT be rerun.")
    print()

    input_file = (
        PROCESSED_DIR /
        "final_labour_market_refined.csv"
    )

    if not input_file.exists():

        print("ERROR: Final refined dataset not found:")
        print(input_file)

        return

    print("Input dataset found:")
    print(input_file)

    # --------------------------------------------------------
    # CURRENT FINAL ANALYSIS NOTEBOOK
    # --------------------------------------------------------

    notebook_11 = find_notebook(
        "11_refined_labour_market_analysis.ipynb"
    )

    if notebook_11 is None:

        print()
        print(
            "ERROR: 11_refined_labour_market_analysis.ipynb "
            "was not found."
        )

        return

    print()
    print("Final analysis notebook:")
    print(notebook_11)

    # --------------------------------------------------------
    # EXECUTE
    # --------------------------------------------------------

    success = execute_notebook(notebook_11)

    if not success:
        return

    # --------------------------------------------------------
    # CREATE FINAL EXCEL WORKBOOK
    # --------------------------------------------------------

    workbook_success = create_final_excel_workbook()

    if not workbook_success:
        print()
        print(
            "WARNING: Analysis completed, but the final "
            "Excel workbook could not be created."
        )

    # --------------------------------------------------------
    # FINAL STATUS
    # --------------------------------------------------------

    print()
    print("=" * 60)
    print("ANALYTICS PIPELINE COMPLETED")
    print("=" * 60)

    print()
    print("Analysis outputs:")
    print(OUTPUTS_DIR)

    print()
    print("Tableau data sources:")
    print(PROCESSED_DIR)

    print()
    print("Final Excel workbook:")

    workbook = (
        OUTPUTS_DIR /
        "Labour_Market_Intelligence_Final_Results.xlsx"
    )

    print(
        "READY | " + str(workbook)
        if workbook.exists()
        else "MISSING | " + str(workbook)
    )  
    

# ============================================================
# FILE STATUS
# ============================================================

def file_status(path):

    if not path.exists():
        return f"MISS | {path}"

    size_bytes = path.stat().st_size

    if size_bytes < 1024:
        size_text = f"{size_bytes} bytes"

    elif size_bytes < 1024 * 1024:
        size_text = f"{size_bytes / 1024:.1f} KB"

    else:
        size_text = f"{size_bytes / (1024 * 1024):.2f} MB"

    return f"OK   | {size_text} | {path}"


# ============================================================
# SYSTEM STATUS
# ============================================================

def run_system_status():

    print("\n" + "=" * 60)
    print("SYSTEM STATUS")
    print("=" * 60)

# --------------------------------------------------------
# CORE DATA
# --------------------------------------------------------

    print("\nCore processed datasets:")

    core_files = [

        PROCESSED_DIR /
        "master_jobs_llm.csv",

        PROCESSED_DIR /
        "final_labour_market_refined.csv"
    ]

    for path in core_files:
        print(file_status(path))

    # --------------------------------------------------------
    # TABLEAU
    # --------------------------------------------------------

    print("\nTableau data sources:")

    tableau_files = [

        PROCESSED_DIR /
        "tableau_technical_skill_pressure.csv",

        PROCESSED_DIR /
        "tableau_soft_skill_pressure.csv",

        PROCESSED_DIR /
        "tableau_combined_skill_pressure.csv",

        PROCESSED_DIR /
        "tableau_integrated_industry_profile.csv"
    ]

    for path in tableau_files:
        print(file_status(path))

    # --------------------------------------------------------
    # OUTPUTS
    # --------------------------------------------------------

    print("\nFinal analysis workbook:")

    print(
        file_status(
            OUTPUTS_DIR /
            "Labour_Market_Intelligence_Final_Results.xlsx"
        )
    )

    # --------------------------------------------------------
    # SCRIPTS
    # --------------------------------------------------------

    print("\nImportant scripts:")

    scripts = [

        SCRIPTS_DIR /
        "master_controller.py",

        SCRIPTS_DIR /
        "demo_controller.py"
    ]

    for path in scripts:
        print(file_status(path))

    # --------------------------------------------------------
    # PYTHON
    # --------------------------------------------------------

    print("\nPython environment:")

    print(f"Python executable:")
    print(sys.executable)

    print()
    print(
        "nbconvert: "
        + (
            "AVAILABLE"
            if nbconvert_available()
            else "MISSING"
        )
    )

    # --------------------------------------------------------
    # NOTE
    # --------------------------------------------------------

    print()
    print("Note:")
    print(
        "System status checks files and the Python environment."
    )
    print(
        "It does not verify Tableau Desktop or Ollama service state."
    )


# ============================================================
# MAIN MENU
# ============================================================

def main():

    while True:

        print()
        print("=" * 60)
        print("          LABOUR MARKET INTELLIGENCE SYSTEM")
        print("=" * 60)

        print()
        print("1. Random Job Demonstration")
        print("2. Live LLM Demonstration")
        print("3. Run Analytics Pipeline")
        print("4. System Status")
        print("5. Exit")

        print()

        choice = input(
            "Select option: "
        ).strip()

        if choice == "1":

            run_demo()

        elif choice == "2":

            run_live()

        elif choice == "3":

            run_analytics_pipeline()

        elif choice == "4":

            run_system_status()

        elif choice == "5":

            print()
            print(
                "Exiting Labour Market Intelligence System."
            )

            break

        else:

            print()
            print(
                "Invalid option. "
                "Please select 1, 2, 3, 4, or 5."
            )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()