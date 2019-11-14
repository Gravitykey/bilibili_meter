# -*- coding: utf-8 -*-
import gevent.monkey

gevent.monkey.patch_all()

import multiprocessing
import os


debug = True
loglevel = 'warning'
bind = '127.0.0.1:8081'
pidfile = '/www/log/gunicorn/gunicorn.pid'
logfile = '/www/log/gunicorn/debug.log'
errorlog = '/www/log/gunicorn/error.log'
accesslog = '/www/log/gunicorn/access.log'

# 启动的进程数
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gunicorn.workers.ggevent.GeventWorker'

x_forwarded_for_header = 'X-FORWARDED-FOR'