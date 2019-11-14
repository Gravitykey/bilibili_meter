from flask import Blueprint, jsonify, request
import time
import logging
from ..model import WebUser, WatchedUser, WatchedVideo, Task, TaskStatus,\
                ItemOnline, ItemVideoStat, ItemUpStat, ItemRegionActivity,\
                TaskFailed,TotalWatchedUser,TotalWatchedVideo,TotalEnabledTask,\
                WorkerStatus
from .. import orm
from ..utils import get_zero_timestamp
main = Blueprint('api_online', __name__)


@main.route('/get')
def get_online():
    byday = request.values.get('byday', None)
    if not byday or not int(byday):
        items = ItemOnline.findAll(limit=500, orderBy='id DESC')
        items.reverse()
    else:
        max_sql = '''
            SELECT MAX(`d_web_online`) as `max_web_online`,
            MAX(`d_play_online`) as `max_play_online`,
            FROM_UNIXTIME( `time`, '%%Y-%%m-%%d' ) as `date`
            FROM `''' + ItemOnline.__table__ + '''`
            GROUP BY `date`ORDER BY `date` DESC
        '''
        maxlist = orm.select(max_sql, args=[])
        # 因为ID是整型且随时间增加，此时用max(`id`)取每天最后一个数据
        items = ItemOnline.findByDay(need_key='id', need_filter='MAX(`id`)')
        # print('------',len(maxlist),len(items))
        # 把items里面的播放数更新为最大播放数
        if len(maxlist) == len(items):
            for i in range(len(items)):
                items[i]['d_web_online'] = maxlist[i]['max_web_online']
                items[i]['d_play_online'] = maxlist[i]['max_play_online']
                items[i]['raw_time'] = items[i]['time']
                items[i]['time'] = get_zero_timestamp(items[i]['time'])
        items.reverse()

    d = dict()
    d['data'] = items
    # 统计总提交数
    for i in items:
        del i['id']
        del i['task_id']
    return jsonify(d)