def build_dashboard_html(metrics: dict) -> str:
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>FlashEats Dashboard</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .metric {{ font-size: 24px; font-weight: bold; color: #333; }}
            .card {{ border: 1px solid #ccc; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <h1>FlashEats Operations Dashboard</h1>
        
        <div class="card">
            <h3>Total Delivered Orders</h3>
            <p class="metric">{metrics.get('total_delivered', 0)}</p>
        </div>
        
        <div class="card">
            <h3>Late Deliveries (%)</h3>
            <p class="metric">{metrics.get('late_pct', 0):.2f}%</p>
        </div>
        
        <div class="card">
            <h3>Average Delay (mins)</h3>
            <p class="metric">{metrics.get('avg_delay_mins', 0):.2f}</p>
        </div>
        
    </body>
    </html>
    """
    return html
