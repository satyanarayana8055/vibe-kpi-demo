"""
KPI script: City-level analytics using parameterized SQL
"""
import sqlite3
import os

db_path = os.path.join("data", "db", "analytics.db")

def city_kpi(city: str):
    """
    Calculate KPIs for a given city.
    Uses parameterized SQL to prevent SQL injection.
    
    Args:
        city: City name (e.g., 'Mumbai')
    
    Returns:
        Dictionary with KPIs: total_customers, avg_spend, churn_rate
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Parameterized query - the ? placeholder prevents SQL injection
    query = """
        SELECT 
            COUNT(*) as total_customers,
            ROUND(AVG(monthly_spend), 2) as avg_spend,
            ROUND(SUM(CAST(churned AS FLOAT)) / COUNT(*) * 100, 2) as churn_rate
        FROM customers_raw
        WHERE city = ?
    """
    
    # Execute with parameter binding
    cursor.execute(query, (city,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        total, avg_spend, churn_rate = result
        # Return None if no customers found for this city
        if total == 0:
            return None
        return {
            "city": city,
            "total_customers": int(total),
            "avg_spend": avg_spend,
            "churn_rate": churn_rate
        }
    else:
        return None

if __name__ == "__main__":
    # Test with valid city
    print("Test 1: Valid city (Mumbai)")
    kpi = city_kpi("Mumbai")
    print(kpi)
    print()
    
    # Test injection attempt - should NOT return all rows
    print("Test 2: SQL injection attempt")
    injection_attempt = "Mumbai' OR 1=1 --"
    kpi = city_kpi(injection_attempt)
    print(f"Result for '{injection_attempt}': {kpi}")
    print("(Should be None - parameterized SQL prevents injection)")
