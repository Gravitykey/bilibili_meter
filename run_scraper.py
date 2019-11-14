import threading
import bilibili_meter.config
from multiprocessing import Process
import _scraper_do

def once():
    p = Process(target=_scraper_do.do)
    p.start()
    p.join()

    timer = threading.Timer(bilibili_meter.config.QUERY_INTERVAL,once)
    timer.start()


if __name__ == '__main__':
    print('Scraper starting running...')
    once()