"""Live Qwen demonstration on 1–20 existing job postings."""
from __future__ import annotations
import argparse, json, os
from pathlib import Path
import pandas as pd
import ollama
import random

PROJECT_ROOT = Path(__file__).resolve().parents[1]
os.chdir(PROJECT_ROOT)
INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "final_labour_market_refined.csv"
OUTPUT_DIR = PROJECT_ROOT / "data" / "demo"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
MODEL = "qwen2.5:7b"

DEFAULT = {"technical_skills":[],"soft_skills":[],"tools_and_technologies":[],"certifications":[],"licenses":[],"education_required":"","experience_required":"","languages":[]}
PROMPT = '''You are an expert Labour Market Intelligence information extraction system.
Analyse ONE UK job advertisement. Extract ONLY information explicitly stated in the job title or job description.
Return ONLY valid JSON. Do not use Markdown. Do not explain anything. Do not invent information.
If information is missing, use [] for list fields and "" for text fields.

TECHNICAL SKILLS: professional or job-specific capabilities.
SOFT SKILLS: interpersonal or behavioural competencies.
TOOLS AND TECHNOLOGIES: specific software, programming languages, databases, platforms, technologies or technical equipment.
CERTIFICATIONS: formal certificates or qualifications.
LICENSES: professional, legal or occupational licences.
EDUCATION: explicit educational requirements.
EXPERIENCE: explicit previous experience requirements.
LANGUAGES: languages explicitly required or preferred. Do not assume English.

Return EXACTLY this JSON:
{"technical_skills": [], "soft_skills": [], "tools_and_technologies": [], "certifications": [], "licenses": [], "education_required": "", "experience_required": "", "languages": []}

JOB TITLE:
{title}

JOB DESCRIPTION:
{description}'''

def clean_result(result):
    result = {**DEFAULT, **(result or {})}
    invalid = {"", "none", "none mentioned", "not specified", "unknown", "n/a", "no specific tools mentioned"}
    fields = ["technical_skills","soft_skills","tools_and_technologies","certifications","licenses","languages"]
    for field in fields:
        values = result.get(field, [])
        if not isinstance(values, list): values = []
        result[field] = list(dict.fromkeys(str(x).strip() for x in values if str(x).strip().lower() not in invalid))
    result["soft_skills"] = [x for x in result["soft_skills"] if x.lower() not in {"friendly","caring","passionate","lively","enthusiastic","dedicated","helpful"}]
    tools, kept = result["tools_and_technologies"], []
    for item in tools:
        low = item.lower()
        if "certificate" in low or "nvq" in low or "acca" in low:
            if item not in result["certifications"]: result["certifications"].append(item)
        elif any(x in low for x in ["driving licence","driving license","sia licence","cscs","ecs card","licence"]):
            if item not in result["licenses"]: result["licenses"].append(item)
        else: kept.append(item)
    result["tools_and_technologies"] = [x for x in kept if x.lower() not in {"vehicle","equipment","computer","office"}]
    return result

def extract(title, description):

    prompt = PROMPT.replace(
        "{title}",
        str(title)
    ).replace(
        "{description}",
        str(description)[:2500]
    )

    r = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    text = (
        r["message"]["content"]
        .strip()
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        print("WARNING: Qwen returned invalid JSON.")
        print("Raw response:")
        print(text)
        return DEFAULT.copy()

    if not isinstance(parsed, dict):
        print("WARNING: Qwen returned JSON, but not a JSON object.")
        return DEFAULT.copy()

    return clean_result(parsed)
    
def run_live(df, n, seed):
    """Run Qwen on a small number of selected jobs."""
    if not 1 <= n <= 3:
        raise ValueError("LIVE mode allows 1–3 jobs to keep the demonstration lightweight.")

    sample = df.sample(
    n=min(n, len(df)),
    random_state=random.SystemRandom().randint(0, 2**32 - 1)
    ).reset_index(drop=True)
    results = []

    print("LABOUR MARKET INTELLIGENCE — LIVE LLM DEMONSTRATION")
    print(f"Model: {MODEL} | Jobs: {len(sample)}")
    print("LIVE mode uses Ollama/Qwen for the selected jobs only.")

    for i, row in sample.iterrows():
        print(f"\n[{i+1}/{len(sample)}] {row['title']}")
        result = extract(row["title"], row["description_clean"])
        results.append({
            "job_id": row["job_id"],
            "title": row["title"],
            "industry_refined": row.get("industry_refined", ""),
            **result
        })
        print(json.dumps(result, indent=2, ensure_ascii=False))

    out = OUTPUT_DIR / "live_llm_results.csv"
    pd.DataFrame(results).to_csv(out, index=False, encoding="utf-8-sig")
    print(f"\nLive results saved to: {out}")
    print("Research dataset was not modified.")


def run_demo(n):
    """Fast demonstration using the existing LLM-enriched dataset."""

    if not 1 <= n <= 20:
        raise ValueError("DEMO mode allows between 1 and 20 jobs.")

    llm_file = PROJECT_ROOT / "data" / "processed" / "master_jobs_llm.csv"

    if not llm_file.exists():
        raise FileNotFoundError(
            f"Existing LLM dataset not found: {llm_file}"
        )

    df = pd.read_csv(llm_file)

    required_columns = [
        "job_id", "title", "industry", "status",
        "technical_skills", "soft_skills", "tools_and_technologies",
        "certifications", "licenses", "education_required",
        "experience_required", "languages"
    ]

    missing = [c for c in required_columns if c not in df.columns]
    if missing:
        raise ValueError(
            f"master_jobs_llm.csv is missing columns: {missing}"
        )

    # Fresh random sample on every execution.
    sample = df.sample(
        n=min(n, len(df))
    ).reset_index(drop=True)

    out = OUTPUT_DIR / "fast_demo_results.csv"
    sample.to_csv(out, index=False, encoding="utf-8-sig")

    print()
    print("=" * 70)
    print("LABOUR MARKET INTELLIGENCE — FAST DEMONSTRATION")
    print("=" * 70)
    print(f"Source dataset : {llm_file}")
    print(f"Jobs selected  : {len(sample)}")
    print("Ollama called  : NO")
    print(f"Output saved   : {out}")
    print("=" * 70)

    print("\nSELECTED JOBS\n")

    for i, row in sample.iterrows():
        print(f"[{i + 1}/{len(sample)}] {row['title']}")
        print(f"Industry: {row['industry']}")
        print(f"Technical skills: {row['technical_skills']}")
        print(f"Soft skills: {row['soft_skills']}")
        print(f"Tools & technologies: {row['tools_and_technologies']}")
        print(f"Education: {row['education_required']}")
        print(f"Experience: {row['experience_required']}")
        print(f"Languages: {row['languages']}")
        print("-" * 70)

def main():
    parser = argparse.ArgumentParser(
        description="Labour Market Intelligence LLM demonstration controller."
    )
    parser.add_argument(
        "--mode",
        choices=["DEMO", "LIVE"],
        default="DEMO",
        help="DEMO = fast existing LLM results; LIVE = call local Qwen/Ollama."
    )
    parser.add_argument(
        "--n",
        type=int,
        default=10,
        help="Number of jobs. DEMO: 1–20; LIVE: 1–3."
    )
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    if args.mode == "DEMO":
        run_demo(args.n)
    else:
        df = pd.read_csv(INPUT_FILE)

        required = ["job_id", "title", "description_clean"]
        missing = [c for c in required if c not in df.columns]
        if missing:
            raise ValueError(f"Missing columns: {missing}")

        run_live(df, args.n, args.seed)


if __name__ == "__main__":
    main()
