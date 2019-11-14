from flask import Blueprint, jsonify, request, abort, session
import time
import logging
from ..model import WebUser, WatchedUser, WatchedVideo, Task, TaskStatus,\
                ItemOnline, ItemVideoStat, ItemUpStat, ItemRegionActivity,\
                TaskFailed,TotalWatchedUser,TotalWatchedVideo,TotalEnabledTask,\
                WorkerStatus

from . import current_user
main = Blueprint('api_login', __name__)


@main.route('/getstat')
def get_login_stat():
    u = current_user()
    d = dict()
    if u:
        d['logged_in'] = True
        d['name'] = u.name
        d['admin'] = u.admin
    else:
        d['logged_in'] = False

    return jsonify(d)


@main.route('/auth')
def login():
    username = request.values.get('username', None)
    password = request.values.get('password', None)
    # print(username,password)
    if not (username and password):
        return jsonify(message='error')
    u = WebUser.auth(username, password)
    if not u:
        return jsonify(message='failed')
    else:
        session['user_id'] = u.id
        session.permanent = True
    return jsonify(message='success', name=u.name, admin=u.admin)

@main.route('/logout')
def logout():
    session.pop('user_id',None)
    return jsonify(message='ok')