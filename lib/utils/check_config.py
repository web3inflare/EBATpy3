"""
@Time ： 2023/1/28 20:55
@Auth ： Web3inFlare
@File ：check_config.py
@IDE ：PyCharm
@Motto: 咕咕嘎嘎
"""
import requests
# 检测配置文件功能

import yaml
from twocaptcha import TwoCaptcha
from lib.utils.output import status_print
# 添加 requests 错误提示关闭
requests.packages.urllib3.disable_warnings()

with open('config.yaml', encoding='utf-8') as f:
    cont = f.read()
    config = yaml.load(cont, Loader=yaml.SafeLoader)

# 读取 配置文件
proxy_url = config['Proxy_Api']['url']
TwoCaptcha_Api = config['TwoCaptcha']['key']
solver = TwoCaptcha(TwoCaptcha_Api)


def check_config():
    flag = False
    try:
        balance = solver.balance()
        if balance > 0:
            status_print(f"[*] 2captcha balance: {balance}", 1)
            flag = True
        else:
            status_print(f"[*] 2captcha balance insufficient", 2)
    except Exception as e:
        status_print("[-] There may be an error with the Key！", 2)
        status_print(f"[-] {e}", 2)
    try:
        # 检测代理是否为空
        if proxy_url is not None:
            # 检测代理API 是否能获取到IP
            try:
                proxy_ip = requests.get(proxy_url, verify=False).text.replace('\r\n', "")
                status_print("[-] The proxy API is available", 1)
            except Exception as e:
                status_print(f"[-] Error Code {e}", 2)
                status_print("[-] Proxy API is not available, please enter the correct API URL", 2)
            try:
                # 检测代理是否可以使用
                proxy = {
                    "http": f'http://{proxy_ip}',
                    "https": f'http://{proxy_ip}'
                }
                test_proxy = requests.get("https://ip.smartproxy.com/", verify=False, proxies=proxy)
                if test_proxy.status_code == 200:
                    # 代理IP 可用
                    status_print("[*] Proxy IP available", 1)
                    if flag:
                        # 所有配置文件都可用使用
                        status_print("[*] All configurations are available", 1)
                else:
                    # 代理链接不上 一般来说是白名单没有添加成功
                    # 打印 http代码
                    status_print(f"[-] Error Code {test_proxy.status_code}", 2)
                    status_print("[-] Proxy not available! Please check the proxy whitelist", 2)
            except Exception as e:
                # 检测代理出现问题 输出错误代码
                status_print(f"[-] Error Code {e}", 2)
        else:
            status_print("[*] The proxy configuration is empty, and features other than queries may not be available!",
                         1)
    except Exception as e:
        status_print(f"[-] {e}", 2)
