// const HOST = 'http://127.0.0.1:8081/'
const HOST = '/' // 发布时使用
const API_URLS = {
    // 登录验证相关
    'login_stat': 'api/login/getstat',
    'login_auth': 'api/login/auth', // 传入 username/password
    'login_logout': 'api/login/logout',

    // 运行状态
    'running_stat': 'api/stat/get',

    // 在线数据
    'online': 'api/online/get',
    'activity': 'api/activity/get',

    // UP相关
    'up_list': 'api/up/getlist',
    'up_info': 'api/up/get', // 传入uid

    // 视频相关
    'video_list': 'api/video/getlist',
    'video_info': 'api/video/get', // 传入av

    // 任务管理
    'task_add': 'api/task/add', // 传入type, param, period, phase
    'task_list': 'api/task/getlist',
    'task_update': 'api/task/update', // 传入 id, period, phase, enable
    'task_get_fail_log': 'api/task/getfaillog'

}
const ADMIN_TASKLIST_PAGI_SIZE = 30
export { HOST, API_URLS,ADMIN_TASKLIST_PAGI_SIZE }