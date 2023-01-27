"""
@Time ： 2023/1/17 14:56
@Auth ： Web3inFlare
@File ：console.py
@IDE ：PyCharm
@Motto: 咕咕嘎嘎
"""
import sys

from lib.core import engine
from lib.utils import output
from lib.utils import payload_init
from csv import DictReader


def EBATpy3_console(args):
    target_list = []
    # 显示所有 payload
    if args.show:
        payload_module_list = payload_init.get_payload_module_list()
        output.show(payload_module_list)
        sys.exit()
    if args.file:
        # 读取文件
        with open(args.file, mode='r') as read_obj:
            dict_reader = DictReader(read_obj)
            for i in list(dict_reader):
                # 判断是否有表头
                if 'wallet_address' not in i:
                    output.status_print('[-] The CSV file format is incorrect', 2)
                    sys.exit()
                target_list.append(i)
    # 线程
    if args.thread:
        max_thread = args.thread
    # 指定payload类型或 payload
    if 'all' == args.payload:
        payload_module_list = payload_init.get_payload_module_list()
    elif 'query' == args.payload:
        payload_module_list = payload_init.get_payload_module_list_by_type(args.payload)
    elif 'swap' == args.payload:
        payload_module_list = payload_init.get_payload_module_list_by_type(args.payload)
    elif 'faucet' == args.payload:
        payload_module_list = payload_init.get_payload_module_list_by_type(args.payload)
    elif 'playwright' == args.payload:
        payload_module_list = payload_init.get_payload_module_list_by_type(args.payload)
    elif 'mint' == args.payload:
        payload_module_list = payload_init.get_payload_module_list_by_type(args.payload)
    elif 'transfer' == args.payload:
        payload_module_list = payload_init.get_payload_module_list_by_type(args.payload)
    elif args.payload:
        payload_module_list = payload_init.get_payload_module_list_by_search(args.payload.split(','))
    else:
        output.usage()
        sys.exit()
    output.status_print('[*] Starting {0}'.format(output.get_time1()), 0)
    output.status_print('[*] Tasks:{0} Payload: {1}'.format(len(target_list), len(payload_module_list)), 0)
    try:
        engine.run(target_list, payload_module_list, max_thread)
    except Exception as e:
        output.status_print(f'[-] The Program Terminated Abnormally{e}', 3)
        sys.exit(0)
    output.status_print('[*] Ending {0}'.format(output.get_time1()), 1)
