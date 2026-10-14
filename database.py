import sqlite3
def get_connection():
    conn = sqlite3.connect("netflix.db")
    return conn
def create_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
    customer_id TEXT PRIMARY KEY,
    age INTEGER,
    gender TEXT,
    subscription_type TEXT,
    watch_hours REAL,
    last_login_days INTEGER,
    region TEXT,
    device TEXT,
    monthly_fee REAL,
    churned INTEGER,
    payment_method TEXT,
    number_of_profiles INTEGER,
    avg_watch_time_per_day REAL,
    favorite_genre TEXT
    )
    """)
def insert_customer(conn, converted_row):
    cursor = conn.cursor()
    values = (
        converted_row["customer_id"],
        converted_row["age"],
        converted_row["gender"],
        converted_row["subscription_type"],
        converted_row["watch_hours"],
        converted_row["last_login_days"],
        converted_row["region"],
        converted_row["device"],
        converted_row["monthly_fee"],
        converted_row["churned"],
        converted_row["payment_method"],
        converted_row["number_of_profiles"],
        converted_row["avg_watch_time_per_day"],
        converted_row["favorite_genre"]
    )
    cursor.execute("""
        INSERT OR IGNORE INTO customers (
        customer_id,
        age,
        gender,
        subscription_type,
        watch_hours,
        last_login_days,
        region,
        device,
        monthly_fee,
        churned,
        payment_method,
        number_of_profiles,
        avg_watch_time_per_day,
        favorite_genre)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, values)

    