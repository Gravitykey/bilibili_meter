'''
@Date: 2019-08-23 18:05:16
@LastEditors: Gravitykey
@LastEditTime: 2019-08-28 18:11:04
'''
import time, uuid
from .orm import Model, StringField, BooleanField, IntegerField, FloatField, TextField, execute
from .utils import Snow
from .utils import date_to_str, now_date_to_str, get_zero_timestamp
snow = Snow()

import hashlib
from ..config import PW


def int_timestamp():
    return int(time.time())


def next_guid():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)


class WebUser(Model):
    __table__ = 'web_users'

    id = StringField(primary_key=True, default=next_guid, ddl='varchar(50)')
    name = StringField(ddl='varchar(50)')
    passwd = StringField(ddl='varchar(50)')
    admin = BooleanField(default=False)
    created_at = IntegerField(default=int_timestamp)

    @staticmethod
    def calc_pw(rawpw):
        return hashlib.md5((PW + rawpw).encode(encoding='utf-8')).hexdigest()

    @classmethod
    def auth(cls, name, pw):
        us = cls.findAll(
            where='`name`=? AND `passwd`=?', args=(name, cls.calc_pw(pw)))
        if not us:
            return None
        else:
            return us[0]

    @classmethod
    def new(cls, name, pw):
        us = cls.findAll(where='`name`=?', args=(name, ))
        # print(us)
        if len(us) == 0:
            u = cls(name=name, passwd=cls.calc_pw(pw))
            u.insert()


class WatchedUser(Model):
    __table__ = 'watched_users'
    id = IntegerField(primary_key=True)
    name = StringField(ddl='varchar(30)')
    sex = StringField(ddl='varchar(10)')
    face = StringField(ddl='varchar(150)')
    sign = StringField(ddl='varchar(100)')
    hide = BooleanField(default=False)


class WatchedVideo(Model):
    __table__ = 'watched_videos'
    id = IntegerField(primary_key=True)
    owner_mid = IntegerField()
    tid = IntegerField()
    tname = StringField(ddl='varchar(20)')
    pic = StringField(ddl='varchar(150)')
    title = StringField(ddl='varchar(100)')
    desc = StringField(ddl='varchar(300)')
    pubdate = IntegerField()
    hide = BooleanField(default=False)


class Task(Model):
    __table__ = 'tasks'
    id = IntegerField(primary_key=True, default=snow.getInt)
    period = IntegerField(default=1800)
    phase = IntegerField(default=0)
    type_ = StringField(ddl='varchar(30)')
    param = StringField(ddl='varchar(50)')
    enable = BooleanField(default=True)
    creat_time = IntegerField(default=int_timestamp)

    @classmethod
    def count_enable(cls):
        return cls.findNumber('COUNT(1)', where='`enable`=1')


# class LastSubmit(Model):
#     __table__ = 'task_last_submit'
#     id = IntegerField(primary_key=True)
#     last_sub_time = IntegerField()


class TaskStatus(Model):
    __table__ = 'task_status'
    id = IntegerField(primary_key=True)
    last_sub_time = IntegerField(default=0)
    assigned_time = IntegerField(default=0, nullable=True)
    assigned_to = StringField(ddl='varchar(20)', nullable=True)


class TaskFailed(Model):
    __table__ = 'task_failed'
    id = IntegerField(primary_key=True, default=snow.getInt)
    task_id = IntegerField()
    fail_time = IntegerField()
    fail_type = StringField(ddl='varchar(10)')  #'timeup' or 'report'
    worker = StringField(ddl='varchar(20)')

    @classmethod
    def count_today(cls):
        t = get_zero_timestamp()
        return cls.findNumber('COUNT(1)', where='`fail_time` > ?', args=(t, ))


# 三个表统计数量，做缓存


class TotalWatchedUser(Model):
    __link__ = WatchedUser
    __table__ = 'total_user'
    __pre_sql__ = 'INSERT INTO `' + __table__ + '` (`id`,`total`)VALUES (1,0)'
    id = IntegerField(primary_key=True, default=1)
    total = IntegerField()

    @classmethod
    def get_total(cls):
        return cls.findNumber('total')

    @classmethod
    def refresh(cls):
        sql = 'UPDATE `' + cls.__table__ + '` SET `total` = (SELECT COUNT(1) FROM `' + cls.__link__.__table__ + '`) WHERE `id` = 1'
        return execute(sql, [])

    @classmethod
    def add_one(cls):
        sql = 'UPDATE `' + cls.__table__ + '` SET `total` = `total` + 1 WHERE `id` = 1'
        return execute(sql, [])


class TotalWatchedVideo(Model):
    __link__ = WatchedVideo
    __table__ = 'total_video'
    __pre_sql__ = 'INSERT INTO `' + __table__ + '` (`id`,`total`)VALUES (1,0)'
    id = IntegerField(primary_key=True, default=1)
    total = IntegerField()

    @classmethod
    def get_total(cls):
        return cls.findNumber('total')

    @classmethod
    def refresh(cls):
        sql = 'UPDATE `' + cls.__table__ + '` SET `total` = (SELECT COUNT(1) FROM `' + cls.__link__.__table__ + '`) WHERE `id` = 1'
        return execute(sql, [])

    @classmethod
    def add_one(cls):
        sql = 'UPDATE `' + cls.__table__ + '` SET `total` = `total` + 1 WHERE `id` = 1'
        return execute(sql, [])


class TotalEnabledTask(Model):
    __link__ = Task
    __table__ = 'total_task'
    __pre_sql__ = 'INSERT INTO `' + __table__ + '` (`id`,`total`)VALUES (1,0)'
    id = IntegerField(primary_key=True, default=1)
    total = IntegerField()

    @classmethod
    def get_total(cls):
        return cls.findNumber('total')

    @classmethod
    def refresh(cls):
        sql = 'UPDATE `' + cls.__table__ + '` SET `total` = (SELECT COUNT(1) FROM `' + cls.__link__.__table__ + '` WHERE `enable`) WHERE `id` = 1'
        return execute(sql, [])


class WorkerStatus(Model):
    __table__ = 'worker_status'
    __index__ = ['date']
    id = IntegerField(primary_key=True, default=snow.getInt)
    worker_name = StringField(ddl='varchar(20)')
    date = StringField(ddl='varchar(20)')
    last_query_time = IntegerField(default=0)
    last_sub_time = IntegerField(default=0)
    day_submit_count = IntegerField(default=0)

    @classmethod
    def add_one(cls, time, worker_name, act='query'):
        if act == 'submit':
            s = '`last_sub_time`= ?,`day_submit_count`=`day_submit_count`+1'
        else:
            s = '`last_query_time`= ?'

        date_str = date_to_str(time)
        sql = 'UPDATE `worker_status` SET ' + s + ' WHERE `worker_name`=? AND `date`=?'
        rowcount = execute(sql, (time, worker_name, date_str))

        # 没有当天记录的情况下
        if rowcount == 0 and (not cls.findAll('`worker_name`=? AND `date`=?',
                                              (worker_name, date_str))):
            x = cls()
            x.worker_name = worker_name
            x.date = date_str
            x.day_submit_count = 1 if act == 'submit' else 0
            x.last_sub_time = time if act == 'submit' else 0
            x.last_query_time = time if act == 'query' else 0
            x.insert()

    @classmethod
    def get_today(cls):
        return cls.findAll(where='`date`=?', args=(now_date_to_str(), ))


class ItemBase(Model):
    __table__ = None
    id = IntegerField(primary_key=True)
    @classmethod
    def findByDay(cls, need_key, need_filter, key=None, val=None, limit=500):
        '''
        获取实例：
        need_key = 'id', 
        need_filter='MAX(`id`)',
        可获取当天内ID最大的数据
        need_key='id',
        need_filter='MAX(`id`)',
        key='d_aid' val='1234',
        可获取当天 d_aid为1234的id最大的数据
        '''
        table_name = cls.__table__
        if key is None:
            key = 1
            val = 1
        else:
            key='`'+key+'`'
        d = {
            'need_key': need_key,
            'need_filter': need_filter,
            'key': key,
            'val': val,
            'table_name': table_name,
        }
        sub_where_sql = '''`{need_key}` 
        IN ( SELECT {need_filter} FROM `{table_name}`
            WHERE {key}={val} 
                GROUP BY FROM_UNIXTIME( `time`, '%%Y-%%m-%%d' ))'''.format(**d)
        # print(d)

        return cls.findAll(
            where=sub_where_sql, orderBy='id DESC', limit=limit)


class ItemOnline(ItemBase):
    __table__ = 'items_online'
    id = IntegerField(primary_key=True, default=snow.getInt)
    task_id = IntegerField()
    time = IntegerField(default=int_timestamp)
    # param = StringField(ddl='varchar(50)')
    # 数据部分
    d_web_online = IntegerField()
    d_play_online = IntegerField()
    d_all_count = IntegerField()
    d_region_count = StringField(ddl='varchar(500)')


class ItemVideoStat(ItemBase):
    __table__ = 'items_video_stat'
    __index__ = ['d_aid']
    id = IntegerField(primary_key=True, default=snow.getInt)
    task_id = IntegerField()
    time = IntegerField(default=int_timestamp)
    # param = StringField(ddl='varchar(50)')
    # 数据部分
    d_aid = IntegerField()
    d_view = IntegerField()
    d_danmaku = IntegerField()
    d_reply = IntegerField()
    d_favorite = IntegerField()
    d_coin = IntegerField()
    d_share = IntegerField()
    d_like = IntegerField()


class ItemUpStat(ItemBase):
    __table__ = 'items_up_stat'
    __index__ = ['d_mid']
    id = IntegerField(primary_key=True, default=snow.getInt)
    task_id = IntegerField()
    time = IntegerField(default=int_timestamp)
    # param = StringField(ddl='varchar(50)')
    # 数据部分
    d_mid = IntegerField()
    d_total_video_view = IntegerField()
    d_total_article_view = IntegerField()
    # 关注人数和粉丝数
    d_following = IntegerField()
    d_follower = IntegerField()


class ItemRegionActivity(ItemBase):
    __table__ = 'items_region_activity'
    id = IntegerField(primary_key=True, default=snow.getInt)
    task_id = IntegerField()
    time = IntegerField(default=int_timestamp)
    #
    d_json = StringField(ddl='varchar(500)')


TYPE_MAP = {
    'Online': ItemOnline,
    'RegionActivity': ItemRegionActivity,
    'VideoInfo': WatchedVideo,
    'VideoStat': ItemVideoStat,
    'UpInfo': WatchedUser,
    'UpStat': ItemUpStat,
    '_IGNORE_PARAM': ['Online', 'RegionActivity'],
    '_NEED_ID': ['VideoInfo', 'UpInfo']
}


# 把Model导出到SQL语句用于新建数据库
def _make_sql(db_name='bilibili_meter'):
    g = globals()
    print('''/*请检查索引项是否正确，以及再次确认可以为空的字段*/
drop database if exists {db_name};
create database {db_name};
use {db_name};'''.format(db_name=db_name))
    # print(g)
    for k in g:
        v = g[k]
        # if k == 'ItemBase':
        # continue
        if isinstance(v, type):
            if not (getattr(v, '__table__', None)):
                continue
            print('\ncreate table ' + v.__table__ + '(')
            pk = v.__mappings__[v.__primary_key__]
            print('`%s` %s %s,' %
                  (getattr(pk, 'name', None) or v.__primary_key__,
                   pk.column_type, 'not null'))
            # d = v.__dict__
            for fs in v.__fields__:
                # print(v)
                f = v.__mappings__[fs]
                print('`%s` %s %s,' % (getattr(f, 'name', None) or fs,
                                       f.column_type,
                                       '' if f.nullable else 'not null'))
            # 额外索引
            if hasattr(v, '__index__'):
                for idx in v.__index__:
                    print('key `idx_%s` (`%s`),' % (idx, idx))

            print('primary key (`%s`)' % (v.__primary_key__))
            print(') engine=innodb default charset=utf8mb4;')

            if hasattr(v, '__pre_sql__'):
                print(v.__pre_sql__ + ';')
