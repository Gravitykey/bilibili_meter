from flask import Blueprint, jsonify
import time
import logging
from ..model import WebUser, WatchedUser, WatchedVideo, Task, TaskStatus,\
                ItemOnline, ItemVideoStat, ItemUpStat, ItemRegionActivity,\
                TaskFailed,TotalWatchedUser,TotalWatchedVideo,TotalEnabledTask,\
                WorkerStatus

main = Blueprint('api_stat', __name__)


@main.route('/get')
def get_stat():
    d = dict()
    d['total_user'] = TotalWatchedUser.get_total()
    d['total_video'] = TotalWatchedVideo.get_total()
    d['total_enabled_task'] = TotalEnabledTask.get_total()
    d['today_task_failed'] = TaskFailed.count_today()
    # 统计总提交数
    ws = WorkerStatus.get_today()
    today_submit = 0
    for i in ws:
        today_submit += i.day_submit_count
        del i['id']
    d['today_submit'] = today_submit
    d['workers_stat'] = ws

    return jsonify(d)