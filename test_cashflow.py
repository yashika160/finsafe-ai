import pandas as pd
from financial_engine.cashflow import forecast_cashflow

t = pd.read_csv("data/processed/transactions_clean.csv", parse_dates=["transaction_date"])

def balance_on(day):
    return t[t["transaction_date"] <= day]["balance"].iloc[-1]

for today, horizon in [("2023-09-30", 30), ("2023-10-30", 30)]:
    print(f"--- today={today}, horizon={horizon} days ---")
    result = forecast_cashflow(t, balance_on(today), today, horizon)
    for k, v in result.items():
        print(f"{k:28s} {v}")
    print()