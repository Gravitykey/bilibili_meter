from flask import Blueprint, jsonify, request
import time
import logging
from ..model import WebUser, WatchedUser, WatchedVideo, Task, TaskStatus,\
                ItemOnline, ItemVideoStat, ItemUpStat, ItemRegionActivity,\
                TaskFailed,TotalWatchedUser,TotalWatchedVideo,TotalEnabledTask,\
                WorkerStatus
from .. import orm
from ... import token

from . import _task
main = Blueprint('api_scraper', __name__)

# 认证失败返回的json
auth_failed = {'status': 'error', 'message': 'invalid token'}

def auth(name,id=None):
    # print(name,id)
    if not id:
        id = name
    if name and id:
        t = request.values.get('token', None)
        tokens = token.get_three_tokens(name=name, id=id)
        # print (tokens)
        return t in tokens
    else:
        return False


@main.route('/gettasks')
def get_tasks():
    scraper_name = request.values.get('scraper_name', None)
    if not auth(scraper_name):
        return jsonify(auth_failed)

    ret = {
        'status': 'success',
        'tasklist': _task.distribute_tasks(scraper_name)
    }
    WorkerStatus.add_one(time.time(), scraper_name)
    return jsonify(ret)


@main.route('/submittask')
def submit_task():
    scraper_name = request.values.get('scraper_name', None)
    task_id = request.values.get('task_id', None)
    if not auth(scraper_name,task_id):
        return jsonify(auth_failed)

    d = {k: v for k, v in request.values.items()}
    _task.receive_item(d['task_id'], d['scraper_name'], d['type'], d)
    WorkerStatus.add_one(time.time(), scraper_name, act='submit')
    return jsonify({'status':'success'})


@main.route('/submitfailure')
def submit_failure():
    scraper_name = request.values.get('scraper_name', None)
    task_id = request.values.get('task_id', None)
    if not auth(scraper_name,task_id):
        return jsonify(auth_failed)

    _task.receive_failure(task_id,scraper_name)
    return jsonify({'status':'success'})
    
