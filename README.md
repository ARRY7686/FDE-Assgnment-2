# FlashEats Late Delivery Analysis

## Problem Statement
Leadership has identified a business problem where "Late deliveries are hurting customer experience." The operational data across different systems is fragmented, making it hard to see a clear picture. Customers claim that delivery times are unreliable, and leadership wants an actionable data pipeline to understand the delays before investing in a new AI delay-prediction system. 

## Users & Stakeholders
- **Operations Team**: Needs to understand where bottlenecks occur (prep vs. travel) to target interventions.
- **Leadership / Executive Team**: Needs dependable metrics to decide whether an AI delay-prediction system is worth the investment or if simpler operational changes can fix the issue.
- **Customers**: Ultimately affected by late deliveries and inaccurate ETA predictions.

## Project KPI
- **Percentage of Late Deliveries**: The primary metric measuring how often orders exceed their promised ETA.
- **Average Delay (in minutes)**: The severity of the late deliveries.
- **Average Prep & Wait Time / Average Travel Time**: Secondary metrics helping diagnose *where* the delay happens.

## Source Overview
- **SQLite Database (`flasheats.db`)**: Contains core entities like `orders`, `customers`, `restaurants`, and `drivers`.
- **Event Logs (CSV)**: `order_events.csv` provides timestamped workflow events (`ORDER_CREATED`, `PICKED_UP`, `DELIVERED`).
- **Dispatch API**: A mock API service (`/dispatch/orders`) that returns dispatcher information, such as driver reassignment and estimated pickup times, complete with pagination and intermittent errors.

## Setup & Run Instructions
1. **Prerequisites**: Python 3.8+, `pip`.
2. **Install Dependencies**:
   ```bash
   pip install pandas requests
   ```
3. **Start the Mock API** (run in a separate terminal):
   ```bash
   python /path/to/flasheats-classroom-pack/api/mock_dispatch_api.py
   ```
4. **Run the Pipeline**:
   ```bash
   python pipeline.py
   ```
5. **Output**: The script will output metrics to the console, save an `analytical_dataset.csv` for dashboarding, and dump metrics to `metrics.json`.

## Supported Decisions
This output allows Operations to definitively see whether delays happen mostly in the kitchen (prep and wait time) or on the road (travel time), and whether driver reassignments impact lateness. This supports the decision of whether to invest in predictive AI or implement operational fixes (like better courier dispatching or kitchen throttling).
