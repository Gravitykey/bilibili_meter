import time
import logging
from ..model import WebUser, WatchedUser, WatchedVideo, Task, TaskStatus,\
                ItemOnline, ItemVideoStat, ItemUpStat, ItemRegionActivity,\
                TaskFailed,TotalEnabledTask,TotalWatchedUser,TotalWatchedVideo

from ..model import TYPE_MAP
from ..model import snow
from .. import orm
from ... import config


def _is_timeup(ct, lt, period, phase):
    '判断是否到了该执行的时间'
    # lt 上次时间 ct现在时间
    if not lt:
        return True
    else:
        ct = int(ct)
        lt = int(lt)
        next_start = lt - lt % period + phase + period
        # print('--',ct,lt,next_start)
        return ct > next_start


def _clear_overtime_assignment():
    '清理分发出去的已经过期的任务'
    t = config.ASSIGNMENT_TIMELIMIT
    ct = int(time.time())
    sqlget = 'SELECT `id`,`assigned_to` FROM `task_status` WHERE `assigned_time` < ? - ?'
    sqlclr = 'UPDATE `task_status` SET `assigned_time`=0,`assigned_to`=NULL where `assigned_time` < ? - ? '
    # ct - t的结果大于assigned_time，说明任务超时
    expired = orm.select(sqlget, (ct, t))
    for task in expired:
        if not task['assigned_to']:
            continue
        tf = TaskFailed(
            task_id=task['id'],
            worker=task['assigned_to'],
            fail_time=ct,
            fail_type='overtime')
        tf.insert()
    orm.execute(sqlclr, (ct, t))


def set_task(type_, param=None, period=None, phase=0, enable=True):
    '新建任务或者保存任务'

    if type_ in TYPE_MAP['_IGNORE_PARAM']:
        param = 0

    param = int(param)
    period =int(period)
    phase = int(phase)
    
    if phase > period:
        phase = phase % period

    if not period:
        return 'NEED_PERIOD'
    if not param and param != 0:
        return 'NEED_PARAM'

    tasks = Task.findAll(where="`type_`=? AND `param`=?", args=(type_, param))
    # print(tasks)
    t = tasks[0] if len(tasks) else Task()
    t.type_ = type_
    t.param = param
    t.phase = phase
    t.period = period
    t.enable = enable
    if getattr(t, 'id', None):
        is_new = False
        t.update()
        print('update:', t.id)
    else:
        is_new = True
        new_id = snow.getInt()
        t.id = new_id
        t.insert()
        ts = TaskStatus(id=new_id)
        ts.insert()
        print('insert both task & status:', t.id)

        if type_=='UpInfo':
            TotalWatchedUser.add_one()
        if type_=='VideoInfo':
            TotalWatchedVideo.add_one()

    return is_new


def distribute_tasks(scraper_name):
    tasks = Task.findAll(where="enable=1")
    if len(tasks) == 0:
        return []
    # 清理过期的任务分发
    _clear_overtime_assignment()
    # 解决1+N查询问题
    ids = [str(x.id) for x in tasks]
    task_status = TaskStatus.findAll(where='`id` in(%s)' % (','.join(ids)))
    d_ts = {ts.id: (ts.last_sub_time, ts.assigned_to) for ts in task_status}
    ct = int(time.time())

    # 找出冷却时间以外以及没有被指派出去的任务
    def filter_func(x):
        ts = d_ts.get(x.id, (0, None))
        is_t_up = _is_timeup(ct, ts[0], x.period, x.phase)
        is_can_assign = (ts[1] is None) or (ts[1] == scraper_name)
        return is_t_up and is_can_assign

    filtered = filter(filter_func, tasks)

    # 单次返回指定数量
    to_ret = list(filtered)[:config.ASSIGNMENT_COUNT]

    # 把准备返回的重新标记任务分配
    if len(to_ret) != 0:
        to_ret_ids = [str(x.id) for x in to_ret]
        sql_set_stat = (
            "UPDATE `task_status` "
            "SET `assigned_time`=?,`assigned_to`=? WHERE `id` in(%s)" %
            (','.join(to_ret_ids)))
        orm.execute(sql_set_stat, (
            ct,
            scraper_name,
        ))

    return [{'id': x.id, 'param': x.param, 'type': x.type_} for x in to_ret]


def receive_item(task_id, scraper_name, type_, obj):
    task = Task.find(task_id)
    if not (task and task.enable):
        logging.warn('received a disabled task item')
        return
    task_status = TaskStatus.find(task_id)

    if _is_timeup(obj['time'], task_status.last_sub_time, task.period,
                  task.phase):

        M = TYPE_MAP.get(type_, None)  # 从TYPE_MAP里找到相应的类
        if not M:
            logging.warn('received a unknown type item :%s' % (type_, ))
            return
        item = M(**obj)

        # 解决model中数据d_开头的问题
        for k in item.__fields__:
            if k.startswith('d_'):
                setattr(item, k, obj[k[2:]])

        # 解决非随机ID的问题
        if type_ in TYPE_MAP['_NEED_ID']:
            item.id = obj.get('aid', None) or obj.get('mid', None)

        item.save()

        # 清理任务状态
        task_status.last_sub_time = obj.get('time', int(time.time()))
        task_status.assigned_to = None
        task_status.assigned_time = 0
        task_status.update()


def receive_failure(task_id, scraper_name):

    task_status = TaskStatus.find(task_id)
    task_status.assigned_to = None
    task_status.assigned_time = 0
    task_status.update()

    tf = TaskFailed(
        task_id=task_id,
        worker=scraper_name,
        fail_time=int(time.time()),
        fail_type='reported')
    tf.insert()

    logging.warn("%s reported a task_failure of task_id: %s" % (scraper_name,
                                                                task_id))


def disable_task(task_id):
    task = Task.find(task_id)
    if not task:
        logging.warn("disable_task:can't find task by id %s" % task_id)
        return
    task.enable = False
    task.update()


def set_user_visibility(mid, vis):
    item = WatchedUser.find(mid)
    if not item:
        logging.warn("hide_user:can't find user by id %s" % mid)
        return
    item.hide = not vis
    item.update()


def set_video_visibility(mid, vis):
    item = WatchedUser.find(mid)
    if not item:
        logging.warn("hide_user:can't find user by id %s" % mid)
        return
    item.hide = not vis
    item.update()
