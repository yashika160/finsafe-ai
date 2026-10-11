"""
Phase 1 cleaning pipeline for FinSafe's real transaction data.
Decisions made (documented, not silent):
  - Drop the single fully-blank row and the 3 exact duplicate rows (certain fixes, done first).
  - Date: parse `Date` as primary; where it fails, fall back to `Date.1`. Drop `Date.1` after.
    Known limitation: a handful of rows may be off by 1 day due to mixed source formats -
    acceptable since forecasting is done at a weekly/monthly granularity.
  - RefNo: cast to string to stop scientific-notation display (it's an ID, not a number to do math on).
  - Large Withdrawal outliers (e.g. ~21000): kept as genuine data, not treated as errors -
    no duplicate/impossible-value evidence they're wrong, and FinSafe specifically needs to
    handle rare large real expenses, not hide them.
"""
import pandas as pd

RAW_PATH = "data/raw/transactions_raw.csv"
OUT_PATH = "data/processed/transactions_clean.csv"

df = pd.read_csv(RAW_PATH, dtype={"RefNo": "string"})
start_rows = len(df)

# 1. Drop the fully blank row (certain fix)
df = df.dropna(how="all")

# 2. Drop exact duplicate rows (certain fix)
dupes_removed = df.duplicated().sum()
df = df.drop_duplicates()

# 3. Resolve the Date vs Date.1 mismatch
date_primary = pd.to_datetime(df["Date"], dayfirst=True, format="mixed", errors="coerce")
date_fallback = pd.to_datetime(df["Date.1"], dayfirst=True, format="mixed", errors="coerce")
df["transaction_date"] = date_primary.fillna(date_fallback)
still_missing_dates = df["transaction_date"].isna().sum()
df = df.drop(columns=["Date", "Date.1"])

# 4. Tidy column names and types
df = df.rename(columns={
    "Category": "category",
    "RefNo": "ref_no",
    "Withdrawal": "withdrawal",
    "Deposit": "deposit",
    "Balance": "balance",
})
df = df.sort_values("transaction_date").reset_index(drop=True)

import os
os.makedirs("data/processed", exist_ok=True)
df.to_csv(OUT_PATH, index=False)

print(f"Start rows: {start_rows}")
print(f"Blank/duplicate rows removed: {start_rows - len(df) - still_missing_dates}")
print(f"Duplicate rows found: {dupes_removed}")
print(f"Rows where date still couldn't be parsed: {still_missing_dates}")
print(f"Final rows: {len(df)}")
print(f"Date range: {df['transaction_date'].min()} to {df['transaction_date'].max()}")
print()
print(df.head(5).to_string())