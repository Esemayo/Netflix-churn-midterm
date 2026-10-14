
import matplotlib.pyplot as plt

# Chart 1: Overall customer churn
labels = ["Stayed", "Churned"]
counts = [2485, 2515]

plt.figure(figsize=(7, 5))
bars = plt.bar(labels, counts, color=["steelblue", "coral"])

plt.title("Overall Netflix Customer Churn")
plt.ylabel("Number of Customers")
plt.ylim(0, 3000)

for bar in bars:
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 50,
        str(int(bar.get_height())),
        ha="center"
    )

plt.tight_layout()
plt.savefig("overall_churn.png", dpi=300)
plt.close()


# Chart 2: Churn rate by subscription type
subscriptions = ["Basic", "Standard", "Premium"]
churn_rates = [61.83, 45.44, 43.71]

plt.figure(figsize=(8, 5))
bars = plt.bar(
    subscriptions,
    churn_rates,
    color=["coral", "steelblue", "seagreen"]
)

plt.title("Customer Churn Rate by Subscription")
plt.ylabel("Churn Rate (%)")
plt.ylim(0, 75)

for bar in bars:
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 1,
        f"{bar.get_height():.1f}%",
        ha="center"
    )

plt.tight_layout()
plt.savefig("subscription_churn.png", dpi=300)
plt.close()

print("Both charts saved successfully!")
