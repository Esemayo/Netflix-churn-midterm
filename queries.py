def count_customers(conn):
    cursor = conn.cursor()
    cursor.execute ("""
        SELECT COUNT(*) FROM customers 
    """)
    results = cursor.fetchone()
    return results[0]
def churn_comparison(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT churned, COUNT(*)
        FROM customers
        GROUP BY churned
    """)
    results = cursor.fetchall()
    return results
def subscription_churn(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT subscription_type, churned, COUNT(*)
        FROM customers
        GROUP BY subscription_type, churned;
    """)
    results = cursor.fetchall()
    return results
def churn_by_inactivity(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            CASE
                WHEN last_login_days <= 7 THEN '0-7 days'
                WHEN last_login_days <= 30 THEN '8-30 days'
                ELSE '31+ days'
            END AS inactivity_group,
            COUNT(*) AS total,
            SUM(churned) AS churned_count,
            ROUND(AVG(churned) * 100, 2) AS churn_rate
        FROM customers
        GROUP BY inactivity_group
        ORDER BY MIN(last_login_days)
    """)
    return cursor.fetchall()


def churn_by_watch_hours(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            CASE
                WHEN watch_hours < 10 THEN 'Under 10 hours'
                WHEN watch_hours < 30 THEN '10-29 hours'
                ELSE '30+ hours'
            END AS watch_group,
            COUNT(*) AS total,
            SUM(churned) AS churned_count,
            ROUND(AVG(churned) * 100, 2) AS churn_rate
        FROM customers
        GROUP BY watch_group
        ORDER BY MIN(watch_hours)
    """)
    return cursor.fetchall()
