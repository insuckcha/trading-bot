from datetime import datetime, timedelta


def parse_interval(interval_str):
    if interval_str.endswith("min"):
        return int(interval_str[:-3]), "minute"
    elif interval_str.endswith("hour"):
        return int(interval_str[:-4]), "hour"
    elif interval_str.endswith("day"):
        return int(interval_str[:-3]), "day"
    else:
        return 1, "minute"


def get_date_range(limit, interval):
    today = datetime.today()
    if interval.endswith("min"):
        start = today
    elif interval.endswith("hour"):
        trading_days_needed = int(limit / 6.5) + 1
        calendar_days = int(trading_days_needed * 1.4)
        start = today - timedelta(days=calendar_days)
    elif interval.endswith("day"):
        calendar_days = int(limit / 0.7)
        start = today - timedelta(days=calendar_days)
    elif interval.endswith("week"):
        start = today - timedelta(weeks=limit + 2)
    else:
        start = today
    return start.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")
