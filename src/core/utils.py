import datetime


def utc_now() -> datetime.datetime:
    return datetime.datetime.now(tz=datetime.UTC)


def today() -> datetime.date:
    return utc_now().date()
