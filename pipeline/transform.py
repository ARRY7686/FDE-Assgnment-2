import sqlite3
from pathlib import Path

def run_transform(db_path: Path, logger=None):
    conn = sqlite3.connect(db_path)
    
    # Example transformation: clean orders and join events
    conn.execute("DROP TABLE IF EXISTS fct_orders;")
    
    conn.execute("""
    CREATE TABLE fct_orders AS
    SELECT 
        o.order_id,
        o.promised_eta,
        o.actual_delivery_at,
        CASE 
            WHEN LOWER(o.final_status) = 'delivered' THEN 1 ELSE 0 
        END as is_delivered
    FROM raw_orders o
    WHERE LOWER(o.final_status) = 'delivered';
    """)
    
    conn.commit()
    conn.close()
