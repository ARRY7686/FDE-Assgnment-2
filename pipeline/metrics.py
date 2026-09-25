import sqlite3
import pandas as pd
from pathlib import Path

def run_metrics(db_path: Path, logger=None):
    conn = sqlite3.connect(db_path)
    
    df = pd.read_sql("SELECT * FROM fct_orders", conn)
    
    df['promised_eta'] = pd.to_datetime(df['promised_eta'], format='ISO8601')
    df['actual_delivery_at'] = pd.to_datetime(df['actual_delivery_at'], format='ISO8601')
    df['delay_minutes'] = (df['actual_delivery_at'] - df['promised_eta']).dt.total_seconds() / 60.0
    
    late_orders = (df['delay_minutes'] > 0).sum()
    total = len(df)
    
    metrics = {
        "total_delivered": int(total),
        "late_pct": float(late_orders / total * 100) if total > 0 else 0.0,
        "avg_delay_mins": float(df.loc[df['delay_minutes'] > 0, 'delay_minutes'].mean()) if late_orders > 0 else 0.0
    }
    
    conn.close()
    return metrics
