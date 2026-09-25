import json
from pathlib import Path

def save_outputs(run_id: str, metrics: dict, dashboard_html: str, logger=None):
    out_dir = Path(f"outputs/run_{run_id}")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    with open(out_dir / "metrics.json", "w") as f:
        json.dump(metrics, f, indent=4)
        
    with open(out_dir / "dashboard.html", "w") as f:
        f.write(dashboard_html)
        
    return out_dir
