import datetime as dt
from dateutil.relativedelta import relativedelta

def get_age(age_str):
    age1 = dt.datetime.fromisoformat(age_str)
    age2 = dt.datetime.now()
    delta = relativedelta(age2, age1)
    age = delta.years + delta.months/12
    return age