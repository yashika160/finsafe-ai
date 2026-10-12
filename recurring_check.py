import pandas as pd

t = pd.read_csv("data/processed/transactions_clean.csv", parse_dates=["transaction_date"])

def summarize(category, amount_col):
    ev = t[(t["category"] == category) & (t[amount_col] > 0)].sort_values("transaction_date")
    gaps = ev["transaction_date"].diff().dt.days.dropna()
    print(f"--- {category} ---")
    print("events:", len(ev))
    print("gap in days between events -> median:", gaps.median(), "| min:", gaps.min(), "| max:", gaps.max())
    print("day of month -> median:", ev["transaction_date"].dt.day.median(),
          "| min:", ev["transaction_date"].dt.day.min(), "| max:", ev["transaction_date"].dt.day.max())
    print("amount -> median:", ev[amount_col].median(), "| min:", ev[amount_col].min(), "| max:", ev[amount_col].max())
    print()

summarize("Salary", "deposit")
summarize("Rent", "withdrawal")