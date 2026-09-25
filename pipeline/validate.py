import pandas as pd
from pathlib import Path

def run_validation(raw_dir: Path, logger=None):
    orders = pd.read_csv(raw_dir / "orders.csv")
    events = pd.read_csv(raw_dir / "order_events.csv")
    
    report = {
        "overall_status": "PASS",
        "checks": []
    }
    
    if len(orders) == 0:
        report["overall_status"] = "FAIL"
        report["checks"].append({"rule_id": "V01", "severity": "FAIL", "msg": "No orders found."})
        
    return report
