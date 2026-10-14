import pandas as pd

t = pd.read_csv("data/processed/transactions_clean.csv", parse_dates=["transaction_date"])

# Everything that is NOT salary or rent = the "irregular remainder"
rest = t[~t["category"].isin(["Salary", "Rent"])].copy()
rest["net"] = rest["deposit"] - rest["withdrawal"]

days = pd.date_range(t["transaction_date"].min(), t["transaction_date"].max(), freq="D")
daily_rest = rest.groupby("transaction_date")["net"].sum().reindex(days).fillna(0)

print("Monthly net of irregular spending:")
print(daily_rest.resample("MS").sum().round(0))

last30 = daily_rest.rolling(30).sum().dropna()
print("\n30-day totals -> 10th / 50th / 90th percentile:")
print(last30.quantile([0.1, 0.5, 0.9]).round(0))