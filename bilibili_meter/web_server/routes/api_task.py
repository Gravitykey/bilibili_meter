from flask import Blueprint, jsonify, request, abort
import time
import logging
from ..model import WebUser, WatchedUser, WatchedVideo, Task, TaskStatus,\
                ItemOnline, ItemVideoStat, ItemUpStat, ItemRegionActivity,\
                TaskFailed,TotalWatchedUser,TotalWatchedVideo,TotalEnabledTask,\
                WorkerStatus
from . import current_user
from ._task import set_task
main = Blueprint('api_task', __name__)


@main.route('/add')
def add_task():
    u = current_user()
    if not u:
        return jsonify(status='error', message='找不到当前用户')
    if not u.admin:
        return jsonify(status='error', message='当前用户没有管理权限')

    type_ = request.values.get('type', None)
    param = request.values.get('param', None)
    period = request.values.get('period', None)
    phase = request.values.get('phase', None)

    if type_ and param and period and phase:
        if set_task(type_, param, period, phase):
            ret = 'OK'
        else:
            ret = '任务已存在，按所指定的参数进行了更新'

        TotalEnabledTask.refresh()
    else:
        ret = '参数不足'

    return jsonify(status='success' if ret == 'OK' else 'error', message=ret)


@main.route('/getlist')
def get_task_list():
    u = current_user()
    if not u:
        return jsonify(status='error', message='需要登录')

    ts = Task.findAll()
    for t in ts:
        t['type'] = t['type_']
        t['enable'] = bool(t['enable'])
        t['id'] = str(t['id']) # 如果不转换为字符串，js会因为数字位数太多转换时产生精度丢失
        del t['type_']
        # del t['id'] 不能去掉

    d = dict()
    d['status'] = 'success'
    d['data'] = ts

    return jsonify(d)


@main.route('/update')
def update_task_list():
    u = current_user()
    if not u:
        return jsonify(status='error', message='需要登录且有管理权限')
    if not u.admin:
        return jsonify(status='error', message='需要登录且有管理权限')

    id = request.values.get('id', None)
    period = request.values.get('period', None)
    phase = request.values.get('phase', None)
    enable = request.values.get('enable', True)

    t = Task.find(id)
    if not t:
        return jsonify(status='error', message='找不到对应任务')

    if period and phase:
        t.period = period
        t.phase = phase
        t.enable = enable
        t.update()

        TotalEnabledTask.refresh()
        return jsonify(status='success')
    else:
        return jsonify(status='error', message='参数不足')


@main.route('/getfaillog')
def get_fail_log():
    u = current_user()
    if not u:
        return jsonify(status='error', message='需要登录')

    logs = TaskFailed.findAll(limit=200,orderBy='ID DESC')
    for l in logs:
        del l['id']
    return jsonify(data=logs)