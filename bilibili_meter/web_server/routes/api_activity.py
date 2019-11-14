from flask import Blueprint, jsonify, request
import time
import logging
from ..model import WebUser, WatchedUser, WatchedVideo, Task, TaskStatus,\
                ItemOnline, ItemVideoStat, ItemUpStat, ItemRegionActivity,\
                TaskFailed,TotalWatchedUser,TotalWatchedVideo,TotalEnabledTask,\
                WorkerStatus
from .. import orm
from ..utils import get_zero_timestamp
main = Blueprint('api_activity', __name__)


@main.route('/get')
def get_activity():
    # byday = request.values.get('byday', None)
    # if not byday:
    c_items = ItemRegionActivity.findAll(limit=500, orderBy='id DESC')
    c_items.reverse()
    # else:
    byday_items = ItemRegionActivity.findByDay(need_key='id', need_filter='MAX(`id`)')
    byday_items.reverse()

    # 清理不必要字段
    for i in c_items:
        del i['id']
        del i['task_id']
        i['rawtime']=i['time']

    for i in byday_items:
        del i['id']
        del i['task_id']
        i['rawtime']=i['time']
        i['time']=get_zero_timestamp(i['time'])

    d = dict()
    d['data'] = {'c':c_items,'byday':byday_items}
    return jsonify(d)


