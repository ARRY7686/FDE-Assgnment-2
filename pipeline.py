import sqlite3
import pandas as pd
import requests
import time
import json
import os

# 1. RETRIEVE DATA
def get_orders_db(db_path):
    print("Retrieving from SQLite...")
    conn = sqlite3.connect(db_path)
    df = pd.read_sql("SELECT * FROM orders", conn)
    conn.close()
    return df

def get_events_csv(csv_path):
    print("Retrieving from CSV...")
    return pd.read_csv(csv_path)

def get_dispatch_api(api_url):
    print("Retrieving from API...")
    orders = []
    page = 1
    while True:
        try:
            resp = requests.get(f"{api_url}?page={page}&page_size=50")
            if resp.status_code == 200:
                data = resp.json()
                orders.extend(data['data'])
                if not data['has_more']:
                    break
                page += 1
            elif resp.status_code == 429:
                print("Rate limited. Retrying...")
                time.sleep(2)
            elif resp.status_code == 500:
                print("Server error. Retrying...")
                time.sleep(2)
            else:
                print(f"Failed with {resp.status_code}")
                break
        except Exception as e:
            print(f"API Error: {e}")
            break
    return pd.DataFrame(orders)

# 2. PROFILE & VALIDATE
def validate_and_clean_orders(orders_df):
    orders_df['created_at'] = pd.to_datetime(orders_df['created_at'], format='ISO8601')
    orders_df['promised_eta'] = pd.to_datetime(orders_df['promised_eta'], format='ISO8601')
    orders_df['pickup_at'] = pd.to_datetime(orders_df['pickup_at'], format='ISO8601')
    orders_df['actual_delivery_at'] = pd.to_datetime(orders_df['actual_delivery_at'], format='ISO8601')
    
    # Validation assumption: Exclude cancelled orders, only look at DELIVERED
    clean_orders = orders_df[orders_df['final_status'].str.lower() == 'delivered'].copy()
    
    return clean_orders

def validate_and_clean_events(events_df):
    events_df['event_time'] = pd.to_datetime(events_df['event_time'], format='ISO8601')
    return events_df

# 3. MODEL WORKFLOW & METRICS
def model_workflow(orders_df, events_df, api_df):
    # Calculate order lateness
    orders_df['delay_minutes'] = (orders_df['actual_delivery_at'] - orders_df['promised_eta']).dt.total_seconds() / 60.0
    orders_df['is_late'] = orders_df['delay_minutes'] > 0
    
    # Calculate stage times from events
    events_pivot = events_df.pivot_table(index='order_id', columns='event_type', values='event_time', aggfunc='first').reset_index()
    
    if 'ORDER_CREATED' in events_pivot.columns and 'PICKED_UP' in events_pivot.columns:
        events_pivot['prep_and_wait_time'] = (events_pivot['PICKED_UP'] - events_pivot['ORDER_CREATED']).dt.total_seconds() / 60.0
    if 'PICKED_UP' in events_pivot.columns and 'DELIVERED' in events_pivot.columns:
        events_pivot['travel_time'] = (events_pivot['DELIVERED'] - events_pivot['PICKED_UP']).dt.total_seconds() / 60.0
        
    merged = pd.merge(orders_df, events_pivot, on='order_id', how='left')
    
    if not api_df.empty:
        api_df['is_reassigned'] = api_df['reassigned_at'].notna()
        api_df_subset = api_df[['order_id', 'is_reassigned', 'estimated_pickup_at']]
        merged = pd.merge(merged, api_df_subset, on='order_id', how='left')
        
    return merged

def calculate_metrics(merged_df):
    total_delivered = len(merged_df)
    late_orders = merged_df['is_late'].sum()
    late_pct = (late_orders / total_delivered) * 100 if total_delivered > 0 else 0
    avg_delay = merged_df.loc[merged_df['is_late'], 'delay_minutes'].mean() if late_orders > 0 else 0
    
    print(f"Total Delivered Orders: {total_delivered}")
    print(f"Late Orders: {late_orders} ({late_pct:.2f}%)")
    print(f"Avg Delay (minutes) for late orders: {avg_delay:.2f}")
    
    avg_prep = merged_df['prep_and_wait_time'].mean()
    avg_travel = merged_df['travel_time'].mean()
    print(f"Average Prep & Wait Time: {avg_prep:.2f} mins")
    print(f"Average Travel Time: {avg_travel:.2f} mins")
    
    return {
        'total_delivered': int(total_delivered),
        'late_orders': int(late_orders),
        'late_pct': float(late_pct),
        'avg_delay_mins': float(avg_delay),
        'avg_prep_wait_mins': float(avg_prep),
        'avg_travel_mins': float(avg_travel)
    }

def run_pipeline():
    db_path = r'C:\Users\aadig\OneDrive\Desktop\flasheats-classroom-pack\database\flasheats.db'
    events_path = r'C:\Users\aadig\OneDrive\Desktop\flasheats-classroom-pack\data\order_events.csv'
    api_url = 'http://localhost:8000/dispatch/orders'
    
    orders = get_orders_db(db_path)
    events = get_events_csv(events_path)
    api_data = get_dispatch_api(api_url)
    
    clean_orders = validate_and_clean_orders(orders)
    clean_events = validate_and_clean_events(events)
    
    workflow_df = model_workflow(clean_orders, clean_events, api_data)
    workflow_df.to_csv('analytical_dataset.csv', index=False)
    
    print("\nMetrics:")
    metrics = calculate_metrics(workflow_df)
    
    with open('metrics.json', 'w') as f:
        json.dump(metrics, f, indent=4)

if __name__ == '__main__':
    run_pipeline()
