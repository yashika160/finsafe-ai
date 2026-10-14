import pandas as pd

t = pd.read_csv("data/processed/transactions_clean.csv", parse_dates=["transaction_date"])
rest = t[~t["category"].isin(["Salary", "Rent"])].copy()
rest["net"] = rest["deposit"] - rest["withdrawal"]
days = pd.date_range(t["transaction_date"].min(), t["transaction_date"].max(), freq="D")
daily_rest = rest.groupby("transaction_date")["net"].sum().reindex(days).fillna(0)

monthly = daily_rest.resample("MS").sum()
monthly = monthly[monthly.index < "2024-01-01"]      # drop Jan 2024: it is only 1 day

rows = []
for i in range(3, len(monthly)):                      # need at least 3 past months
    past = monthly.iloc[:i]                           # ONLY months before the one we predict
    actual = monthly.iloc[i]
    rows.append({
        "month": monthly.index[i].strftime("%b"),
        "actual": actual,
        # error = prediction - actual.  POSITIVE = we were too optimistic (predicted less spending)
        "A_last_month": past.iloc[-1] - actual,
        "B_median_all": past.median() - actual,
        "C_mean_last3": past.tail(3).mean() - actual,
    })

res = pd.DataFrame(rows).set_index("month")
cols = ["A_last_month", "B_median_all", "C_mean_last3"]
print(res.round(0))
print()
print("Average size of error (MAE):")
print(res[cols].abs().mean().round(0))
print()
print("Months we were too optimistic (error > 0):")
print((res[cols] > 0).sum())
print("Worst optimistic miss:")
print(res[cols].max().round(0))