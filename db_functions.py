# # ---- db_functions.py ----
# import psycopg2
# import pandas as pd

# DATABASE_URL = "postgresql://postgres:Bharathraj@localhost:5432/postgres"

# def get_db_connection():
#     return psycopg2.connect(DATABASE_URL)

# def setup_database():
#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute("""
#         CREATE TABLE IF NOT EXISTS recommendations (
#             id SERIAL PRIMARY KEY,
#             nitrogen FLOAT, phosphorus FLOAT, potassium FLOAT,
#             temperature FLOAT, humidity FLOAT, ph FLOAT, rainfall FLOAT,
#             crop VARCHAR(255), timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#         )
#     """)
#     conn.commit()
#     cur.close()
#     conn.close()

# def save_recommendation(data, crop):
#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute(
#         """
#         INSERT INTO recommendations (nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall, crop)
#         VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#         """,
#         (data['nitrogen'], data['phosphorus'], data['potassium'], data['temperature'],
#          data['humidity'], data['ph'], data['rainfall'], crop)
#     )
#     conn.commit()
#     cur.close()
#     conn.close()

# def get_history():
#     conn = get_db_connection()
#     df = pd.read_sql("SELECT * FROM recommendations ORDER BY timestamp DESC", conn)
#     conn.close()
#     if not df.empty:
#         df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d %H:%M')
#     return df

# def clear_history():
#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute("DELETE FROM recommendations")
#     conn.commit()
#     cur.close()
#     conn.close()

# def get_dashboard_stats():
#     conn = get_db_connection()
#     try:
#         total = pd.read_sql("SELECT COUNT(*) FROM recommendations", conn).iloc[0, 0]
#         unique = pd.read_sql("SELECT COUNT(DISTINCT crop) FROM recommendations", conn).iloc[0, 0]
#         latest_time = pd.read_sql("SELECT MAX(timestamp) FROM recommendations", conn).iloc[0, 0]
#     except (IndexError, TypeError):
#         total, unique, latest_time = 0, 0, None
#     conn.close()
#     latest_str = pd.to_datetime(latest_time).strftime('%Y-%m-%d %H:%M') if latest_time else "N/A"
#     return {"total": total, "unique_crops": unique, "latest": latest_str}

# def get_crop_counts():
#     conn = get_db_connection()
#     df = pd.read_sql("SELECT crop, COUNT(*) as count FROM recommendations GROUP BY crop ORDER BY count DESC", conn)
#     conn.close()
#     return df

# # ---- db_functions.py ----
# import sqlite3
# import pandas as pd
# from datetime import datetime

# DB_NAME = "agriassist.db"

# def setup_database():
#     """Initializes the database and creates tables if they don't exist."""
#     conn = sqlite3.connect(DB_NAME)
#     c = conn.cursor()
    
#     # Create recommendations table
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS recommendations (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
#             nitrogen REAL, phosphorus REAL, potassium REAL,
#             temperature REAL, humidity REAL, ph REAL, rainfall REAL,
#             crop TEXT
#         )
#     ''')
    
#     # --- NEW: Create profiles table ---
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS profiles (
#             id INTEGER PRIMARY KEY,
#             farm_info TEXT,
#             soil_type TEXT,
#             preferences TEXT,
#             last_updated DATETIME
#         )
#     ''')
    
#     conn.commit()
#     conn.close()

# def save_recommendation(data, crop):
#     """Saves a new crop recommendation to the database."""
#     conn = sqlite3.connect(DB_NAME)
#     c = conn.cursor()
#     c.execute('''
#         INSERT INTO recommendations (nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall, crop)
#         VALUES (?, ?, ?, ?, ?, ?, ?, ?)
#     ''', (data['nitrogen'], data['phosphorus'], data['potassium'], data['temperature'], 
#           data['humidity'], data['ph'], data['rainfall'], crop))
#     conn.commit()
#     conn.close()

# def get_history():
#     """Retrieves the recommendation history."""
#     conn = sqlite3.connect(DB_NAME)
#     df = pd.read_sql_query("SELECT timestamp, nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall, crop FROM recommendations ORDER BY timestamp DESC", conn)
#     conn.close()
#     return df

# def clear_history():
#     """Deletes all records from the recommendations table."""
#     conn = sqlite3.connect(DB_NAME)
#     c = conn.cursor()
#     c.execute("DELETE FROM recommendations")
#     conn.commit()
#     conn.close()

# def get_dashboard_stats():
#     """Gets statistics for the dashboard."""
#     conn = sqlite3.connect(DB_NAME)
#     history_df = pd.read_sql_query("SELECT crop, timestamp FROM recommendations", conn)
#     conn.close()
#     if not history_df.empty:
#         total = len(history_df)
#         unique_crops = history_df['crop'].nunique()
#         latest = pd.to_datetime(history_df['timestamp']).max().strftime('%Y-%m-%d')
#         return {'total': total, 'unique_crops': unique_crops, 'latest': latest}
#     return {'total': 0, 'unique_crops': 0, 'latest': 'N/A'}

# def get_crop_counts():
#     """Gets the count of each recommended crop."""
#     conn = sqlite3.connect(DB_NAME)
#     df = pd.read_sql_query("SELECT crop, COUNT(*) as count FROM recommendations GROUP BY crop ORDER BY count DESC", conn)
#     conn.close()
#     return df

# # --- NEW: Functions for profile management ---
# def save_profile_data(farm_info, soil_type, preferences):
#     """Saves or updates the user's profile data."""
#     conn = sqlite3.connect(DB_NAME)
#     c = conn.cursor()
#     c.execute('''
#         INSERT OR REPLACE INTO profiles (id, farm_info, soil_type, preferences, last_updated)
#         VALUES (?, ?, ?, ?, ?)
#     ''', (1, farm_info, soil_type, preferences, datetime.now()))
#     conn.commit()
#     conn.close()

# def get_profile_data():
#     """Retrieves the user's profile data."""
#     conn = sqlite3.connect(DB_NAME)
#     c = conn.cursor()
#     c.execute("SELECT farm_info, soil_type, preferences FROM profiles WHERE id = 1")
#     profile = c.fetchone()
#     conn.close()
#     if profile:
#         return {'farm_info': profile[0], 'soil_type': profile[1], 'preferences': profile[2]}
#     return {'farm_info': '', 'soil_type': 'Loamy', 'preferences': ''}

# # ---- db_functions.py ----
# import sqlite3
# import pandas as pd
# from datetime import datetime

# DB_NAME = "agriassist.db"

# def setup_database():
#     """Initializes the database and creates tables if they don't exist."""
#     conn = sqlite3.connect(DB_NAME)
#     c = conn.cursor()
    
#     # --- UPDATED: Added 'status' and 'id' to the table ---
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS recommendations (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
#             nitrogen REAL, phosphorus REAL, potassium REAL,
#             temperature REAL, humidity REAL, ph REAL, rainfall REAL,
#             crop TEXT,
#             status TEXT DEFAULT 'new'
#         )
#     ''')
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS profiles ( id INTEGER PRIMARY KEY, farm_info TEXT, soil_type TEXT, preferences TEXT, last_updated DATETIME )
#     ''')
#     conn.commit()
#     conn.close()

# def save_recommendation(data, crop):
#     """Saves a new crop recommendation and returns its ID."""
#     conn = sqlite3.connect(DB_NAME)
#     c = conn.cursor()
#     c.execute(
#         "INSERT INTO recommendations (nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall, crop) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
#         (data['nitrogen'], data['phosphorus'], data['potassium'], data['temperature'], data['humidity'], data['ph'], data['rainfall'], crop)
#     )
#     new_id = c.lastrowid
#     conn.commit()
#     conn.close()
#     return new_id

# # --- NEW: Function to mark a recommendation as done ---
# def mark_as_done(recommendation_id):
#     """Updates the status of a recommendation to 'done'."""
#     conn = sqlite3.connect(DB_NAME)
#     c = conn.cursor()
#     c.execute("UPDATE recommendations SET status = 'done' WHERE id = ?", (recommendation_id,))
#     conn.commit()
#     conn.close()

# def get_history():
#     """Retrieves the recommendation history, including status and id."""
#     conn = sqlite3.connect(DB_NAME)
#     df = pd.read_sql_query("SELECT id, timestamp, nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall, crop, status FROM recommendations ORDER BY timestamp DESC", conn)
#     conn.close()
#     return df

# # ... (rest of the functions like clear_history, get_dashboard_stats, etc. remain the same) ...
# def clear_history():
#     conn = sqlite3.connect(DB_NAME)
#     c = conn.cursor()
#     c.execute("DELETE FROM recommendations")
#     conn.commit()
#     conn.close()

# def get_dashboard_stats():
#     conn = sqlite3.connect(DB_NAME)
#     history_df = pd.read_sql_query("SELECT crop, timestamp FROM recommendations", conn)
#     conn.close()
#     if not history_df.empty:
#         total = len(history_df)
#         unique_crops = history_df['crop'].nunique()
#         latest = pd.to_datetime(history_df['timestamp']).max().strftime('%Y-%m-%d')
#         return {'total': total, 'unique_crops': unique_crops, 'latest': latest}
#     return {'total': 0, 'unique_crops': 0, 'latest': 'N/A'}

# def get_crop_counts():
#     conn = sqlite3.connect(DB_NAME)
#     df = pd.read_sql_query("SELECT crop, COUNT(*) as count FROM recommendations GROUP BY crop ORDER BY count DESC", conn)
#     conn.close()
#     return df

# def save_profile_data(farm_info, soil_type, preferences):
#     conn = sqlite3.connect(DB_NAME)
#     c = conn.cursor()
#     c.execute("INSERT OR REPLACE INTO profiles (id, farm_info, soil_type, preferences, last_updated) VALUES (?, ?, ?, ?, ?)", (1, farm_info, soil_type, preferences, datetime.now()))
#     conn.commit()
#     conn.close()

# def get_profile_data():
#     conn = sqlite3.connect(DB_NAME)
#     c = conn.cursor()
#     c.execute("SELECT farm_info, soil_type, preferences FROM profiles WHERE id = 1")
#     profile = c.fetchone()
#     conn.close()
#     if profile:
#         return {'farm_info': profile[0], 'soil_type': profile[1], 'preferences': profile[2]}
#     return {'farm_info': '', 'soil_type': 'Loamy', 'preferences': ''}

# ---- db_functions.py ----
# import sqlite3
# import pandas as pd
# from datetime import datetime

# DB_NAME = "agriassist.db"

# def setup_database():
#     """Initializes the database and creates tables if they don't exist."""
#     conn = sqlite3.connect(DB_NAME)
#     c = conn.cursor()
    
#     # Create recommendations table with a 'status' column
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS recommendations (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
#             nitrogen REAL, phosphorus REAL, potassium REAL,
#             temperature REAL, humidity REAL, ph REAL, rainfall REAL,
#             crop TEXT,
#             status TEXT DEFAULT 'new'
#         )
#     ''')
    
#     # Create profiles table
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS profiles (
#             id INTEGER PRIMARY KEY,
#             farm_info TEXT,
#             soil_type TEXT,
#             preferences TEXT,
#             last_updated DATETIME
#         )
#     ''')
    
#     conn.commit()
#     conn.close()

# def save_recommendation(data, crop):
#     """Saves a new crop recommendation to the database and returns its ID."""
#     conn = sqlite3.connect(DB_NAME)
#     c = conn.cursor()
#     c.execute(
#         "INSERT INTO recommendations (nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall, crop) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
#         (data['nitrogen'], data['phosphorus'], data['potassium'], data['temperature'], data['humidity'], data['ph'], data['rainfall'], crop)
#     )
#     new_id = c.lastrowid
#     conn.commit()
#     conn.close()
#     return new_id

# def mark_as_done(recommendation_id):
#     """Updates the status of a recommendation to 'done'."""
#     conn = sqlite3.connect(DB_NAME)
#     c = conn.cursor()
#     c.execute("UPDATE recommendations SET status = 'done' WHERE id = ?", (recommendation_id,))
#     conn.commit()
#     conn.close()

# def get_history():
#     """Retrieves the recommendation history, including status and id."""
#     conn = sqlite3.connect(DB_NAME)
#     # Ensure the table exists before trying to read from it
#     try:
#         df = pd.read_sql_query("SELECT id, timestamp, nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall, crop, status FROM recommendations ORDER BY timestamp DESC", conn)
#     except pd.io.sql.DatabaseError:
#         df = pd.DataFrame() # Return empty dataframe if table doesn't exist yet
#     conn.close()
#     return df

# def clear_history():
#     """Deletes all records from the recommendations table."""
#     conn = sqlite3.connect(DB_NAME)
#     c = conn.cursor()
#     c.execute("DELETE FROM recommendations")
#     conn.commit()
#     conn.close()

# def get_dashboard_stats():
#     """Gets statistics for the dashboard."""
#     conn = sqlite3.connect(DB_NAME)
#     try:
#         history_df = pd.read_sql_query("SELECT crop, timestamp FROM recommendations", conn)
#     except pd.io.sql.DatabaseError:
#         history_df = pd.DataFrame()
#     conn.close()
#     if not history_df.empty:
#         total = len(history_df)
#         unique_crops = history_df['crop'].nunique()
#         latest = pd.to_datetime(history_df['timestamp']).max().strftime('%Y-%m-%d')
#         return {'total': total, 'unique_crops': unique_crops, 'latest': latest}
#     return {'total': 0, 'unique_crops': 0, 'latest': 'N/A'}

# def get_crop_counts():
#     """Gets the count of each recommended crop."""
#     conn = sqlite3.connect(DB_NAME)
#     try:
#         df = pd.read_sql_query("SELECT crop, COUNT(*) as count FROM recommendations GROUP BY crop ORDER BY count DESC", conn)
#     except pd.io.sql.DatabaseError:
#         df = pd.DataFrame()
#     conn.close()
#     return df

# def save_profile_data(farm_info, soil_type, preferences):
#     conn = sqlite3.connect(DB_NAME)
#     c = conn.cursor()
#     c.execute("INSERT OR REPLACE INTO profiles (id, farm_info, soil_type, preferences, last_updated) VALUES (?, ?, ?, ?, ?)", (1, farm_info, soil_type, preferences, datetime.now()))
#     conn.commit()
#     conn.close()

# def get_profile_data():
#     conn = sqlite3.connect(DB_NAME)
#     c = conn.cursor()
#     try:
#         c.execute("SELECT farm_info, soil_type, preferences FROM profiles WHERE id = 1")
#         profile = c.fetchone()
#     except sqlite3.OperationalError:
#         profile = None # Table might not exist yet
#     conn.close()
#     if profile:
#         return {'farm_info': profile[0], 'soil_type': profile[1], 'preferences': profile[2]}
#     return {'farm_info': '', 'soil_type': 'Loamy', 'preferences': ''}

# # ---- db_functions.py ----
# import sqlite3
# import pandas as pd
# from datetime import datetime

# DB_NAME = "agriassist.db"

# def get_db_connection():
#     """Establishes a connection to the database."""
#     return sqlite3.connect(DB_NAME)

# def setup_database():
#     """Initializes the database and creates tables if they don't exist."""
#     conn = get_db_connection()
#     c = conn.cursor()
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS recommendations (
#             id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
#             nitrogen REAL, phosphorus REAL, potassium REAL, temperature REAL, humidity REAL, ph REAL, rainfall REAL,
#             crop TEXT, status TEXT DEFAULT 'new'
#         )
#     ''')
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS profiles (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT DEFAULT 'Default User',
#             email TEXT DEFAULT 'user@example.com',
#             farm_info TEXT,
#             soil_type TEXT,
#             preferences TEXT,
#             last_updated DATETIME
#         )
#     ''')
#     conn.commit()
#     conn.close()

# # --- Functions for Recommendations (no changes here) ---
# def save_recommendation(data, crop):
#     conn = get_db_connection()
#     c = conn.cursor()
#     c.execute( "INSERT INTO recommendations (nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall, crop) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (data['nitrogen'], data['phosphorus'], data['potassium'], data['temperature'], data['humidity'], data['ph'], data['rainfall'], crop) )
#     new_id = c.lastrowid
#     conn.commit()
#     conn.close()
#     return new_id

# def mark_as_done(recommendation_id):
#     conn = get_db_connection()
#     c = conn.cursor()
#     c.execute("UPDATE recommendations SET status = 'done' WHERE id = ?", (recommendation_id,))
#     conn.commit()
#     conn.close()

# def get_history():
#     conn = get_db_connection()
#     try:
#         df = pd.read_sql_query("SELECT id, timestamp, nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall, crop, status FROM recommendations ORDER BY timestamp DESC", conn)
#     except pd.io.sql.DatabaseError:
#         df = pd.DataFrame()
#     conn.close()
#     return df

# def clear_history():
#     conn = get_db_connection()
#     c = conn.cursor()
#     c.execute("DELETE FROM recommendations")
#     conn.commit()
#     conn.close()

# def get_dashboard_stats():
#     conn = get_db_connection()
#     try:
#         history_df = pd.read_sql_query("SELECT crop, timestamp FROM recommendations", conn)
#     except pd.io.sql.DatabaseError:
#         history_df = pd.DataFrame()
#     conn.close()
#     if not history_df.empty:
#         total, unique_crops, latest = len(history_df), history_df['crop'].nunique(), pd.to_datetime(history_df['timestamp']).max().strftime('%Y-%m-%d')
#         return {'total': total, 'unique_crops': unique_crops, 'latest': latest}
#     return {'total': 0, 'unique_crops': 0, 'latest': 'N/A'}

# def get_crop_counts():
#     conn = get_db_connection()
#     try:
#         df = pd.read_sql_query("SELECT crop, COUNT(*) as count FROM recommendations GROUP BY crop ORDER BY count DESC", conn)
#     except pd.io.sql.DatabaseError:
#         df = pd.DataFrame()
#     conn.close()
#     return df

# def get_admin_stats():
#     conn = get_db_connection()
#     try:
#         total_recs = pd.read_sql_query("SELECT COUNT(*) FROM recommendations", conn).iloc[0, 0]
#         total_profiles = pd.read_sql_query("SELECT COUNT(*) FROM profiles", conn).iloc[0, 0]
#     except (pd.io.sql.DatabaseError, IndexError):
#         total_recs, total_profiles = 0, 0
#     conn.close()
#     return {'total_recommendations': total_recs, 'total_profiles': total_profiles}

# # --- Functions for Profile Management ---
# def get_all_profiles():
#     """Retrieves all profiles from the database for the admin."""
#     conn = get_db_connection()
#     try:
#         df = pd.read_sql_query("SELECT id, name, email, farm_info, soil_type, preferences, last_updated FROM profiles ORDER BY id", conn)
#     except pd.io.sql.DatabaseError:
#         df = pd.DataFrame()
#     conn.close()
#     return df

# def save_profile_data(farm_info, soil_type, preferences):
#     """Saves or updates the user's profile data (for the default user, id=1)."""
#     conn = get_db_connection()
#     c = conn.cursor()
#     c.execute("INSERT OR REPLACE INTO profiles (id, farm_info, soil_type, preferences, last_updated) VALUES (?, ?, ?, ?, ?)", (1, farm_info, soil_type, preferences, datetime.now()))
#     conn.commit()
#     conn.close()

# def get_profile_data():
#     """Retrieves the default user's profile data."""
#     conn = get_db_connection()
#     c = conn.cursor()
#     try:
#         c.execute("SELECT farm_info, soil_type, preferences FROM profiles WHERE id = 1")
#         profile = c.fetchone()
#     except sqlite3.OperationalError:
#         profile = None
#     conn.close()
#     if profile:
#         return {'farm_info': profile[0], 'soil_type': profile[1], 'preferences': profile[2]}
#     return {'farm_info': '', 'soil_type': 'Loamy', 'preferences': ''}

# # --- NEW: Admin functions for User Management ---
# def add_profile(name, email, farm_info, soil_type, preferences):
#     """Admin function to add a new user profile."""
#     conn = get_db_connection()
#     c = conn.cursor()
#     c.execute("INSERT INTO profiles (name, email, farm_info, soil_type, preferences, last_updated) VALUES (?, ?, ?, ?, ?, ?)",
#               (name, email, farm_info, soil_type, preferences, datetime.now()))
#     conn.commit()
#     conn.close()

# def update_profile(profile_id, name, email, farm_info, soil_type, preferences):
#     """Admin function to update an existing user profile."""
#     conn = get_db_connection()
#     c = conn.cursor()
#     c.execute("UPDATE profiles SET name=?, email=?, farm_info=?, soil_type=?, preferences=?, last_updated=? WHERE id=?",
#               (name, email, farm_info, soil_type, preferences, datetime.now(), profile_id))
#     conn.commit()
#     conn.close()

# def delete_profile(profile_id):
#     """Admin function to delete a user profile."""
#     conn = get_db_connection()
#     c = conn.cursor()
#     c.execute("DELETE FROM profiles WHERE id=?", (profile_id,))
#     conn.commit()
#     conn.close()

# # ---- Add this function to db_functions.py ----

# def get_admin_stats():
#     """Gets statistics for the Admin Dashboard."""
#     conn = get_db_connection()
#     try:
#         total_recs = pd.read_sql_query("SELECT COUNT(*) FROM recommendations", conn).iloc[0, 0]
#         total_profiles = pd.read_sql_query("SELECT COUNT(*) FROM profiles", conn).iloc[0, 0]
#     except (pd.io.sql.DatabaseError, IndexError):
#         total_recs, total_profiles = 0, 0
#     conn.close()
#     return {'total_recommendations': total_recs, 'total_profiles': total_profiles}

# # ---- db_functions.py ----
# import sqlite3
# import pandas as pd
# from datetime import datetime
# import crop_data # Used for one-time data population

# DB_NAME = "agriassist.db"

# def get_db_connection():
#     """Establishes a connection to the database."""
#     return sqlite3.connect(DB_NAME)

# def setup_database():
#     """Initializes the database and creates tables if they don't exist."""
#     conn = get_db_connection()
#     c = conn.cursor()
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS recommendations (
#             id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
#             nitrogen REAL, phosphorus REAL, potassium REAL, temperature REAL, humidity REAL, ph REAL, rainfall REAL,
#             crop TEXT, status TEXT DEFAULT 'new'
#         )
#     ''')
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS profiles (
#             id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, farm_info TEXT,
#             soil_type TEXT, preferences TEXT, last_updated DATETIME
#         )
#     ''')
#     # --- NEW: Create crops table ---
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS crops (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT UNIQUE,
#             description TEXT,
#             water_needs TEXT,
#             yield_potential TEXT,
#             image_path TEXT
#         )
#     ''')
#     conn.commit()
#     conn.close()

# # --- NEW: One-time function to populate the crops table ---
# def populate_crops_table_if_empty():
#     """Populates the crops table from the crop_data.py file if the table is empty."""
#     conn = get_db_connection()
#     c = conn.cursor()
#     c.execute("SELECT COUNT(*) FROM crops")
#     count = c.fetchone()[0]
#     if count == 0:
#         for crop_name, details in crop_data.CROP_DETAILS.items():
#             if crop_name != 'default':
#                 image = crop_data.CROP_IMAGES.get(crop_name, '')
#                 c.execute(
#                     "INSERT INTO crops (name, description, water_needs, yield_potential, image_path) VALUES (?, ?, ?, ?, ?)",
#                     (crop_name.capitalize(), details['description'], details['water'], details['yield'], image)
#                 )
#         conn.commit()
#     conn.close()


# # ... (save_recommendation, mark_as_done, get_history, etc. are unchanged) ...

# # --- NEW: Functions for Admin Crop Management ---
# def get_all_crops():
#     """Retrieves all crops from the database for the admin."""
#     conn = get_db_connection()
#     try:
#         df = pd.read_sql_query("SELECT id, name, description, water_needs, yield_potential, image_path FROM crops ORDER BY name", conn)
#     except pd.io.sql.DatabaseError:
#         df = pd.DataFrame()
#     conn.close()
#     return df

# # ... (The rest of your functions remain the same) ...
# # ---- db_functions.py ----
# import sqlite3
# import pandas as pd
# from datetime import datetime

# DB_NAME = "agriassist.db"

# def get_db_connection():
#     """Establishes a connection to the database."""
#     return sqlite3.connect(DB_NAME)

# def setup_database():
#     """Initializes the database and creates tables if they don't exist."""
#     conn = get_db_connection()
#     c = conn.cursor()
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS recommendations (
#             id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
#             nitrogen REAL, phosphorus REAL, potassium REAL, temperature REAL, humidity REAL, ph REAL, rainfall REAL,
#             crop TEXT, status TEXT DEFAULT 'new'
#         )
#     ''')
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS profiles (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT DEFAULT 'Default User',
#             email TEXT DEFAULT 'user@example.com',
#             farm_info TEXT,
#             soil_type TEXT,
#             preferences TEXT,
#             last_updated DATETIME
#         )
#     ''')
#     conn.commit()
#     conn.close()

# # --- Functions for Recommendations (no changes here) ---
# def save_recommendation(data, crop):
#     conn = get_db_connection()
#     c = conn.cursor()
#     c.execute( "INSERT INTO recommendations (nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall, crop) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (data['nitrogen'], data['phosphorus'], data['potassium'], data['temperature'], data['humidity'], data['ph'], data['rainfall'], crop) )
#     new_id = c.lastrowid
#     conn.commit()
#     conn.close()
#     return new_id

# def mark_as_done(recommendation_id):
#     conn = get_db_connection()
#     c = conn.cursor()
#     c.execute("UPDATE recommendations SET status = 'done' WHERE id = ?", (recommendation_id,))
#     conn.commit()
#     conn.close()

# def get_history():
#     conn = get_db_connection()
#     try:
#         df = pd.read_sql_query("SELECT id, timestamp, nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall, crop, status FROM recommendations ORDER BY timestamp DESC", conn)
#     except pd.io.sql.DatabaseError:
#         df = pd.DataFrame()
#     conn.close()
#     return df

# def clear_history():
#     conn = get_db_connection()
#     c = conn.cursor()
#     c.execute("DELETE FROM recommendations")
#     conn.commit()
#     conn.close()

# def get_dashboard_stats():
#     conn = get_db_connection()
#     try:
#         history_df = pd.read_sql_query("SELECT crop, timestamp FROM recommendations", conn)
#     except pd.io.sql.DatabaseError:
#         history_df = pd.DataFrame()
#     conn.close()
#     if not history_df.empty:
#         total, unique_crops, latest = len(history_df), history_df['crop'].nunique(), pd.to_datetime(history_df['timestamp']).max().strftime('%Y-%m-%d')
#         return {'total': total, 'unique_crops': unique_crops, 'latest': latest}
#     return {'total': 0, 'unique_crops': 0, 'latest': 'N/A'}

# def get_crop_counts():
#     conn = get_db_connection()
#     try:
#         df = pd.read_sql_query("SELECT crop, COUNT(*) as count FROM recommendations GROUP BY crop ORDER BY count DESC", conn)
#     except pd.io.sql.DatabaseError:
#         df = pd.DataFrame()
#     conn.close()
#     return df

# def get_admin_stats():
#     conn = get_db_connection()
#     try:
#         total_recs = pd.read_sql_query("SELECT COUNT(*) FROM recommendations", conn).iloc[0, 0]
#         total_profiles = pd.read_sql_query("SELECT COUNT(*) FROM profiles", conn).iloc[0, 0]
#     except (pd.io.sql.DatabaseError, IndexError):
#         total_recs, total_profiles = 0, 0
#     conn.close()
#     return {'total_recommendations': total_recs, 'total_profiles': total_profiles}

# # --- Functions for Profile Management ---
# def get_all_profiles():
#     """Retrieves all profiles from the database for the admin."""
#     conn = get_db_connection()
#     try:
#         df = pd.read_sql_query("SELECT id, name, email, farm_info, soil_type, preferences, last_updated FROM profiles ORDER BY id", conn)
#     except pd.io.sql.DatabaseError:
#         df = pd.DataFrame()
#     conn.close()
#     return df

# def save_profile_data(farm_info, soil_type, preferences):
#     """Saves or updates the user's profile data (for the default user, id=1)."""
#     conn = get_db_connection()
#     c = conn.cursor()
#     c.execute("INSERT OR REPLACE INTO profiles (id, farm_info, soil_type, preferences, last_updated) VALUES (?, ?, ?, ?, ?)", (1, farm_info, soil_type, preferences, datetime.now()))
#     conn.commit()
#     conn.close()

# def get_profile_data():
#     """Retrieves the default user's profile data."""
#     conn = get_db_connection()
#     c = conn.cursor()
#     try:
#         c.execute("SELECT farm_info, soil_type, preferences FROM profiles WHERE id = 1")
#         profile = c.fetchone()
#     except sqlite3.OperationalError:
#         profile = None
#     conn.close()
#     if profile:
#         return {'farm_info': profile[0], 'soil_type': profile[1], 'preferences': profile[2]}
#     return {'farm_info': '', 'soil_type': 'Loamy', 'preferences': ''}

# # --- Admin functions for User Management ---
# def add_profile(name, email, farm_info, soil_type, preferences):
#     """Admin function to add a new user profile."""
#     conn = get_db_connection()
#     c = conn.cursor()
#     c.execute("INSERT INTO profiles (name, email, farm_info, soil_type, preferences, last_updated) VALUES (?, ?, ?, ?, ?, ?)",
#               (name, email, farm_info, soil_type, preferences, datetime.now()))
#     conn.commit()
#     conn.close()

# def update_profile(profile_id, name, email, farm_info, soil_type, preferences):
#     """Admin function to update an existing user profile."""
#     conn = get_db_connection()
#     c = conn.cursor()
#     c.execute("UPDATE profiles SET name=?, email=?, farm_info=?, soil_type=?, preferences=?, last_updated=? WHERE id=?",
#               (name, email, farm_info, soil_type, preferences, datetime.now(), profile_id))
#     conn.commit()
#     conn.close()

# def delete_profile(profile_id):
#     """Admin function to delete a user profile."""
#     conn = get_db_connection()
#     c = conn.cursor()
#     c.execute("DELETE FROM profiles WHERE id=?", (profile_id,))
#     conn.commit()
#     conn.close()

# import sqlite3
# import pandas as pd
# from datetime import datetime
# import crop_data as cd

# DB_NAME = "agriassist.db"

# def get_db_connection():
#     return sqlite3.connect(DB_NAME)

# def setup_database():
#     """Initializes the database and creates all necessary tables."""
#     conn = get_db_connection()
#     c = conn.cursor()
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS recommendations (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, nitrogen REAL, phosphorus REAL, potassium REAL, temperature REAL, humidity REAL, ph REAL, rainfall REAL, crop TEXT, status TEXT DEFAULT 'new')
#     ''')
#     # UPDATED: Added name and email to profiles table
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS profiles (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, farm_info TEXT, soil_type TEXT, preferences TEXT, last_updated DATETIME)
#     ''')
#     # NEW: Crops table to store manageable crop data
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS crops (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT UNIQUE,
#             description TEXT,
#             water_consumption TEXT,
#             yield TEXT,
#             image_path TEXT
#         )
#     ''')
#     conn.commit()
#     conn.close()

# # --- Functions for Client App ---
# def save_recommendation(data, crop):
#     conn = sqlite3.connect(DB_NAME)
#     c = conn.cursor()
#     c.execute("INSERT INTO recommendations (nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall, crop) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",(data['nitrogen'], data['phosphorus'], data['potassium'], data['temperature'], data['humidity'], data['ph'], data['rainfall'], crop))
#     new_id = c.lastrowid
#     conn.commit()
#     conn.close()
#     return new_id

# def mark_as_done(recommendation_id):
#     conn = sqlite3.connect(DB_NAME)
#     c = conn.cursor()
#     c.execute("UPDATE recommendations SET status = 'done' WHERE id = ?", (recommendation_id,))
#     conn.commit()
#     conn.close()

# def get_history():
#     conn = sqlite3.connect(DB_NAME)
#     try:
#         df = pd.read_sql_query("SELECT id, timestamp, nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall, crop, status FROM recommendations ORDER BY timestamp DESC", conn)
#     except pd.io.sql.DatabaseError:
#         df = pd.DataFrame()
#     conn.close()
#     return df

# def clear_history():
#     conn = sqlite3.connect(DB_NAME)
#     c = conn.cursor()
#     c.execute("DELETE FROM recommendations")
#     conn.commit()
#     conn.close()

# def get_dashboard_stats():
#     conn = sqlite3.connect(DB_NAME)
#     try:
#         history_df = pd.read_sql_query("SELECT crop, timestamp FROM recommendations", conn)
#     except pd.io.sql.DatabaseError:
#         history_df = pd.DataFrame()
#     conn.close()
#     if not history_df.empty:
#         total = len(history_df)
#         unique_crops = history_df['crop'].nunique()
#         latest = pd.to_datetime(history_df['timestamp']).max().strftime('%Y-%m-%d')
#         return {'total': total, 'unique_crops': unique_crops, 'latest': latest}
#     return {'total': 0, 'unique_crops': 0, 'latest': 'N/A'}

# def get_crop_counts():
#     conn = sqlite3.connect(DB_NAME)
#     try:
#         df = pd.read_sql_query("SELECT crop, COUNT(*) as count FROM recommendations GROUP BY crop ORDER BY count DESC", conn)
#     except pd.io.sql.DatabaseError:
#         df = pd.DataFrame()
#     conn.close()
#     return df

# def save_profile_data(name, email, farm_info, soil_type, preferences):
#     conn = sqlite3.connect(DB_NAME)
#     c = conn.cursor()
#     # Assuming one profile per user for now, with ID 1
#     c.execute("INSERT OR REPLACE INTO profiles (id, name, email, farm_info, soil_type, preferences, last_updated) VALUES (?, ?, ?, ?, ?, ?, ?)", (1, name, email, farm_info, soil_type, preferences, datetime.now()))
#     conn.commit()
#     conn.close()

# def get_profile_data():
#     conn = sqlite3.connect(DB_NAME)
#     c = conn.cursor()
#     try:
#         c.execute("SELECT name, email, farm_info, soil_type, preferences FROM profiles WHERE id = 1")
#         profile = c.fetchone()
#     except sqlite3.OperationalError:
#         profile = None
#     conn.close()
#     if profile:
#         return {'name': profile[0], 'email': profile[1], 'farm_info': profile[2], 'soil_type': profile[3], 'preferences': profile[4]}
#     return {'name': '', 'email': '', 'farm_info': '', 'soil_type': 'Loamy', 'preferences': ''}


# # --- NEW Functions for Admin Panel ---
# def get_admin_stats():
#     conn = sqlite3.connect(DB_NAME)
#     try:
#         total_recs = pd.read_sql_query("SELECT COUNT(*) FROM recommendations", conn).iloc[0, 0]
#         total_profiles = pd.read_sql_query("SELECT COUNT(*) FROM profiles", conn).iloc[0, 0]
#     except (pd.io.sql.DatabaseError, IndexError):
#         total_recs, total_profiles = 0, 0
#     conn.close()
#     return {'total_recommendations': total_recs, 'total_profiles': total_profiles}

# def get_all_profiles():
#     conn = sqlite3.connect(DB_NAME)
#     try:
#         df = pd.read_sql_query("SELECT * FROM profiles ORDER BY name", conn)
#     except pd.io.sql.DatabaseError:
#         df = pd.DataFrame()
#     conn.close()
#     return df

# def add_profile(name, email, farm_info, soil_type, preferences):
#     conn = sqlite3.connect(DB_NAME)
#     c = conn.cursor()
#     c.execute("INSERT INTO profiles (name, email, farm_info, soil_type, preferences, last_updated) VALUES (?, ?, ?, ?, ?, ?)",(name, email, farm_info, soil_type, preferences, datetime.now()))
#     conn.commit()
#     conn.close()

# def update_profile(profile_id, name, email, farm_info, soil_type, preferences):
#     conn = sqlite3.connect(DB_NAME)
#     c = conn.cursor()
#     c.execute("UPDATE profiles SET name=?, email=?, farm_info=?, soil_type=?, preferences=?, last_updated=? WHERE id=?",(name, email, farm_info, soil_type, preferences, datetime.now(), profile_id))
#     conn.commit()
#     conn.close()

# def delete_profile(profile_id):
#     conn = sqlite3.connect(DB_NAME)
#     c = conn.cursor()
#     c.execute("DELETE FROM profiles WHERE id=?", (profile_id,))
#     conn.commit()
#     conn.close()

# def get_all_crops():
#     conn = sqlite3.connect(DB_NAME)
#     try:
#         df = pd.read_sql_query("SELECT * FROM crops ORDER BY name", conn)
#     except pd.io.sql.DatabaseError:
#         df = pd.DataFrame()
#     conn.close()
#     return df

# def add_crop(name, description, water, crop_yield, image_path):
#     conn = sqlite3.connect(DB_NAME)
#     c = conn.cursor()
#     c.execute("INSERT INTO crops (name, description, water_consumption, yield, image_path) VALUES (?, ?, ?, ?, ?)", (name, description, water, crop_yield, image_path))
#     conn.commit()
#     conn.close()

# def update_crop(crop_id, name, description, water, crop_yield, image_path):
#     conn = sqlite3.connect(DB_NAME)
#     c = conn.cursor()
#     c.execute("UPDATE crops SET name=?, description=?, water_consumption=?, yield=?, image_path=? WHERE id=?", (name, description, water, crop_yield, image_path, crop_id))
#     conn.commit()
#     conn.close()

# def delete_crop(crop_id):
#     conn = sqlite3.connect(DB_NAME)
#     c = conn.cursor()
#     c.execute("DELETE FROM crops WHERE id=?", (crop_id,))
#     conn.commit()
#     conn.close()

# def populate_crops_table_if_empty():
#     """Populates the crops table from crop_data.py if it's empty."""
#     conn = sqlite3.connect(DB_NAME)
#     c = conn.cursor()
#     c.execute("SELECT COUNT(*) FROM crops")
#     count = c.fetchone()[0]
#     if count == 0:
#         for crop_name, details in cd.CROP_DETAILS.items():
#             if crop_name != 'default':
#                 image_path = cd.CROP_IMAGES.get(crop_name, cd.CROP_IMAGES['default'])
#                 c.execute(
#                     "INSERT INTO crops (name, description, water_consumption, yield, image_path) VALUES (?, ?, ?, ?, ?)",
#                     (crop_name.capitalize(), details['description'], details['water'], details['yield'], image_path)
#                 )
#         conn.commit()
#     conn.close()

# ---- db_functions.py ----
# import sqlite3
# import pandas as pd
# from datetime import datetime
# import os
# import crop_data # Assuming crop_data.py is in the root directory

# DB_NAME = "agriassist.db"
# ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
# DB_PATH = os.path.join(ROOT_DIR, DB_NAME)


# def get_db_connection():
#     return sqlite3.connect(DB_PATH)

# def setup_database():
#     conn = get_db_connection()
#     c = conn.cursor()
#     # Recommendations Table
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS recommendations (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
#             nitrogen REAL, phosphorus REAL, potassium REAL,
#             temperature REAL, humidity REAL, ph REAL, rainfall REAL,
#             crop TEXT,
#             status TEXT DEFAULT 'new'
#         )
#     ''')
#     # Profiles Table
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS profiles (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT,
#             email TEXT,
#             farm_info TEXT,
#             soil_type TEXT,
#             preferences TEXT,
#             last_updated DATETIME
#         )
#     ''')
#     # Crops Table
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS crops (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT UNIQUE,
#             description TEXT,
#             water_consumption TEXT,
#             yield TEXT,
#             image_path TEXT
#         )
#     ''')
#     # Contacts Table
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS contacts (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
#             name TEXT,
#             email TEXT,
#             message TEXT,
#             status TEXT DEFAULT 'new'
#         )
#     ''')
#     conn.commit()
#     conn.close()

# # --- Recommendation Functions ---
# def save_recommendation(data, crop):
#     conn = get_db_connection()
#     c = conn.cursor()
#     c.execute("INSERT INTO recommendations (nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall, crop) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",(data['nitrogen'], data['phosphorus'], data['potassium'], data['temperature'], data['humidity'], data['ph'], data['rainfall'], crop))
#     new_id = c.lastrowid
#     conn.commit()
#     conn.close()
#     return new_id

# def mark_as_done(recommendation_id):
#     conn = get_db_connection()
#     c = conn.cursor()
#     c.execute("UPDATE recommendations SET status = 'done' WHERE id = ?", (recommendation_id,))
#     conn.commit()
#     conn.close()

# def get_history():
#     conn = get_db_connection()
#     try:
#         df = pd.read_sql_query("SELECT id, timestamp, nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall, crop, status FROM recommendations ORDER BY timestamp DESC", conn)
#     except pd.io.sql.DatabaseError: df = pd.DataFrame()
#     conn.close()
#     return df

# def clear_history():
#     conn = get_db_connection()
#     c = conn.cursor()
#     c.execute("DELETE FROM recommendations")
#     conn.commit()
#     conn.close()

# # --- Dashboard/Insights Functions ---
# def get_dashboard_stats():
#     conn = get_db_connection()
#     try:
#         history_df = pd.read_sql_query("SELECT crop, timestamp FROM recommendations", conn)
#     except pd.io.sql.DatabaseError: history_df = pd.DataFrame()
#     conn.close()
#     if not history_df.empty:
#         total = len(history_df); unique_crops = history_df['crop'].nunique(); latest = pd.to_datetime(history_df['timestamp']).max().strftime('%Y-%m-%d')
#         return {'total': total, 'unique_crops': unique_crops, 'latest': latest}
#     return {'total': 0, 'unique_crops': 0, 'latest': 'N/A'}

# def get_crop_counts():
#     conn = get_db_connection()
#     try:
#         df = pd.read_sql_query("SELECT crop, COUNT(*) as count FROM recommendations GROUP BY crop ORDER BY count DESC", conn)
#     except pd.io.sql.DatabaseError: df = pd.DataFrame()
#     conn.close()
#     return df

# # --- Profile Functions ---
# def save_profile_data(farm_info, soil_type, preferences):
#     conn = get_db_connection()
#     c = conn.cursor()
#     c.execute("INSERT OR REPLACE INTO profiles (id, farm_info, soil_type, preferences, last_updated) VALUES (?, ?, ?, ?, ?)", (1, farm_info, soil_type, preferences, datetime.now()))
#     conn.commit()
#     conn.close()

# def get_profile_data():
#     conn = get_db_connection()
#     c = conn.cursor()
#     try:
#         c.execute("SELECT farm_info, soil_type, preferences FROM profiles WHERE id = 1")
#         profile = c.fetchone()
#     except sqlite3.OperationalError: profile = None
#     conn.close()
#     if profile:
#         return {'farm_info': profile[0], 'soil_type': profile[1], 'preferences': profile[2]}
#     return {'farm_info': '', 'soil_type': 'Loamy', 'preferences': ''}

# # --- Admin User Management Functions ---
# def add_profile(name, email, farm_info, soil_type, preferences):
#     conn = get_db_connection()
#     c = conn.cursor()
#     c.execute("INSERT INTO profiles (name, email, farm_info, soil_type, preferences, last_updated) VALUES (?, ?, ?, ?, ?, ?)", (name, email, farm_info, soil_type, preferences, datetime.now()))
#     conn.commit()
#     conn.close()

# def get_all_profiles():
#     conn = get_db_connection()
#     try:
#         df = pd.read_sql_query("SELECT id, name, email, farm_info, soil_type, preferences FROM profiles", conn)
#     except pd.io.sql.DatabaseError: df = pd.DataFrame()
#     conn.close()
#     return df

# def update_profile(profile_id, name, email, farm_info, soil_type, preferences):
#     conn = get_db_connection()
#     c = conn.cursor()
#     c.execute("UPDATE profiles SET name=?, email=?, farm_info=?, soil_type=?, preferences=?, last_updated=? WHERE id=?", (name, email, farm_info, soil_type, preferences, datetime.now(), profile_id))
#     conn.commit()
#     conn.close()

# def delete_profile(profile_id):
#     conn = get_db_connection()
#     c = conn.cursor()
#     c.execute("DELETE FROM profiles WHERE id=?", (profile_id,))
#     conn.commit()
#     conn.close()

# # --- Admin Crop Management Functions ---
# def populate_crops_table_if_empty():
#     conn = get_db_connection()
#     c = conn.cursor()
#     c.execute("SELECT COUNT(*) FROM crops")
#     if c.fetchone()[0] == 0:
#         for crop_name, details in crop_data.CROP_DETAILS.items():
#             if crop_name != 'default':
#                 image_path = crop_data.CROP_IMAGES.get(crop_name, '')
#                 c.execute("INSERT INTO crops (name, description, water_consumption, yield, image_path) VALUES (?, ?, ?, ?, ?)", (crop_name.capitalize(), details['description'], details['water'], details['yield'], image_path))
#         conn.commit()
#     conn.close()

# def get_all_crops():
#     conn = get_db_connection()
#     try:
#         df = pd.read_sql_query("SELECT * FROM crops ORDER BY name", conn)
#     except pd.io.sql.DatabaseError: df = pd.DataFrame()
#     conn.close()
#     return df

# def add_crop(name, description, water, crop_yield, image_path):
#     conn = get_db_connection()
#     c = conn.cursor()
#     c.execute("INSERT INTO crops (name, description, water_consumption, yield, image_path) VALUES (?, ?, ?, ?, ?)",(name.capitalize(), description, water, crop_yield, image_path))
#     conn.commit()
#     conn.close()

# def update_crop(crop_id, name, description, water, crop_yield, image_path):
#     conn = get_db_connection()
#     c = conn.cursor()
#     c.execute("UPDATE crops SET name=?, description=?, water_consumption=?, yield=?, image_path=? WHERE id=?",(name.capitalize(), description, water, crop_yield, image_path, crop_id))
#     conn.commit()
#     conn.close()

# def delete_crop(crop_id):
#     conn = get_db_connection()
#     c = conn.cursor()
#     c.execute("DELETE FROM crops WHERE id=?", (crop_id,))
#     conn.commit()
#     conn.close()

# # --- Support/Contact Functions ---
# def save_contact_message(name, email, message):
#     conn = get_db_connection()
#     c = conn.cursor()
#     c.execute("INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)", (name, email, message))
#     conn.commit()
#     conn.close()

# def get_all_messages():
#     conn = get_db_connection()
#     try:
#         df = pd.read_sql_query("SELECT id, timestamp, name, email, message, status FROM contacts ORDER BY timestamp DESC", conn)
#     except pd.io.sql.DatabaseError: df = pd.DataFrame()
#     conn.close()
#     return df

# def get_admin_stats():
#     conn = get_db_connection()
#     try:
#         total_recs = pd.read_sql_query("SELECT COUNT(*) FROM recommendations", conn).iloc[0, 0]
#         total_profiles = pd.read_sql_query("SELECT COUNT(*) FROM profiles", conn).iloc[0, 0]
#     except (pd.io.sql.DatabaseError, IndexError):
#         total_recs, total_profiles = 0, 0
#     conn.close()
#     return {'total_recommendations': total_recs, 'total_profiles': total_profiles}

# ---- db_functions.py ----
# import sqlite3
# import pandas as pd
# from datetime import datetime
# import os
# import crop_data

# DB_NAME = "agriassist.db"
# ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
# DB_PATH = os.path.join(ROOT_DIR, DB_NAME)

# def get_db_connection():
#     return sqlite3.connect(DB_PATH)

# def setup_database():
#     conn = get_db_connection()
#     c = conn.cursor()
#     c.execute('''CREATE TABLE IF NOT EXISTS recommendations (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, nitrogen REAL, phosphorus REAL, potassium REAL, temperature REAL, humidity REAL, ph REAL, rainfall REAL, crop TEXT, status TEXT DEFAULT 'new')''')
#     c.execute('''CREATE TABLE IF NOT EXISTS profiles (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, farm_info TEXT, soil_type TEXT, preferences TEXT, last_updated DATETIME)''')
#     c.execute('''CREATE TABLE IF NOT EXISTS crops (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE, description TEXT, water_consumption TEXT, yield TEXT, image_path TEXT)''')
#     c.execute('''CREATE TABLE IF NOT EXISTS contacts (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, name TEXT, email TEXT, message TEXT, status TEXT DEFAULT 'new')''')
    
#     # --- NEW: Admin Profiles Table ---
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS admin_profiles (
#             id INTEGER PRIMARY KEY,
#             username TEXT UNIQUE,
#             password TEXT,
#             email TEXT,
#             last_updated DATETIME
#         )
#     ''')
#     # Add a default admin if one doesn't exist
#     c.execute("INSERT OR IGNORE INTO admin_profiles (id, username, password, email) VALUES (1, 'admin', 'admin123', 'admin@agriassist.com')")
    
#     conn.commit()
#     conn.close()

# # ... (All previous functions remain the same)

# # --- NEW: Functions for Admin Profile Management ---
# def get_admin_profile(admin_id=1):
#     """Retrieves the admin's profile data."""
#     conn = get_db_connection()
#     c = conn.cursor()
#     c.execute("SELECT username, email FROM admin_profiles WHERE id = ?", (admin_id,))
#     profile = c.fetchone()
#     conn.close()
#     if profile:
#         return {'username': profile[0], 'email': profile[1]}
#     return {'username': 'admin', 'email': ''}

# def update_admin_profile(username, email, new_password, admin_id=1):
#     """Updates the admin's profile data."""
#     conn = get_db_connection()
#     c = conn.cursor()
#     if new_password:
#         c.execute("UPDATE admin_profiles SET username=?, email=?, password=?, last_updated=? WHERE id=?", (username, email, new_password, datetime.now(), admin_id))
#     else:
#         # Don't update the password if it's empty
#         c.execute("UPDATE admin_profiles SET username=?, email=?, last_updated=? WHERE id=?", (username, email, datetime.now(), admin_id))
#     conn.commit()
#     conn.close()

# # --- All other functions (save_recommendation, get_history, etc.) are unchanged ---
# def save_recommendation(data, crop):
#     conn = get_db_connection()
#     c = conn.cursor()
#     c.execute("INSERT INTO recommendations (nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall, crop) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",(data['nitrogen'], data['phosphorus'], data['potassium'], data['temperature'], data['humidity'], data['ph'], data['rainfall'], crop))
#     new_id = c.lastrowid
#     conn.commit()
#     conn.close()
#     return new_id
# def mark_as_done(recommendation_id):
#     conn = get_db_connection()
#     c = conn.cursor()
#     c.execute("UPDATE recommendations SET status = 'done' WHERE id = ?", (recommendation_id,))
#     conn.commit()
#     conn.close()
# def get_history():
#     conn = get_db_connection()
#     try:
#         df = pd.read_sql_query("SELECT id, timestamp, nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall, crop, status FROM recommendations ORDER BY timestamp DESC", conn)
#     except pd.io.sql.DatabaseError: df = pd.DataFrame()
#     conn.close()
#     return df
# def clear_history():
#     conn = get_db_connection()
#     c = conn.cursor()
#     c.execute("DELETE FROM recommendations")
#     conn.commit()
#     conn.close()
# def get_dashboard_stats():
#     conn = get_db_connection()
#     try:
#         history_df = pd.read_sql_query("SELECT crop, timestamp FROM recommendations", conn)
#     except pd.io.sql.DatabaseError: history_df = pd.DataFrame()
#     conn.close()
#     if not history_df.empty:
#         total = len(history_df); unique_crops = history_df['crop'].nunique(); latest = pd.to_datetime(history_df['timestamp']).max().strftime('%Y-%m-%d')
#         return {'total': total, 'unique_crops': unique_crops, 'latest': latest}
#     return {'total': 0, 'unique_crops': 0, 'latest': 'N/A'}
# def get_crop_counts():
#     conn = get_db_connection()
#     try:
#         df = pd.read_sql_query("SELECT crop, COUNT(*) as count FROM recommendations GROUP BY crop ORDER BY count DESC", conn)
#     except pd.io.sql.DatabaseError: df = pd.DataFrame()
#     conn.close()
#     return df
# def save_profile_data(farm_info, soil_type, preferences):
#     conn = get_db_connection()
#     c = conn.cursor()
#     c.execute("INSERT OR REPLACE INTO profiles (id, farm_info, soil_type, preferences, last_updated) VALUES (?, ?, ?, ?, ?)", (1, farm_info, soil_type, preferences, datetime.now()))
#     conn.commit()
#     conn.close()
# def get_profile_data():
#     conn = get_db_connection()
#     c = conn.cursor()
#     try:
#         c.execute("SELECT farm_info, soil_type, preferences FROM profiles WHERE id = 1")
#         profile = c.fetchone()
#     except sqlite3.OperationalError: profile = None
#     conn.close()
#     if profile:
#         return {'farm_info': profile[0], 'soil_type': profile[1], 'preferences': profile[2]}
#     return {'farm_info': '', 'soil_type': 'Loamy', 'preferences': ''}
# def add_profile(name, email, farm_info, soil_type, preferences):
#     conn = get_db_connection()
#     c = conn.cursor()
#     c.execute("INSERT INTO profiles (name, email, farm_info, soil_type, preferences, last_updated) VALUES (?, ?, ?, ?, ?, ?)", (name, email, farm_info, soil_type, preferences, datetime.now()))
#     conn.commit()
#     conn.close()
# def get_all_profiles():
#     conn = get_db_connection()
#     try:
#         df = pd.read_sql_query("SELECT id, name, email, farm_info, soil_type, preferences FROM profiles", conn)
#     except pd.io.sql.DatabaseError: df = pd.DataFrame()
#     conn.close()
#     return df
# def update_profile(profile_id, name, email, farm_info, soil_type, preferences):
#     conn = get_db_connection()
#     c = conn.cursor()
#     c.execute("UPDATE profiles SET name=?, email=?, farm_info=?, soil_type=?, preferences=?, last_updated=? WHERE id=?", (name, email, farm_info, soil_type, preferences, datetime.now(), profile_id))
#     conn.commit()
#     conn.close()
# def delete_profile(profile_id):
#     conn = get_db_connection()
#     c = conn.cursor()
#     c.execute("DELETE FROM profiles WHERE id=?", (profile_id,))
#     conn.commit()
#     conn.close()
# def populate_crops_table_if_empty():
#     conn = get_db_connection()
#     c = conn.cursor()
#     c.execute("SELECT COUNT(*) FROM crops")
#     if c.fetchone()[0] == 0:
#         for crop_name, details in crop_data.CROP_DETAILS.items():
#             if crop_name != 'default':
#                 image_path = crop_data.CROP_IMAGES.get(crop_name, '')
#                 c.execute("INSERT INTO crops (name, description, water_consumption, yield, image_path) VALUES (?, ?, ?, ?, ?)", (crop_name.capitalize(), details['description'], details['water'], details['yield'], image_path))
#         conn.commit()
#     conn.close()
# def get_all_crops():
#     conn = get_db_connection()
#     try:
#         df = pd.read_sql_query("SELECT * FROM crops ORDER BY name", conn)
#     except pd.io.sql.DatabaseError: df = pd.DataFrame()
#     conn.close()
#     return df
# def add_crop(name, description, water, crop_yield, image_path):
#     conn = get_db_connection()
#     c = conn.cursor()
#     c.execute("INSERT INTO crops (name, description, water_consumption, yield, image_path) VALUES (?, ?, ?, ?, ?)",(name.capitalize(), description, water, crop_yield, image_path))
#     conn.commit()
#     conn.close()
# def update_crop(crop_id, name, description, water, crop_yield, image_path):
#     conn = get_db_connection()
#     c = conn.cursor()
#     c.execute("UPDATE crops SET name=?, description=?, water_consumption=?, yield=?, image_path=? WHERE id=?",(name.capitalize(), description, water, crop_yield, image_path, crop_id))
#     conn.commit()
#     conn.close()
# def delete_crop(crop_id):
#     conn = get_db_connection()
#     c = conn.cursor()
#     c.execute("DELETE FROM crops WHERE id=?", (crop_id,))
#     conn.commit()
#     conn.close()
# def save_contact_message(name, email, message):
#     conn = get_db_connection()
#     c = conn.cursor()
#     c.execute("INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)", (name, email, message))
#     conn.commit()
#     conn.close()
# def get_all_messages():
#     conn = get_db_connection()
#     try:
#         df = pd.read_sql_query("SELECT id, timestamp, name, email, message, status FROM contacts ORDER BY timestamp DESC", conn)
#     except pd.io.sql.DatabaseError: df = pd.DataFrame()
#     conn.close()
#     return df
# def get_admin_stats():
#     conn = get_db_connection()
#     try:
#         total_recs = pd.read_sql_query("SELECT COUNT(*) FROM recommendations", conn).iloc[0, 0]
#         total_profiles = pd.read_sql_query("SELECT COUNT(*) FROM profiles", conn).iloc[0, 0]
#     except (pd.io.sql.DatabaseError, IndexError):
#         total_recs, total_profiles = 0, 0
#     conn.close()
#     return {'total_recommendations': total_recs, 'total_profiles': total_profiles}


import sqlite3
import pandas as pd
from datetime import datetime
import os
import crop_data

# This ensures the database file is created in the main project folder
DB_NAME = "agriassist.db"
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(ROOT_DIR, DB_NAME)

def get_db_connection():
    """Establishes a connection to the database."""
    return sqlite3.connect(DB_PATH)

def setup_database():
    """Initializes the database and creates all tables if they don't exist."""
    conn = get_db_connection()
    c = conn.cursor()

    # Users Table (for login/signup)
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('Client', 'Admin'))
        )
    ''')

    # Recommendations Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            nitrogen REAL, phosphorus REAL, potassium REAL,
            temperature REAL, humidity REAL, ph REAL, rainfall REAL,
            crop TEXT,
            status TEXT DEFAULT 'new'
        )
    ''')
    # Profiles Table (for client and admin management)
    c.execute('''
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            farm_info TEXT,
            soil_type TEXT,
            preferences TEXT,
            last_updated DATETIME
        )
    ''')
    # Crops Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS crops (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            description TEXT,
            water_consumption TEXT,
            yield TEXT,
            image_path TEXT
        )
    ''')
    # Contacts Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            name TEXT,
            email TEXT,
            message TEXT,
            status TEXT DEFAULT 'new'
        )
    ''')
    conn.commit()
    conn.close()

# --- User Authentication Functions ---
def add_user(username, password_hash, role):
    """Adds a new user to the database."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", (username, password_hash, role))
    conn.commit()
    conn.close()

def get_user(username):
    """Retrieves a user's data from the database."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    if user:
        return {'id': user[0], 'username': user[1], 'password_hash': user[2], 'role': user[3]}
    return None

# --- Recommendation Functions ---
def save_recommendation(data, crop):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO recommendations (nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall, crop) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",(data['nitrogen'], data['phosphorus'], data['potassium'], data['temperature'], data['humidity'], data['ph'], data['rainfall'], crop))
    new_id = c.lastrowid
    conn.commit()
    conn.close()
    return new_id

def mark_as_done(recommendation_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("UPDATE recommendations SET status = 'done' WHERE id = ?", (recommendation_id,))
    conn.commit()
    conn.close()

def get_history():
    conn = get_db_connection()
    try:
        df = pd.read_sql_query("SELECT id, timestamp, nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall, crop, status FROM recommendations ORDER BY timestamp DESC", conn)
    except pd.io.sql.DatabaseError: df = pd.DataFrame()
    conn.close()
    return df

def clear_history():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM recommendations")
    conn.commit()
    conn.close()

# --- Dashboard/Insights Functions ---
def get_dashboard_stats():
    conn = get_db_connection()
    try:
        history_df = pd.read_sql_query("SELECT crop, timestamp FROM recommendations", conn)
    except pd.io.sql.DatabaseError: history_df = pd.DataFrame()
    conn.close()
    if not history_df.empty:
        total = len(history_df); unique_crops = history_df['crop'].nunique(); latest = pd.to_datetime(history_df['timestamp']).max().strftime('%Y-%m-%d')
        return {'total': total, 'unique_crops': unique_crops, 'latest': latest}
    return {'total': 0, 'unique_crops': 0, 'latest': 'N/A'}

def get_crop_counts():
    conn = get_db_connection()
    try:
        df = pd.read_sql_query("SELECT crop, COUNT(*) as count FROM recommendations GROUP BY crop ORDER BY count DESC", conn)
    except pd.io.sql.DatabaseError: df = pd.DataFrame()
    conn.close()
    return df

# --- Client Profile Functions ---
def save_profile_data(farm_info, soil_type, preferences):
    # This assumes a single-user mode for the client side for simplicity.
    # To support multiple clients, this would need a user_id.
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO profiles (id, farm_info, soil_type, preferences, last_updated) VALUES (?, ?, ?, ?, ?)", (1, farm_info, soil_type, preferences, datetime.now()))
    conn.commit()
    conn.close()

def get_profile_data():
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute("SELECT farm_info, soil_type, preferences FROM profiles WHERE id = 1")
        profile = c.fetchone()
    except sqlite3.OperationalError: profile = None
    conn.close()
    if profile:
        return {'farm_info': profile[0], 'soil_type': profile[1], 'preferences': profile[2]}
    return {'farm_info': '', 'soil_type': 'Loamy', 'preferences': ''}

# --- Admin User Management Functions ---
def add_profile(name, email, farm_info, soil_type, preferences):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO profiles (name, email, farm_info, soil_type, preferences, last_updated) VALUES (?, ?, ?, ?, ?, ?)", (name, email, farm_info, soil_type, preferences, datetime.now()))
    conn.commit()
    conn.close()

def get_all_profiles():
    conn = get_db_connection()
    try:
        df = pd.read_sql_query("SELECT id, name, email, farm_info, soil_type, preferences FROM profiles", conn)
    except pd.io.sql.DatabaseError: df = pd.DataFrame()
    conn.close()
    return df

def update_profile(profile_id, name, email, farm_info, soil_type, preferences):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("UPDATE profiles SET name=?, email=?, farm_info=?, soil_type=?, preferences=?, last_updated=? WHERE id=?", (name, email, farm_info, soil_type, preferences, datetime.now(), profile_id))
    conn.commit()
    conn.close()

def delete_profile(profile_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM profiles WHERE id=?", (profile_id,))
    conn.commit()
    conn.close()

# --- Admin Crop Management Functions ---
def populate_crops_table_if_empty():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM crops")
    if c.fetchone()[0] == 0:
        for crop_name, details in crop_data.CROP_DETAILS.items():
            if crop_name != 'default':
                image_path = crop_data.CROP_IMAGES.get(crop_name, '')
                c.execute("INSERT INTO crops (name, description, water_consumption, yield, image_path) VALUES (?, ?, ?, ?, ?)", (crop_name.capitalize(), details['description'], details['water'], details['yield'], image_path))
        conn.commit()
    conn.close()

def get_all_crops():
    conn = get_db_connection()
    try:
        df = pd.read_sql_query("SELECT * FROM crops ORDER BY name", conn)
    except pd.io.sql.DatabaseError: df = pd.DataFrame()
    conn.close()
    return df

def add_crop(name, description, water, crop_yield, image_path):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO crops (name, description, water_consumption, yield, image_path) VALUES (?, ?, ?, ?, ?)",(name.capitalize(), description, water, crop_yield, image_path))
    conn.commit()
    conn.close()

def update_crop(crop_id, name, description, water, crop_yield, image_path):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("UPDATE crops SET name=?, description=?, water_consumption=?, yield=?, image_path=? WHERE id=?",(name.capitalize(), description, water, crop_yield, image_path, crop_id))
    conn.commit()
    conn.close()

def delete_crop(crop_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM crops WHERE id=?", (crop_id,))
    conn.commit()
    conn.close()

# --- Support/Contact Functions ---
def save_contact_message(name, email, message):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)", (name, email, message))
    conn.commit()
    conn.close()

def get_all_messages():
    conn = get_db_connection()
    try:
        df = pd.read_sql_query("SELECT id, timestamp, name, email, message, status FROM contacts ORDER BY timestamp DESC", conn)
    except pd.io.sql.DatabaseError: df = pd.DataFrame()
    conn.close()
    return df

# --- Admin Stats Function ---
def get_admin_stats():
    conn = get_db_connection()
    try:
        total_recs = pd.read_sql_query("SELECT COUNT(*) FROM recommendations", conn).iloc[0, 0]
        total_profiles = pd.read_sql_query("SELECT COUNT(*) FROM profiles", conn).iloc[0, 0]
    except (pd.io.sql.DatabaseError, IndexError):
        total_recs, total_profiles = 0, 0
    conn.close()
    return {'total_recommendations': total_recs, 'total_profiles': total_profiles}

