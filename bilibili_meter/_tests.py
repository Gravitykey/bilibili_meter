# 测试新建任务，分发任务，查询任务状态
import bilibili_meter.routes as routes
import time,random
import orm

task = routes.task
def test_set_tasks():
    task.set_task('test_type1','param1',1800,30)
    task.set_task('test_type2','param2',1800,30)
    task.set_task('test_type3','param3',1800,30)
    task.set_task('test_type4','param4',1800,30)
    task.set_task('test_type5','param5',120,30)
    task.set_task('test_type6','param6',120,30)
    task.set_task('test_type7','param7',120,30)
    task.set_task('test_type5','param5',120,31)
    task.set_task('test_type8','param8',120,30)
    task.set_task('test_type9','param9',120,30)
    task.set_task('test_type10','param10',120,30)
    task.set_task('test_type11','param11',60,0)
    task.set_task('test_type12','param12',60,0)
    task.set_task('test_type13','param13',60,0)
    task.set_task('test_type14','param14',60,0)
    task.set_task('test_type15','param15',60,0)
    task.set_task('test_type16','param16',60,0)
    task.set_task('test_type17','param17',60,0)

def test_get_tasks():
    for _ in range(5):
        worker = random.choice(['worker1','worker2','worker3'])
        print(worker,'get-----')
        ct = time.time()
        for i in task.get_tasks(worker):
            print(i)
        print(time.time()-ct)
        print('')
        time.sleep(5)

def multi_thread_test():
    import threading,time
    threads = [threading.Thread(target=test_get_tasks) for i in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


def get_pid():
    import os
    print(os.getpid())
def pid_test():
    import multiprocessing
    processes = [multiprocessing.Process(target=get_pid) for i in range(5)]
    for t in processes:
        t.start()
    for t in processes:
        t.join()