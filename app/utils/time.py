from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))

def now_kst():
    return datetime.now(KST)
