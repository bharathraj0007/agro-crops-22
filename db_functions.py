# ---- db_functions.py ----
import psycopg2
import pandas as pd

DATABASE_URL = "postgresql://postgres:Bharathraj@localhost:5432/postgres"

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

def setup_database():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS recommendations (
            id SERIAL PRIMARY KEY,
            nitrogen FLOAT, phosphorus FLOAT, potassium FLOAT,
            temperature FLOAT, humidity FLOAT, ph FLOAT, rainfall FLOAT,
            crop VARCHAR(255), timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def save_recommendation(data, crop):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO recommendations (nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall, crop)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (data['nitrogen'], data['phosphorus'], data['potassium'], data['temperature'],
         data['humidity'], data['ph'], data['rainfall'], crop)
    )
    conn.commit()
    cur.close()
    conn.close()

def get_history():
    conn = get_db_connection()
    df = pd.read_sql("SELECT * FROM recommendations ORDER BY timestamp DESC", conn)
    conn.close()
    if not df.empty:
        df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d %H:%M')
    return df

def clear_history():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM recommendations")
    conn.commit()
    cur.close()
    conn.close()

def get_dashboard_stats():
    conn = get_db_connection()
    try:
        total = pd.read_sql("SELECT COUNT(*) FROM recommendations", conn).iloc[0, 0]
        unique = pd.read_sql("SELECT COUNT(DISTINCT crop) FROM recommendations", conn).iloc[0, 0]
        latest_time = pd.read_sql("SELECT MAX(timestamp) FROM recommendations", conn).iloc[0, 0]
    except (IndexError, TypeError):
        total, unique, latest_time = 0, 0, None
    conn.close()
    latest_str = pd.to_datetime(latest_time).strftime('%Y-%m-%d %H:%M') if latest_time else "N/A"
    return {"total": total, "unique_crops": unique, "latest": latest_str}

def get_crop_counts():
    conn = get_db_connection()
    df = pd.read_sql("SELECT crop, COUNT(*) as count FROM recommendations GROUP BY crop ORDER BY count DESC", conn)
    conn.close()
    return df