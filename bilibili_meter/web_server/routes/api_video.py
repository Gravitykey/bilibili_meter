from flask import Blueprint, jsonify,request,abort
import time
import logging
from ..model import WebUser, WatchedUser, WatchedVideo, Task, TaskStatus,\
                ItemOnline, ItemVideoStat, ItemUpStat, ItemRegionActivity,\
                TaskFailed,TotalWatchedUser,TotalWatchedVideo,TotalEnabledTask,\
                WorkerStatus

main = Blueprint('api_video', __name__)


@main.route('/getlist')
def get_video_list():
    videos = WatchedVideo.findAll(where='`hide`=0')
    return jsonify(videos)

@main.route('/get')
def get_video_info():
    av = request.values.get('av',None)
    if not av:
        abort(404)
    v = WatchedVideo.find(av)
    if not v:
        abort(404)

    d = dict()

    # 用户信息
    d['videoinfo'] = v

    # 关注数啥的
    data = ItemVideoStat.findAll(where='`d_aid`=?',args=(v.id,))
    for i in data:
        del i['id']
        del i['d_aid']
        del i['task_id']
    d['data'] = data

    return jsonify(d)