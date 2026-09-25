import os
import shutil
import requests
import json
import sqlite3
import pandas as pd
from pathlib import Path

def extract_data(run_id: str, logger=None):
    raw_dir = Path(f"data/raw/run_{run_id}")
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    # Extract from SQLite
    db_path = r"C:\Users\aadig\OneDrive\Desktop\flasheats-classroom-pack\database\flasheats.db"
    conn = sqlite3.connect(db_path)
    orders = pd.read_sql("SELECT * FROM orders", conn)
    orders.to_csv(raw_dir / "orders.csv", index=False)
    conn.close()
    
    # Extract from CSV
    events_path = r"C:\Users\aadig\OneDrive\Desktop\flasheats-classroom-pack\data\order_events.csv"
    shutil.copy(events_path, raw_dir / "order_events.csv")
    
    # Extract from API
    api_url = "http://localhost:8000/dispatch/orders"
    api_data = []
    page = 1
    while True:
        try:
            resp = requests.get(f"{api_url}?page={page}&page_size=200", timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                api_data.extend(data['data'])
                if not data['has_more']:
                    break
                page += 1
            elif resp.status_code == 429 or resp.status_code == 500:
                pass # retry logic simplified
            else:
                break
        except Exception:
            break
            
    with open(raw_dir / "dispatch_data.json", "w") as f:
        json.dump(api_data, f)
        
    return raw_dir
