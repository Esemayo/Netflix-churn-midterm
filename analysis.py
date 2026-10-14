import csv
import sqlite3
from validation.cleaner import validate_row
from validation.converter import convert_row
from database import get_connection, create_table, insert_customer
from queries import count_customers, churn_comparison, subscription_churn, churn_by_inactivity, churn_by_watch_hours
with open("data/netflix_customer_churn.csv") as dataset:
    reader = csv.DictReader(dataset)
    empty_entry_check = []
    seen_ids = set()
    duplicate_ids = []
    invalid_rows = []
    conn = get_connection()
    create_table(conn)
    for row in reader:
        if row["customer_id"] not in seen_ids:
            seen_ids.add(row["customer_id"])
        else:
            duplicate_ids.append(row["customer_id"])
        for value in row.values():
            if value == "":
                empty_entry_check.append(row["customer_id"])
                break
            errors = validate_row(row)
            if errors:
                    invalid_rows.append({
                        "value": value,
                        "errors": errors
                        })
            else: 
                converted_row = convert_row(row)
                try: 
                    insert_customer(conn, converted_row)
                except sqlite3.IntegrityError:
                    pass
    if not empty_entry_check:
        print("No empty rows")
    if not duplicate_ids:
        print("No duplicate customer IDs")
    if not invalid_rows:
        print("No invalid rows")
    total_customers = count_customers(conn)
    print(total_customers)
    churn_result = churn_comparison(conn)
    print(churn_result)
    churn_rate = churn_result[1][1] / total_customers * 100
    print(churn_rate)
    subscription_churn_rate = subscription_churn(conn)
    subscription_totals = {}
    subscription_churned = {}
    for subscription, churned, count in subscription_churn_rate:
        subscription_totals[subscription] = subscription_totals.get(subscription, 0) + count
        print(subscription, churned, count)
        if churned == 1:
            subscription_churned[subscription] = count 
    for subscription in subscription_totals:
        subscription_churn_rate = subscription_churned[subscription] / subscription_totals[subscription] * 100
        print(f"{subscription} {subscription_churn_rate:.2f}%")
    print("Churn by inactivity:")
    for row in churn_by_inactivity(conn):
        print(row)
    print("Churn by watch hours:")
    for row in churn_by_watch_hours(conn):
        print(row)
    conn.commit()
    conn.close()
    
    
        

        