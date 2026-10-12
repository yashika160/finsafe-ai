import pandas as pd
from forecasting.recurring import get_events, expected_next

t = pd.read_csv("data/processed/transactions_clean.csv", parse_dates=["transaction_date"])
salary = get_events(t, "Salary", "deposit")

# Test 1: full history, checking on Dec 1
print("Test 1:", expected_next(salary, "2023-12-01"))

# Test 2: pretend it is Oct 30 and we only know salaries up to Sep (the missing-October case)
before_oct = salary[salary["transaction_date"] < "2023-10-01"]
print("Test 2:", expected_next(before_oct, "2023-10-30"))