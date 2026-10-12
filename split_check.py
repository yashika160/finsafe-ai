import pandas as pd

df = pd.read_csv("data/processed/features_daily.csv", parse_dates=["transaction_date"])

split_date = "2023-10-01"
train = df[df["transaction_date"] < split_date]
test = df[df["transaction_date"] >= split_date]

print("Train rows:", len(train), "|", train["transaction_date"].min().date(), "to", train["transaction_date"].max().date())
print("Test rows: ", len(test), "|", test["transaction_date"].min().date(), "to", test["transaction_date"].max().date())