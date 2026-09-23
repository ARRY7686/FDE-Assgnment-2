import sqlite3
conn = sqlite3.connect(r'C:\Users\aadig\OneDrive\Desktop\flasheats-classroom-pack\database\flasheats.db')
tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
print("Tables:", tables)

for table in tables:
    table_name = table[0]
    columns = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
    print(f"\nTable {table_name}:")
    for col in columns:
        print(f"  {col[1]} ({col[2]})")
