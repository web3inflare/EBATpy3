"""
@Time ： 2023/1/19 00:18
@Auth ： Web3inFlare
@File ：engine.py
@IDE ：PyCharm
@Motto: 咕咕嘎嘎
"""


from lib.core import thread
from lib.utils import output


def run(target_list, payload_module_list, max_thread):
    """

    :param target_list: 目标列表
    :param payload_module_list: payload列表
    :param max_thread: 线程池数量
    :return:
    """
    try:
        thread_pool = thread.ThreadPool(max_thread)
        for current_target in target_list:
            # 处理传入的列表,每一个payload 需要的参数不同
            current_targets = current_target.split("----")
            # 提交到线程池中
            [thread_pool.add_task(payload.run, current_targets) for payload in payload_module_list]
        # 线程执行后的回调信息
        futures = thread_pool.start_threadpool()
        # 打印所有的线程的任务结果
        output.output(futures)
    except Exception as e:
        print(e)
