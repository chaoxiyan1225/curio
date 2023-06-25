# coding=utf-8
# version:python3.6.0

import queue
import argparse
import threading
import time
 
class MultiThreadHandler(object):
    """
    多线程通用任务处理型驱动框架
    task_queue 任务队列
    task_handler 任务处理函数
    thread_count 线程数数目
    result_queue 结果存放队列
    args,kwargs为可变参数列表，为扩展性考虑
    """
 
    def __init__(self, task_queue, task_handler, result_queue=None, thread_count=1, *args, **kwargs):
        self.task_queue = task_queue
        self.task_handler = task_handler
        self.result_queue = result_queue
        self.thread_count = thread_count
        self.args = args
        self.kwagrs = kwargs
        self.thread_pool = []
 
    def run(self, block_flag):
        for i in range(self.thread_count):
            t = _TaskHandler(self.task_queue, self.task_handler, self.result_queue, *self.args, **self.kwagrs)
            self.thread_pool.append(t)
        for th in self.thread_pool:
            th.setDaemon(True)
            th.start()
        '''
        # 阻塞等待所有线程结束
        if block_flag:
            for th in thread_pool:
                threading.Thread.join(th)
        '''
        # 阻塞等待所有线程结束
        while self._check_stop():
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                print('KeyboardInterruption')
                self.stop_all()
                break
        print('>>>all Done')
 
    def _check_stop(self):
        """检查线程池中所有线程是否全部运行完"""
        finish_num = 0
        for th in self.thread_pool:
            if not th.is_alive():
                finish_num += 1
 
        return False if finish_num == len(self.thread_pool) else True
 
    def stop_all(self):
        """掉用线程体stop方法，停止所有线程"""
        for th in self.thread_pool:
            th.stop()
 
class _TaskHandler(threading.Thread):
    """
    一个任务处理器线程，task_queue任务队列,task_handler任务处理函数,result_queue是结果队列，args,kwargs可变控制参数
    可外部中断
    """
 
    def __init__(self, task_queue, task_handler, result_queue=None, *args, **kwargs):
        threading.Thread.__init__(self)
        self.task_queue = task_queue
        self.task_handler = task_handler
        self.result_queue = result_queue
        self.args = args
        self.kwargs = kwargs
        self.is_stoped = True
 
    def run(self):
        while self.is_stoped:
            try:
                item = self.task_queue.get(False)  # block= False
                self.task_handler(item, self.result_queue, *self.args, **self.kwargs)
                self.task_queue.task_done()  # 退出queue
            except queue.Empty as e:
                print("all task has done!")
                break
            except Exception as e:
                print("error:", e)
                # time.sleep(1)
 
    def stop(self):
        self.is_stoped = False


''' 
def out(item, result_queue):  # 加载处理函数
    result_queue.put(item)
 
if __name__ == '__main__':
    # parse the command args
    start = time.time()
    parse = argparse.ArgumentParser()
    parse.add_argument("-f", "--file", default='yyqtext.txt',help="the target file")
    parse.add_argument("-th", "--thread", type=int, default=1, help="the thread number")
    parse.add_argument("-o", "--outfile", default='yyqout.txt',help="the outputfile")
    # 解析命令行
    results = parse.parse_args()
    filename = results.file
    th = results.thread
    outfile = results.outfile
    task_queue = queue.Queue()
    out_queue = queue.Queue()
    with open(filename, "r+") as f:
        for line in f:
            line = line.rstrip()
            if line:
                task_queue.put(line)
 
    MultiThreadHandler(task_queue, out, out_queue, th).run(True)
 
    with open(outfile, "w+") as f:
        while True:
            f.write(out_queue.get() + '\n')
            if out_queue.empty():
                break
    end = time.time()
    print(end - start)

'''
