import hashlib
import time

from . import  config

# _SCRAPER_NAME = config.SCRAPER_NAME
_TOKEN = config.TOKEN
_TIME_DIVIDER = config._TOKEN_TIME_DIVIDER

def make_token(name, id=None, time_offset=0):
    '''
    name : str  id : str or int
    if don't have id, use name
    '''
    if not id:
        id = name
    t = str(int(time.time() // _TIME_DIVIDER) + time_offset)
    w = (name + str(id) +_TOKEN+ str(id) + name[::-1] + t).encode('utf-8')
    x = hashlib.sha1(w)
    return x.hexdigest()

def get_three_tokens(name,id):
    return [
        make_token(name,id,-1),
        make_token(name,id,0),
        make_token(name,id,1),
    ]