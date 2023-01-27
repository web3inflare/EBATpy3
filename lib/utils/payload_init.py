"""
@Time ： 2023/1/17 16:20
@Auth ： Web3inFlare
@File ：payload_init.py
@IDE ：PyCharm
@Motto: 咕咕嘎嘎
"""

import importlib
import os.path
import platform
import sys

from lib.utils import output


def get_dir_files(base_path):
    file_list = []
    if os.path.isdir(base_path):
        for each_file_or_dir in os.listdir(base_path):
            current_path = os.path.join(base_path, each_file_or_dir)
            if os.path.isfile(current_path) and each_file_or_dir.split('.')[-1] != 'py':
                continue
            each_path = get_dir_files(current_path)
            for file in each_path:
                file_list.append(file)

    else:
        file_list.append(base_path)
    return file_list


def path_to_module_path(path):
    if 'Windows' in platform.system():
        path = path.lstrip('\\')
        module_path = path.replace('\\', '.')
    else:
        path = path.lstrip('/')
        module_path = path.replace('/', '.')
    module_path = module_path.replace('.py', '')
    return module_path


# 获取全部payload
def get_payload_module_list():
    payload_module_list = []
    current_path = os.path.abspath('.')
    payloads_base_path = os.path.join(current_path, 'payload')
    payload_path_list = get_dir_files(payloads_base_path)
    for payload_path in payload_path_list:
        payload_path = payload_path.replace(current_path, '')
        payload_module_path = path_to_module_path(payload_path)
        try:
            payload_module_list.append(importlib.import_module(payload_module_path))
        except:
            pass
    return payload_module_list


def get_filename_by_path(path):
    if 'Windows' in platform.system():
        filename = path.split('\\')[-1]
    else:
        filename = path.split('/')[-1]
    return filename


# 指定payload
def get_payload_module_list_by_search(search_keys_list):
    search_flag = True
    payload_module_list = []
    current_path = os.path.abspath('.')
    payloads_base_path = os.path.join(current_path, 'payload')
    payload_path_list = get_dir_files(payloads_base_path)
    for search_keys in search_keys_list:
        for payload_path in payload_path_list:
            payload_paths = payload_path.replace(current_path, '')
            payload_filename = get_filename_by_path(payload_paths)
            if search_keys == payload_filename.split('.')[0] and search_flag:
                try:
                    output.status_print("[*] Load Payload File : {0}".format(payload_filename), 0)
                    payload_module_path = path_to_module_path(payload_paths)
                    payload_module_list.append(importlib.import_module(payload_module_path))
                    search_flag = False
                    break
                except Exception as e:
                    search_flag = True
                    print(e)
                    break
        if search_flag:
            output.status_print('[-] The Payload {0} File Does Not Exist'.format(search_keys), 3)
            sys.exit()
        search_flag = True
    return payload_module_list


# 指定payload类型

def get_payload_module_list_by_type(module_type):
    payload_module_list = []
    payload_module_lists = []
    current_path = os.path.abspath('.')
    payloads_base_path = os.path.join(current_path, 'payload')
    payload_path_list = get_dir_files(payloads_base_path)
    for payload_path in payload_path_list:
        payload_path = payload_path.replace(current_path, '')
        payload_module_path = path_to_module_path(payload_path)
        try:
            payload_module_lists.append(importlib.import_module(payload_module_path))
        except Exception as e:
            print(e)
            pass
    # 在循环一遍拿到指定的类型
    for payload_module in payload_module_lists:
        result = payload_module.payload_info()
        if module_type in result['Type']:
            output.status_print("[*] Load Payload Name:[{0}]".format(result['Name']), 0)
            payload_module_list.append(payload_module)
    if not len(payload_module_list) > 0:
        output.status_print(f'[-] No Payload Does Not Perform An Operation', 3)
        sys.exit()
    return payload_module_list
