'''
@Date: 2019-08-13 16:32:23
@LastEditors: Gravitykey
@LastEditTime: 2019-08-27 11:32:42
'''
from . import scraper_model as model
from .. import config

import time
import hashlib
import requests
import logging

_GET_TASK_URL = config.HOST + config.URLS['GET_TASK']
_SUBMIT_TASK_URL = config.HOST + config.URLS['SUBMIT_TASK']
_SUBMIT_FAILURE_URL = config.HOST + config.URLS['SUBMIT_FAILURE']
_SCRAPER_NAME = config.SCRAPER_NAME

_TIME_DIVIDER = config._TOKEN_TIME_DIVIDER


from ..import token


class Task:
    _TASK_TYPE_MAP = {
        'Online': model.OnlineData,
        'RegionActivity': model.RegionActivity,
        'VideoInfo': model.VideoInfo,
        'VideoStat': model.VideoStat,
        'UpInfo': model.UpInfo,
        'UpStat': model.UpStat,
        # 'UpRelation': model.UpRelation,
    }

    def __init__(self, id_, type_, param):
        self.failure = True
        self.id = id_  # 任务编号
        self.type_ = type_  # 类型
        
        if param == '0':
            param = None
        self.param = param  # 参数

        if param:
            self.m = self._TASK_TYPE_MAP[type_](param)
        else:
            self.m = self._TASK_TYPE_MAP[type_]()

    def get(self):
        try:
            self.m.fromRemote()
            if self.m.getData():
                self.failure = False
        except:
            self.failure = True
            # raise

    def submit(self):
        payload = {
            'task_id': self.id,
            'scraper_name': _SCRAPER_NAME,
            'token': token.make_token(_SCRAPER_NAME, self.id),
            'type': self.type_,
        }
        if self.failure:
            logging.error('Submit Failure: ' + str(payload))
            requests.get(_SUBMIT_FAILURE_URL, params=payload)
        else:
            payload.update(self.m.getData())
            requests.get(_SUBMIT_TASK_URL, params=payload)


def get_task():
    d = dict()
    d['token'] = token.make_token(_SCRAPER_NAME)
    d['scraper_name'] = _SCRAPER_NAME
    r = requests.get(_GET_TASK_URL, params=d)
    ret = r.json()
    a = list()
    if ret and ret['status'] == 'success':
        print(ret)
        for x in ret['tasklist']:
            t = Task(x['id'], x['type'], x['param'])
            a.append(t)
    return a