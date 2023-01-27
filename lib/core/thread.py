"""
@Time ： 2023/1/19 00:05
@Auth ： Web3inFlare
@File ：thread.py
@IDE ：PyCharm
@Motto: 咕咕嘎嘎
"""
import concurrent.futures

import queue




class ThreadPool(object):
    # 初始化
    def __init__(self, max_thread):
        self.thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=max_thread)
        self.task_queue = queue.Queue()
        self.futures = {}

    # 添加任务
    def add_task(self, payload, target):
        new_task = (payload, target)
        self.task_queue.put(new_task)

    # 执行操作
    def start_threadpool(self):
        while self.task_queue.qsize() != 0:
            current_task = self.task_queue.get()
            current_payload = current_task[0]
            current_target = current_task[1]
            future = self.thread_pool.submit(current_payload, **current_target)
            self.futures[future] = current_target
        return concurrent.futures.as_completed(self.futures)
