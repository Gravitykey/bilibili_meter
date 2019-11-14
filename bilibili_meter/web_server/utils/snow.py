'''
@Date: 2019-08-24 16:45:36
@LastEditors: Gravitykey
@LastEditTime: 2019-08-26 15:22:14
'''
# 实现一个8字节int之内的雪花算法

import time
import os
import threading
lock = threading.Lock()

class Snow(object):
    def __init__(self, machine_idx=None):
        init_date = time.strptime('2010-01-01 00:00:00', "%Y-%m-%d %H:%M:%S")
        self.start = int(time.mktime(init_date))
        self.last = int(time.time())
        self.pid = self.fill_zero(str(os.getpid() % 1000),3)
        if machine_idx is None:
            machine_idx = 1
        self.machine_idx = self.fill_zero(str(machine_idx),2)
        self.count_id = 0

    @staticmethod
    def fill_zero(str, target_length):
        length = len(str)
        if length < target_length:
            z = '0' * (target_length - length)
            return z + str
        else:
            return str

    def get(self):
        # 非常简陋的处理方法，如果1秒钟之内大于99999，睡一秒
        if self.count_id == 9999:
            time.sleep(1)

        # 防止生成重复序号，加锁
        lock.acquire()
        now = int(time.time())
        if now == self.last:
            self.count_id += 1
        else:
            self.count_id = 0
        self.last = now
        lock.release()
        temp = str(now - self.start)
        temp = self.fill_zero(temp,9)

        count_id_str = self.fill_zero(str(self.count_id),4)
        return ''.join([temp, self.machine_idx,self.pid, count_id_str])

    def getInt(self):
        return int(self.get())

if __name__ == '__main__':
    import threading
    snow = Snow()

    def echo():
        print(snow.get(),os.getpid())
        time.sleep(1)
        print(snow.get(),os.getpid())
        time.sleep(0.01)
        print(snow.get(),os.getpid())
    echo()

    threads = [threading.Thread(target=echo) for i in range(1000)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # 9-delta seconds  2-machine_idx 3-pid 4-count