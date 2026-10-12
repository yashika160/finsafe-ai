import pandas as pd

GRACE_DAYS = 3      # design choice: how many days late before we call an event "overdue"
N_RECENT = 3        # design choice: how many recent amounts to look at


def get_events(transactions, category, amount_col):
    """All past events of one category (e.g. Salary uses 'deposit', Rent uses 'withdrawal')."""
    ev = transactions[(transactions["category"] == category) & (transactions[amount_col] > 0)]
    ev = ev.sort_values("transaction_date")
    return ev[["transaction_date", amount_col]].rename(columns={amount_col: "amount"})


def expected_next(events, today):
    """Predict the next occurrence of a recurring event, and say whether it is overdue."""
    today = pd.Timestamp(today)
    last_date = events["transaction_date"].iloc[-1]

    # WHEN: the usual day of the month (median is robust to one odd month)
    day = min(int(events["transaction_date"].dt.day.median()), 28)   # 28 avoids short-month errors
    next_date = (last_date + pd.offsets.MonthBegin(1)).replace(day=day)

    # HOW MUCH: the LOWEST of the recent amounts (conservative design choice for income)
    amount = float(events["amount"].tail(N_RECENT).min())

    # IS IT LATE?
    status = "overdue" if today > next_date + pd.Timedelta(days=GRACE_DAYS) else "expected"
    return {"expected_date": next_date.date(), "expected_amount": amount, "status": status}