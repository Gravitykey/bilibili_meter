import time

def now_date_to_str():
    return time.strftime('%Y-%m-%d',time.localtime())

def date_to_str(t):
    return time.strftime('%Y-%m-%d',time.localtime(t))

def get_zero_timestamp(x=None):
    if not x:
        t = time.time()
    else:
        t = int(x)
    return t - ( t- time.timezone) %86400
