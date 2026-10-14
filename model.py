
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    ConfusionMatrixDisplay,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from database import get_connection


# 1. Load customer data from SQLite
conn = get_connection()

df = pd.read_sql_query("""
    SELECT
        subscription_type,
        watch_hours,
        last_login_days,
        monthly_fee,
        number_of_profiles,
        avg_watch_time_per_day,
        churned
    FROM customers
""", conn)

conn.close()


# 2. Separate independent and dependent variables
X = df.drop(columns=["churned"])
y = df["churned"]

numeric_features = [
    "watch_hours",
    "last_login_days",
    "monthly_fee",
    "number_of_profiles",
    "avg_watch_time_per_day",
]

categorical_features = ["subscription_type"]


# 3. Prepare the features
numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
])

categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore")),
])

preprocessor = ColumnTransformer([
    ("numeric", numeric_pipeline, numeric_features),
    ("categorical", categorical_pipeline, categorical_features),
])


# 4. Split customers into training and testing data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y,
)


# 5. Build and train logistic regression
model = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression(max_iter=1000)),
])

model.fit(X_train, y_train)


# 6. Make predictions on unseen test customers
predictions = model.predict(X_test)


# 7. Evaluate the model
print("Training customers:", len(X_train))
print("Testing customers:", len(X_test))
print(f"Accuracy: {accuracy_score(y_test, predictions):.2%}")

print("\nClassification report:")
print(classification_report(y_test, predictions, zero_division=0))


# 8. Save a confusion matrix for the poster
ConfusionMatrixDisplay.from_predictions(
    y_test,
    predictions,
    display_labels=["Stayed", "Churned"],
    cmap="Blues",
    values_format="d",
)

plt.title("Netflix Churn Prediction — Logistic Regression")
plt.tight_layout()
plt.savefig("confusion_matrix.png", dpi=300)
plt.close()

print("\nSaved confusion_matrix.png")
