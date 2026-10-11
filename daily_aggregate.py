"""
Phase 1 - collapse cleaned transactions (one row per transaction)
into one row per day (what the forecaster actually needs).
Run from the finsafe-ai/ project root:  python daily_aggregate.py
"""
import pandas as pd

df = pd.read_csv("data/processed/transactions_clean.csv", parse_dates=["transaction_date"])

daily = df.groupby("transaction_date").agg(
    total_withdrawal=("withdrawal", "sum"),
    total_deposit=("deposit", "sum"),
    end_of_day_balance=("balance", "last"),  # snapshot: last reading of the day, never summed
    num_transactions=("balance", "count"),
).reset_index()

daily["daily_net"] = daily["total_deposit"] - daily["total_withdrawal"]
daily = daily.sort_values("transaction_date").reset_index(drop=True)

# Reindex to EVERY calendar day so "shift by 1 row" == "shift by 1 day"
full_range = pd.date_range(daily["transaction_date"].min(), daily["transaction_date"].max(), freq="D")
daily = daily.set_index("transaction_date").reindex(full_range)
daily.index.name = "transaction_date"

# No-transaction days: flows are genuinely 0
daily[["total_withdrawal", "total_deposit", "daily_net", "num_transactions"]] = (
    daily[["total_withdrawal", "total_deposit", "daily_net", "num_transactions"]].fillna(0)
)
# Balance is a snapshot: it stays whatever it last was -> forward-fill
daily["end_of_day_balance"] = daily["end_of_day_balance"].ffill()

daily = daily.reset_index()
daily.to_csv("data/processed/transactions_daily.csv", index=False)

print(f"Days in dataset: {len(daily)}")
print(daily.head(5).to_string(index=False))