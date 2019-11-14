from flask import Blueprint, jsonify,request,abort
import time
import logging
from ..model import WebUser, WatchedUser, WatchedVideo, Task, TaskStatus,\
                ItemOnline, ItemVideoStat, ItemUpStat, ItemRegionActivity,\
                TaskFailed,TotalWatchedUser,TotalWatchedVideo,TotalEnabledTask,\
                WorkerStatus

main = Blueprint('api_up', __name__)


@main.route('/getlist')
def get_up_list():
    ups = WatchedUser.findAll(where='`hide`=0')
    return jsonify(ups)

@main.route('/get')
def get_up_info():
    uid = request.values.get('uid',None)
    if not uid:
        abort(404)
    u = WatchedUser.find(uid)
    if not u:
        abort(404)

    d = dict()

    # 用户信息
    d['upinfo'] = u

    # 用户的视频
    videolist = WatchedVideo.findAll(where='`owner_mid`=?',args=(u.id,))
    for v in videolist:
        del v['hide']
    d['videos'] = videolist
    # d['videos'] = []

    # 关注数啥的
    data = ItemUpStat.findAll(where='`d_mid`=?',args=(u.id,))
    for i in data:
        del i['id']
        del i['d_mid']
        del i['d_following']
        del i['task_id']
    d['data'] = data

    return jsonify(d)