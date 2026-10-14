# All tunable design choices live here, not scattered through the code.
# These are DESIGN CHOICES (assumptions), not facts about the data.

GRACE_DAYS = 3             # days late before a recurring event is called "overdue"
N_RECENT = 3               # how many recent amounts to look at for a recurring event
BAD_CASE_QUANTILE = 0.10   # bad case = the 10th percentile of past spending periods
MIN_HISTORY_DAYS = 60      # refuse to forecast with less history than this