from flask import session
from ..model import WebUser
from ...config import PW
import hashlib

def current_user():
    uid = session.get('user_id','')
    if uid:
        u = WebUser.find(uid)
        return u
    else:
        return None
