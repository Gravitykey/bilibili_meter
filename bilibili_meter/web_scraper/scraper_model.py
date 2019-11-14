'''
@Description: DataModel
@Author: Gravitykey
@Date: 2019-08-07 14:00:46
@LastEditTime: 2019-08-27 11:32:58
@LastEditors: Gravitykey
'''
from . import fetch
import time
import json

from ..region import _REGION_NAME, _SUB_REGION_NAME, get_region_name


def make_task_id(aid_or_mid):
    '''
    @description: make a task No.
    @param {av_no or member_id} 
    @return: str:taskNo.
    '''
    t = int(time.time() // 1800)

    return int(str(t) + str(aid_or_mid))  # 频率每半小时一次


class DataClass:
    def __init__(self):
        self.data = None

    def __repr__(self):
        return '<{name} : {d} >\n'.format(
            name=self.__class__.__name__, d=str(self.data))

    def getData(self):
        return self.data


class OnlineData(DataClass):
    def fromRemote(self):
        self.raw = fetch.BilibiliOnlineData()
        d = self.raw.get()
        if d:
            self.data = dict()
            self.data['region_count'] = json.dumps(
                d['data']['region_count'])  # 各分区投稿数统计
            self.data['all_count'] = d['data']['all_count']  # 总投稿数
            self.data['web_online'] = d['data']['web_online']  # 在线人数
            self.data['play_online'] = d['data']['play_online']  # 当前播放器数量
            # 时间使用时间戳
            self.data['time'] = int(time.time())


class VideoInfo(DataClass):
    def __init__(self, av):
        super().__init__()
        self.av = av

    def fromRemote(self):
        self.raw = fetch.BilibiliVideoInfo(self.av)
        d = self.raw.get()
        if d:
            self.data = dict()
            self.data['aid'] = d['videoData']['aid']  # av号
            self.data['tid'] = d['videoData']['tid']  # 分类ID
            self.data['tname'] = d['videoData']['tname']  # 分类名称
            self.data['pic'] = d['videoData']['pic']  # 封面
            self.data['title'] = d['videoData']['title']  # 标题
            self.data['pubdate'] = d['videoData']['pubdate']  # 发布时间戳
            self.data['desc'] = d['videoData']['desc']  # 描述
            self.data['owner_name'] = d['videoData']['owner']['name']  # UP的名字
            self.data['owner_mid'] = d['videoData']['owner']['mid']  # UP的MID
            self.data['owner_face'] = d['videoData']['owner']['face']  # UP的头像
            # 时间使用时间戳
            self.data['time'] = int(time.time())


class VideoStat(DataClass):
    def __init__(self, av):
        super().__init__()
        self.av = av

    def fromRemote(self):
        self.raw = fetch.BilibiliVideoStat(self.av)
        d = self.raw.get()
        if d:
            self.data = dict()
            self.data['aid'] = d['data']['aid']  # av号
            self.data['view'] = d['data']['view']  # 播放量
            self.data['danmaku'] = d['data']['danmaku']  # 弹幕数
            self.data['reply'] = d['data']['reply']  # 评论
            self.data['favorite'] = d['data']['favorite']  # 收藏
            self.data['coin'] = d['data']['coin']  # 硬币
            self.data['share'] = d['data']['share']  # 分享
            self.data['like'] = d['data']['like']  # 点赞
            # 时间使用时间戳
            self.data['time'] = int(time.time())


class UpInfo(DataClass):
    def __init__(self, mid):
        super().__init__()
        self.mid = mid

    def fromRemote(self):
        self.raw = fetch.BilibiliUpInfo(self.mid)
        d = self.raw.get()
        if d:
            self.data = dict()
            self.data['mid'] = d['data']['mid']  # 用户id
            self.data['name'] = d['data']['name']  # 用户名
            self.data['sex'] = d['data']['sex']  # 性别
            self.data['face'] = d['data']['face']  # 头像
            self.data['sign'] = d['data']['sign']  # 签名
            # 时间使用时间戳
            self.data['time'] = int(time.time())


class UpStat(DataClass):
    def __init__(self, mid):
        super().__init__()
        self.mid = mid

    def fromRemote(self):
        self.raw = fetch.BilibiliUpStat(self.mid)
        self.raw2 = fetch.BilibiliUpRelation(self.mid)
        d = self.raw.get()
        d2 = self.raw2.get()
        if d and d2:
            self.data = dict()
            self.data['mid'] = self.mid  # 用户id
            # 视频总播放
            self.data['total_video_view'] = d['data']['archive']['view']
            # 文章总观看
            self.data['total_article_view'] = d['data']['article']['view']
            # 合并原来的Relation类
            self.data['following'] = d2['data']['following']  # 关注数
            self.data['follower'] = d2['data']['follower']  # 粉丝数
            # 时间使用时间戳
            self.data['time'] = int(time.time())


# 下面的Relation合并到Stat类里面

# class UpRelation(DataClass):
#     def __init__(self, mid):
#         super().__init__()
#         self.mid = mid

#     def fromRemote(self):
#         self.raw = fetch.BilibiliUpRelation(self.mid)
#         d = self.raw.get()
#         if d:
#             self.data = dict()
#             self.data['mid'] = d['data']['mid']  # 用户id
#             self.data['following'] = d['data']['following']  # 关注数
#             self.data['follower'] = d['data']['follower']  # 粉丝数
#             # 时间使用时间戳
#             self.data['time'] = int(time.time())


class RegionActivity(DataClass):
    def fromRemote(self):
        self.raw = fetch.BilibiliSub()
        d = self.raw.get()
        if d:
            self.data = dict()
            for key in _REGION_NAME:
                self.data[key] = d.get(key,0)

            x = json.dumps(self.data)
            self.data['json'] = x
            # 时间使用时间戳
            self.data['time'] = int(time.time())


if __name__ == '__main__':
    mid = 621607
    av = 1559315
    a = OnlineData()
    a.fromRemote()

    b = RegionActivity()
    b.fromRemote()

    c = UpInfo(mid)
    c.fromRemote()

    # d = UpRelation(mid)
    # d.fromRemote()

    e = UpStat(mid)
    e.fromRemote()

    f = VideoInfo(av)
    f.fromRemote()

    g = VideoStat(av)
    g.fromRemote()

    print(a)
    print(b)
    print(c)
    # print(d)
    print(e)
    print(f)
    print(g)