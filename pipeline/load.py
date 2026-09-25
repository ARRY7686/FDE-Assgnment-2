import sqlite3
import pandas as pd
import json
from pathlib import Path

def load_data(raw_dir: Path, db_path: Path, logger=None):
    conn = sqlite3.connect(db_path)
    
    orders = pd.read_csv(raw_dir / "orders.csv")
    orders.to_sql("raw_orders", conn, if_exists="replace", index=False)
    
    events = pd.read_csv(raw_dir / "order_events.csv")
    events.to_sql("raw_events", conn, if_exists="replace", index=False)
    
    with open(raw_dir / "dispatch_data.json", "r") as f:
        api_data = json.load(f)
    if api_data:
        pd.DataFrame(api_data).to_sql("raw_dispatch", conn, if_exists="replace", index=False)
    
    conn.close()
