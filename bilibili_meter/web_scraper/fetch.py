#coding:utf-8

import websocket
import requests
import base64
import logging
import json
import time
import re

_URLS = {
    # wss协议的各分区活跃评论数据
    'wss': 'wss://broadcast.chat.bilibili.com:7823/sub',

    # 网站总在线数，投稿数
    'online': 'https://api.bilibili.com/x/web-interface/online',

    # av1234567 可以拿到标题，投稿时间等数据
    'video': 'https://www.bilibili.com/video/av',

    # aid=av号 获取视频播放数评论数等
    'video_stat': 'https://api.bilibili.com/x/web-interface/archive/stat?aid=',

    # mid是up主mid 有name sex等数据
    'up_info': 'https://api.bilibili.com/x/space/acc/info?mid=',

    # mid是up主mid 查看总视频播放量和阅读数
    'up_stat': 'https://api.bilibili.com/x/space/upstat?mid=',

    # vmid是up主mid粉丝数，关注别人的数据等
    'up_relation': 'https://api.bilibili.com/x/relation/stat?vmid=',
}


class DataFromRemote:
    # 缺header会提示412
    headers = {
        'Host':
        'api.bilibili.com',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    }

    def __init__(self):
        self.encoding = 'utf-8'
        self.url = None
        self.data = None

    def fetch(self):
        logging.debug('---fetch--- ' + self.url)
        try:
            r = requests.get(self.url, headers=self.headers)
            r.encoding = self.encoding
            data = r.text
            # print(data)
            if r.status_code == 200:
                self.data = data
            else:
                self.data = None
        except requests.exceptions.HTTPError:
            print(r.data)
            self.data = None
            raise

    def post_process(self, x):
        return json.loads(x)

    def get(self):
        if self.data == None:
            self.fetch()

        if self.data:
            return self.post_process(self.data)
        else:
            return None


# 首页投稿和在线数据
class BilibiliOnlineData(DataFromRemote):
    def __init__(self):
        super().__init__()
        self.url = _URLS['online']


# av号静态页面
class BilibiliVideoInfo(DataFromRemote):
    def __init__(self, av_no):
        super().__init__()
        self.url = _URLS['video'] + str(av_no)

        # 覆盖基类的 host:api.bilibili.com
        self.headers = {
            'Host':
            'www.bilibili.com',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def getInnerJson(self, data):
        '使用正则表达式匹配HTML里面的__INITIAL_STATE__对象'
        p = re.compile(r'window.__INITIAL_STATE__=({.+});')
        j = None
        try:
            j = p.search(data).group(1)
        except IndexError:
            pass
        else:
            j = json.loads(j)

        return j

    def post_process(self, x):
        nd = None
        d = self.getInnerJson(x)
        if d:
            nd = dict()
            nd['videoData'] = d['videoData']
            nd['upData'] = d['upData']
        return nd


# 视频状态
class BilibiliVideoStat(DataFromRemote):
    def __init__(self, av_no):
        super().__init__()
        self.url = _URLS['video_stat'] + str(av_no)


# up基本信息
class BilibiliUpInfo(DataFromRemote):
    def __init__(self, mid):
        super().__init__()
        self.url = _URLS['up_info'] + str(mid)


# up播放数订阅数等
class BilibiliUpStat(DataFromRemote):
    def __init__(self, mid):
        super().__init__()
        self.url = _URLS['up_stat'] + str(mid)


# up粉丝数关注数
class BilibiliUpRelation(DataFromRemote):
    def __init__(self, mid):
        super().__init__()
        self.url = _URLS['up_relation'] + str(mid)


# 各个板块的活跃数和评论数，wss连接
class BilibiliSub(DataFromRemote):
    raw_payloads_b64 = [
        'AAAAOgASAAEAAAAHAAAAAQAAeyJwbGF0Zm9ybSI6IndlYiIsImFjY2VwdHMiOlsxMDAzLDEwMDJdfQ==',
        'AAAAJAASAAEAAAAOAAAAAgAAeyJvcGVyYXRpb24iOjEwMDN9',
        'AAAAJAASAAEAAAAOAAAAAwAAeyJvcGVyYXRpb24iOjEwMDJ9',
        'AAAAIQASAAEAAAACAAAABAAAW29iamVjdCBPYmplY3Rd'
    ]

    payloads = map(base64.b64decode, raw_payloads_b64)

    def __init__(self):
        super().__init__()
        self.url = _URLS['wss']

    def fetch(self):
        res = None
        try:
            ws = websocket.WebSocket()
            ws.connect(
                self.url,
                header=[
                    'Host: broadcast.chat.bilibili.com:7823',
                    'Connection: Upgrade', 'Pragma: no-cache',
                    'Cache-Control: no-cache',
                    'User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
                    'Upgrade: websocket', 'Origin: https://www.bilibili.com',
                    'Accept-Encoding: gzip, deflate, br',
                    'Accept-Language: zh-CN,zh;q=0.9',
                    'Sec-WebSocket-Version: 13',
                    'Sec-WebSocket-Extensions: permessage-deflate; client_max_window_bits',
                    'Sec-WebSocket-Key: GXBrML6bGG2BfBV9sod83A=='
                ],
                timeout=15)
            print(ws)
            for p in self.payloads:
                ws.send_binary(p)

            for _ in range(4):
                print(ws.recv())

            res = ws.recv()
        except websocket.WebSocketException as e:
            print('wss:error', e)
        finally:
            if res and len(res) > 18:
                self.data = res[18:].decode('ascii')
            else:
                self.data = None
            ws.close(timeout=3)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    # 测试用mid
    mid = 621607
    av = 1559315
    a = BilibiliOnlineData()
    b = BilibiliSub()
    c = BilibiliUpInfo(mid)
    d = BilibiliUpRelation(mid)
    e = BilibiliUpStat(mid)
    f = BilibiliVideoInfo(av)
    g = BilibiliVideoStat(av)

    print('+++++++++++++++a BilibiliOnlineData()')
    print(a.get())
    print('+++++++++++++++b BilibiliSub()')
    print(b.get())
    print('+++++++++++++++c BilibiliUpInfo(mid)')
    print(c.get())
    print('+++++++++++++++d BilibiliUpRelation(mid)')
    print(d.get())
    print('+++++++++++++++e BilibiliUpStat(mid)')
    print(e.get())
    print('+++++++++++++++f BilibiliVideoInfo(av)')
    print(f.get())
    print('+++++++++++++++g BilibiliVideoStat(av)')
    print(g.get())