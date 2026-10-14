def convert_row(row):
        integer_fields = ["age", "number_of_profiles", "last_login_days", "churned"]
        float_fields = ["watch_hours", "monthly_fee", "avg_watch_time_per_day"]
        for field in integer_fields:
            row[field] = int(row[field])
        for field in float_fields:
            row[field] = float(row[field])
        return row