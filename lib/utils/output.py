"""
@Time ： 2023/1/17 03:58
@Auth ： Web3inFlare
@File ：output.py
@IDE ：PyCharm
@Motto: 咕咕嘎嘎
"""

import ctypes
import platform
import sys
import time



def banner():
    banner_logo = r"""   ___    _          __                   ______            __   
  / _ |  (_)____ ___/ /____ ___   ___    /_  __/___  ___   / /___
 / __ | / // __// _  // __// _ \ / _ \    / /  / _ \/ _ \ / /(_-<
/_/ |_|/_//_/   \_,_//_/   \___// .__/   /_/   \___/\___//_//___/
                               /_/                               
                               
                               Author  Web3inflare"""
    print(banner_logo)


def usage():
    print('''
usage:
    Show All Payloads:   python3 EBATpy3.py --show
    Execute The Query:   python3 EBATpy3.py -p query
    Execute The Swap:   python3 EBATpy3.py -p swap
    Execute The Faucet:   python3 EBATpy3.py -p faucet
    Execute The Playwright:   EBATpy3 ATSRRF.py -p playwright
    Execute The Mint:   python3 EBATpy3.py -p mint
    Execute The Transfer:   python3 EBATpy3.py -p transfer
    Set The Thread Pool: python3 EBATpy3.py -p query -t 100
    Use The Specified Payload: EBATpy3 ATSRRF.py -p test 
    Use Multiple Payloads: python3 EBATpy3.py -p test,test2
parameter:
    --show        Show all Payload
    -f  --file     list of files
    -p  --payload  Specify a single payload type or single, multiple payloads to execute. Use (,) to separate multiple payloads
    -t  --thread   Specifies the number of thread pool concurrency
''', end='')


def get_time1():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def get_time2():
    return time.strftime("%H:%M:%S", time.localtime())


if 'Windows' in platform.system():
    STD_INPUT_HANDLE = -10
    STD_OUTPUT_HANDLE = -11
    STD_ERROR_HANDLE = -12
    FOREGROUND_BLUE = 0x09
    FOREGROUND_GREEN = 0x0a
    FOREGROUND_DEEPGREEN = 0x02
    FOREGROUND_RED = 0x0c
    FOREGROUND_YELLOW = 0x0e
    FOREGROUND_WHITE = 0x0f

    std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)


    def set_cmd_text_color(color, handle=std_out_handle):
        ok = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
        return ok


    def resetColor():
        set_cmd_text_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)


    def printGreen(mess):
        set_cmd_text_color(FOREGROUND_GREEN)
        sys.stdout.write(mess)
        sys.stdout.flush()
        resetColor()


    def printRed(mess):
        set_cmd_text_color(FOREGROUND_RED)
        sys.stdout.write(mess)
        sys.stdout.flush()
        resetColor()


    def printYellow(mess):
        set_cmd_text_color(FOREGROUND_YELLOW)
        sys.stdout.write(mess)
        sys.stdout.flush()
        resetColor()


    def printDeepGreen(mess):
        set_cmd_text_color(FOREGROUND_DEEPGREEN)
        sys.stdout.write(mess)
        sys.stdout.flush()
        resetColor()


    def printBlue(mess):
        set_cmd_text_color(FOREGROUND_BLUE)
        sys.stdout.write(mess)
        sys.stdout.flush()
        resetColor()


    def printWhite(mess):
        set_cmd_text_color(FOREGROUND_WHITE)
        sys.stdout.write(mess + '\n')
        sys.stdout.flush()
        resetColor()


    def get_INFO():
        printBlue('[{0}] '.format(get_time2()))
        printDeepGreen('[INFO] ')


    def get_SUCCESS():
        printBlue('[{0}] '.format(get_time2()))
        printGreen('[SUCCESS] ')


    def get_WARNING():
        printBlue('[{0}] '.format(get_time2()))
        printYellow('[WARNING] ')


    def get_CRITICAL():
        printBlue('[{0}] '.format(get_time2()))
        printRed('[CRITICAL] ')

else:
    DEEP_GREEN = "\033[30;1m{0}\033[0m"
    GREEN = "\033[32;1m{0}\033[0m"
    WHITE = "\033[29;1m{0}\033[0m"
    RED = "\033[31;1m{0}\033[0m"
    YELLOW = "\033[33;1m{0}\033[0m"
    BLUE = "\033[34;1m{0}\033[0m"


    def get_INFO():
        print('{0} {1} '.format(BLUE.format('[' + get_time2() + ']'), GREEN.format('[INFO]')), end='')


    def get_SUCCESS():
        print('{0} {1} '.format(BLUE.format('[' + get_time2() + ']'), GREEN.format('[SUCCESS]')), end='')


    def get_WARNING():
        print('{0} {1} '.format(BLUE.format('[' + get_time2() + ']'), YELLOW.format('[WARNING]')), end='')


    def get_CRITICAL():
        print('{0} {1} '.format(BLUE.format('[' + get_time2() + ']'), RED.format('[CRITICAL]')), end='')


    def printWhite(mess):
        print('{0}'.format(WHITE.format(mess)))


def status_print(value='', status=-1):
    if status == -1:
        print(value)
    elif status == 0:
        get_INFO()
        print(value)
    elif status == 1:
        get_SUCCESS()
        printWhite(value)
    elif status == 2:
        get_WARNING()
        print(value)
    elif status == 3:
        get_CRITICAL()
        print(value)
    elif status == 4:
        printWhite(value)


def show(payload_module_list):
    payload_info_list = []
    type_query = 0  # 查询
    type_swap = 0  # 交互
    type_faucet = 0  # 水龙头
    type_playwright = 0  # 模拟
    type_mint = 0  # mint nft
    type_transfer = 0  # 转账
    status_print('[*] Loading Payload ......', 0)
    for payload_module in payload_module_list:
        path = payload_module.__file__
        try:
            result = payload_module.payload_info()
            name = result['Name']
            payload_type = result['Type']
            network = result['Network']
            description = result['Description']
            description_cn = result['Description_cn']
            if 'query' in result['Type']:
                type_query += 1
            elif 'swap' in result['Type']:
                type_swap += 1
            elif 'playwright' in result['Type']:
                type_playwright += 1
            elif 'mint' in result['Type']:
                type_mint += 1
            elif 'transfer' in result['Type']:
                type_transfer += 1
            else:
                type_faucet += 1
        except Exception as e:
            print(e)
            continue
        payload_info = (name, path, payload_type, network, description, description_cn)
        payload_info_list.append(payload_info)
    for (name, path, payload_type, network, description, description_cn) in payload_info_list:
        if 'Windows' in platform.system():
            printDeepGreen('[+] Name: {0}\n'.format(name))
            print('    Payload_Type: {0}'.format(payload_type))
            print('    Network: {0}'.format(network))
            print('    FileName: {0}'.format(path.split('\\')[-1]))
            print('    Path: {0}'.format(path))
            print('    Description: {0}'.format(path))
            print('    Description_cn: {0}'.format(path))
        else:
            print('{0}\n'.format(GREEN.format('[+] Name: {0}'.format(name))), end='')
            print('    Payload_Type: {0}'.format(payload_type))
            print('    Network: {0}'.format(network))
            print('    FileName: {0}'.format(path.split('/')[-1]))
            print('    Path: {0}'.format(path))
            print('    Description: {0}'.format(description))
            print('    Description_cn: {0}'.format(description_cn))
    print(
        '''[*] Total Payload: {0} \n[~] Query: {1} Swap: {2} Faucet: {3} Mint: {4} Transfer: {5} Playwright: {6}'''
        .format(len(payload_info_list), type_query, type_swap, type_faucet, type_mint, type_transfer, type_playwright))


def output(futures):
    succeed_report = []
    fail_report = []
    for future in futures:
        try:
            result = future.result()
            if result['Succeed']:
                status_print('[*] Executing Payload[{0}]Address:{1} '.format(result['Name'], result['Address']), 1)
                succeed_report.append(result)
            else:
                status_print('[*] Executing Payload[{0}]Address:{1}'.format(result['Name'], result['Address']), 2)
                fail_report.append(result)
        except Exception as e:
            status_print(f'[-] An Error is Generated in the Payload {e}', 2)
            pass
    status_print('[*] All Tasks Are Completed And The Report is About To Be Generated......', 0)
    # 打印报告并写入
    if len(succeed_report) != 0:
        status_print(f"[*] Succeed_Tasks: {len(succeed_report)} ", 0)
        for result in succeed_report:
            status_print(f"[*] Report:[{result['Type']}]{result['Name']}|{result['Address']}|{result['Payload_msg']}",
                         0)
            with open('succeed_report.txt', 'a+') as report_file:
                report_file.write(
                    f"{get_time1()}[{result['Type']}]{result['Name']}|{result['Address']}|{result['Payload_msg']}\n")
    if len(fail_report) != 0:
        status_print(f"[*] Fail_Tasks: {len(fail_report)} ", 2)
        for result in fail_report:
            status_print(f"[-] Report:[{result['Type']}]{result['Name']}|{result['Address']}|{result['Payload_msg']}",
                         2)
            with open('fail_report.txt', 'a+') as report_file:
                report_file.write(
                    f"{get_time1()}[{result['Type']}]{result['Name']}|{result['Address']}|{result['Payload_msg']}\n")
