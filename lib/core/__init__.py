"""
@Time ： 2023/1/19 00:03
@Auth ： Web3inFlare
@File ：__init__.py.py
@IDE ：PyCharm
@Motto: 咕咕嘎嘎
"""


def verify(target_list, poc_modole_list, output_path):
    try:
        thread_pool = thread.ThreadPool(config.max_thread)
        for current_target in target_list:
            [thread_pool.add_task(poc.verify, current_target) for poc in poc_modole_list]         # 向线程池中添加所有poc和当前的url

        futures = thread_pool.start_threadpool()
        output.output(thread_pool, futures, output_path)
        return True
    except:
        return False