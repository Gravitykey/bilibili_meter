# ========== FOR SCRAPER =============

HOST = 'https://127.0.0.1'
URLS = {
    'GET_TASK':'/s/gettasks',
    'SUBMIT_TASK':'/s/submittask',
    'SUBMIT_FAILURE':'/s/submitfailure',
}
SCRAPER_NAME = 'HOME_LAPTOP' # 此爬虫节点名称

QUERY_INTERVAL = 20 # 爬虫轮询任务的时间


# ============ FOR AUTH ===============
TOKEN = 'your_token'
_TOKEN_TIME_DIVIDER = 31


# ============ FOR SERVER =============

# DB///
DB_HOST = '127.0.0.1'
DB_USER = 'root'
# DB_PASSWORD = 'root'
DB_PASSWORD = None
DB_NAME = 'bilibili_meter'
DB_PORT = 3306
DB_CHARSET = 'utf8'

# TASK///
ASSIGNMENT_TIMELIMIT = 30 # 分发后多少秒钟没提交则报错
ASSIGNMENT_COUNT = 10   # 单次查询后分发任务数量

# PW FOR AUTH
PW = 's-a-l-t!#.type_something$#' 

#FLASK_CONFIGS
from datetime import timedelta
FLASK_CONFIG={
    'SECRET_KEY': 'NXU*(*^231)414cf81',
    'PERMANENT_SESSION_LIFETIME' : timedelta(days=1),
    'JSON_AS_ASCII' : False,
    # 'JSONIFY_PRETTYPRINT_REGULAR':False,
}