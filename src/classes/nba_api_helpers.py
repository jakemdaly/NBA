import datetime as dt
from dateutil.relativedelta import relativedelta
import time

import requests
import urllib3


def get_age(age_str):
    age1 = dt.datetime.fromisoformat(age_str)
    age2 = dt.datetime.now()
    delta = relativedelta(age2, age1)
    age = delta.years + delta.months/12
    return age

def get_season_str_YY(year_that_needs_converting_int):
    year_str = str(year_that_needs_converting_int)[2:]

    # NEED TO RETURN AS STRING BECAUSE CAN'T RETURN 00 as int

    return year_str

def try_request(api_call, number_tries=5):

    sleep_time = 5
    tries_left = number_tries

    if tries_left == 1:
        print("Final try...")
        return api_call
    else:
        try:
            api_call
        except (urllib3.exceptions.ReadTimeoutError, requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
            print("Caught exception in Endpoint request... Waiting {} seconds to try again".format(sleep_time))
            time.sleep(sleep_time)
            try_request(api_call, tries_left-1)