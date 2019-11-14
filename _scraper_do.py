#不拆成单独文件，在windows环境下使用多线程容易出问题
from bilibili_meter.web_scraper import task
def do():
    try:
        a = task.get_task()
        for t in a:
            try:
                t.get()
                t.submit()
            except:
                pass
    except:
        pass