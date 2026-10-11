import pandas as pd

daily = pd.read_csv("data/processed/transactions_daily.csv", parse_dates=["transaction_date"])

# --- Lag features: values from the past ---
daily["balance_lag_1"] = daily["end_of_day_balance"].shift(1)
daily["balance_lag_7"] = daily["end_of_day_balance"].shift(7)

# --- Rolling features: summarize the PAST 7 days ---
# shift(1) first, so today's own value is NOT inside its own average
past_net = daily["daily_net"].shift(1)
daily["rolling_mean_7"] = past_net.rolling(7).mean()
daily["rolling_std_7"] = past_net.rolling(7).std()

# --- Calendar features: come straight from the date, no history needed ---
daily["day_of_month"] = daily["transaction_date"].dt.day
daily["day_of_week"] = daily["transaction_date"].dt.dayofweek   # Monday=0 ... Sunday=6
daily["is_month_start"] = daily["transaction_date"].dt.is_month_start.astype(int)

print(daily[["transaction_date", "daily_net", "rolling_mean_7", "rolling_std_7"]].head(10))
print()
print(daily[["transaction_date", "day_of_month", "day_of_week", "is_month_start"]].head(5))
# Drop the first rows where lag/rolling features can't exist yet
feature_cols = ["balance_lag_1", "balance_lag_7", "rolling_mean_7", "rolling_std_7"]
before = len(daily)
daily = daily.dropna(subset=feature_cols).reset_index(drop=True)
print(f"Rows before: {before}, after dropping incomplete rows: {len(daily)}")

daily.to_csv("data/processed/features_daily.csv", index=False)