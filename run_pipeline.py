import time
from pathlib import Path

from pipeline.extract import extract_data
from pipeline.validate import run_validation
from pipeline.load import load_data
from pipeline.transform import run_transform
from pipeline.metrics import run_metrics
from pipeline.report import build_dashboard_html
from pipeline.save import save_outputs

def run():
    run_id = str(int(time.time()))
    db_path = Path(f"data/processed/flasheats_warehouse.db")
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Starting run {run_id}...")
    
    # Extract
    print("Extracting data...")
    raw_dir = extract_data(run_id)
    
    # Validate
    print("Validating data...")
    report = run_validation(raw_dir)
    if report["overall_status"] == "FAIL":
        print(f"Validation failed: {report['checks']}")
        return
        
    # Load
    print("Loading data...")
    load_data(raw_dir, db_path)
    
    # Transform
    print("Transforming data...")
    run_transform(db_path)
    
    # Metrics
    print("Calculating metrics...")
    metrics = run_metrics(db_path)
    
    # Report
    print("Building report...")
    dashboard_html = build_dashboard_html(metrics)
    
    # Save
    print("Saving outputs...")
    out_dir = save_outputs(run_id, metrics, dashboard_html)
    
    print(f"Done! Outputs saved to {out_dir}")

if __name__ == "__main__":
    run()
