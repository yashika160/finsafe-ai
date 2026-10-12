import pandas as pd
import numpy as np

df = pd.read_csv("data/processed/features_daily.csv", parse_dates=["transaction_date"])
train = df[df["transaction_date"] < "2023-10-01"]
test = df[df["transaction_date"] >= "2023-10-01"]
print("Train rows:", len(train), "| Test rows:", len(test))

actual = test["daily_net"]

def score(name, predicted):
    errors = predicted - actual
    mae = errors.abs().mean()
    rmse = np.sqrt((errors ** 2).mean())
    print(f"{name:28s} MAE={mae:9.2f}  RMSE={rmse:9.2f}")

score("A: predict 0 every day", pd.Series(0.0, index=test.index))
score("B: train average", pd.Series(train["daily_net"].mean(), index=test.index))
score("C: last-7-day average", test["rolling_mean_7"])
print("Zero-net days in test:", (actual == 0).sum(), "of", len(actual))
print(actual.abs().sort_values(ascending=False).head(5))