def validate_row(row):
    errors = []
    categories = {
        "gender": {"Female", "Male", "Other"},
        "subscription_type": {"Basic", "Standard", "Premium"},
        "region": {"Africa", "Asia", "Europe", "North America", "Oceania", "South America"},
        "device": {"TV", "Mobile", "Laptop", "Tablet", "Desktop"},
        "payment_method": {"Debit Card", "PayPal", "Crypto", "Gift Card", "Credit Card"},
        "favorite_genre": {"Drama", "Documentary", "Romance", "Sci-Fi", "Horror", "Comedy", "Action"}
    }
    for column in categories:
        if row[column] not in categories[column]:
            errors.append(f"Invalid {column}")     
    integer_fields = ["age", "number_of_profiles", "last_login_days", "churned"]
    for field in integer_fields:
        try:
            int(row[field])
        except ValueError:
            errors.append(f"Invalid{field}")
    float_fields = ["watch_hours", "monthly_fee", "avg_watch_time_per_day"]
    for field in float_fields:
        try:
            float(row[field])
        except ValueError:
            errors.append(f"Invalid{field}")
    return errors
    