"""
ETL script: Load CSV data into SQLite database
"""
import sqlite3
import pandas as pd
import os

# Paths
csv_path = os.path.join("data", "raw", "customers_raw.csv")
db_path = os.path.join("data", "db", "analytics.db")

# Create database and load CSV
def load_csv_to_sqlite():
    # Read CSV
    df = pd.read_csv(csv_path)
    
    # Connect to SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Drop table if exists (for fresh load)
    cursor.execute("DROP TABLE IF EXISTS customers_raw")
    
    # Create table
    cursor.execute("""
        CREATE TABLE customers_raw (
            customer_id INTEGER PRIMARY KEY,
            city TEXT,
            monthly_spend REAL,
            churned INTEGER
        )
    """)
    
    # Load data into table
    df.to_sql("customers_raw", conn, if_exists="append", index=False)
    
    conn.commit()
    conn.close()
    
    print(f"✓ Loaded {len(df)} rows from {csv_path} into {db_path}")

if __name__ == "__main__":
    load_csv_to_sqlite()
