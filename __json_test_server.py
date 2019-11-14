'''
@Date: 2019-08-16 14:51:18
@LastEditors: Gravitykey
@LastEditTime: 2019-08-18 11:43:54
'''

from flask import Flask, jsonify, request
import logging
logging.basicConfig(level=logging.DEBUG)
from bilibili_meter.web_server import routes
from bilibili_meter.web_server import app


# 解决测试时跨域问题
def after_request(resp):
    # resp.headers['Access-Control-Allow-Origin'] = '*,127.0.0.1:8080,localhost:8080'
    resp.headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1:8080'
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    return resp

app.after_request(after_request)

# @app.route('/test/addtask')
# def addtask():
#     d = {k: v for k, v in request.values.items()}
#     routes.task.set_task(d['type'], d['param'], d['period'], d['phase'])
#     return 'ok'


# @app.route('/test/gettask')
# def gettask():
#     d = request.values
#     scraper_name = d['name']
#     ret = {'code': 0, 'tasklist': routes.task.get_tasks(scraper_name)}
#     return jsonify(ret)


# @app.route('/test/submittask')
# def submittask():
#     d = {k: v for k, v in request.values.items()}
#     print(d)
#     routes.task.receive_item(d['task_id'], d['scraper_name'], d['type'], d)
#     return 'ok'


@app.route('/')
def page():
    return app.send_static_file('index.html')
@app.route('/favicon.ico')
def page3():
    return app.send_static_file('favicon.ico')
@app.route('/dist/<filename>')
def page2(filename):
    return app.send_static_file(filename)

# #------------------


# @app.route('/submit_task')
# def submit_task():
#     d = request.values
#     print('\n++++++++submit_task+++++++++++++++++')
#     for k, v in d.items():
#         print(k, v)
#     return 'ok'


# @app.route('/submit_failure')
# def submit_failure():
#     d = request.values
#     print('\n++++++++submit_failure+++++++++++++++++')
#     for k, v in d.items():
#         print(k, v)
#     return 'bad'


# @app.route('/get_task')
# def taskroute():
#     d = {
#         'code':
#         0,
#         'tasklist': [
#             {
#                 'id': 123124839,  # 任务编号
#                 'param': None,  # 参数
#                 'type': 'Online',  # 类型
#             },
#             {
#                 'id': 123124840,  # 任务编号
#                 'param': None,  # 参数
#                 'type': 'RegionActivity',  # 类型
#             },
#             {
#                 'id': 123124841,  # 任务编号
#                 'param': 64145803,  # 参数
#                 'type': 'VideoInfo',  # 类型
#             },
#             {
#                 'id': 123124842,  # 任务编号
#                 'param': 64145803,  # 参数
#                 'type': 'VideoStat',  # 类型
#             },
#             {
#                 'id': 123124843,  # 任务编号
#                 'param': 10955926,  # 参数
#                 'type': 'UpInfo',  # 类型
#             },
#             {
#                 'id': 123124844,  # 任务编号
#                 'param': 10955926,  # 参数
#                 'type': 'UpStat',  # 类型
#             },
#         ]
#     }
#     return jsonify(d)


if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=8081,debug=True
    )
