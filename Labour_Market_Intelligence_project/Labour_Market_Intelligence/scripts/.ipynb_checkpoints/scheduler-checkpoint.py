"""Daily scheduler for the Labour Market Intelligence prototype."""
from __future__ import annotations
import os, subprocess, sys, time
from datetime import datetime
from pathlib import Path
PROJECT_ROOT=Path(__file__).resolve().parents[1]
os.chdir(PROJECT_ROOT)
try:
    from config import SCHEDULER_TIME
except Exception:
    SCHEDULER_TIME="08:00"
TARGET_HOUR,TARGET_MINUTE=map(int,SCHEDULER_TIME.split(":"))

def run_update():
    print(f"\nSCHEDULED PIPELINE STARTED: {datetime.now():%Y-%m-%d %H:%M:%S}")
    subprocess.run([sys.executable,str(PROJECT_ROOT/"controllers"/"full_pipeline_controller.py"),"--mode","update"],cwd=PROJECT_ROOT,check=True)
    print(f"SCHEDULED PIPELINE FINISHED: {datetime.now():%Y-%m-%d %H:%M:%S}")

def main():
    print("LABOUR MARKET INTELLIGENCE — DAILY SCHEDULER")
    print(f"Configured run time: {TARGET_HOUR:02d}:{TARGET_MINUTE:02d}")
    print("Waiting... Press Ctrl+C to stop.")
    last_run_date=None
    while True:
        now=datetime.now()
        if now.hour==TARGET_HOUR and now.minute==TARGET_MINUTE and last_run_date!=now.date():
            try: run_update()
            except Exception as exc: print(f"Scheduled pipeline error: {exc}")
            last_run_date=now.date()
        time.sleep(20)
if __name__=="__main__": main()
