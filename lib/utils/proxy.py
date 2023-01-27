"""
@Time ： 2023/1/24 22:30
@Auth ： Web3inFlare
@File ：proxy.py
@IDE ：PyCharm
@Motto: 咕咕嘎嘎
"""
import yaml
import requests

requests.packages.urllib3.disable_warnings()

with open('config.yaml', encoding='utf-8') as f:
    cont = f.read()
    config = yaml.load(cont, Loader=yaml.SafeLoader)

proxy_url = config['Proxy_Api']['url']


def get_proxy():
    # 如果不为空
    if proxy_url is not None:
        try:
            # 尝试获取代理ip
            proxy_ip = requests.get(proxy_url, verify=False).text.replace('\r\n', "")
            proxy = {
                "http": f'http://{proxy_ip}',
                "https": f'http://{proxy_ip}'
            }
            #  测试代理是否可用
            test_proxy = requests.get("https://ip.smartproxy.com/", verify=False, proxies=proxy)
            if test_proxy.status_code == 200:
                # 代理可用
                return proxy
            else:
                #  代理不可用
                return None
        except:
            # 获取代理失败
            return None
    # 如果为空 返回None值 即不使用代理
    else:
        return None


# 添加一个代理返回格式
# 有一些类似于websocket 协议的代理模式形式不一样
def get_proxy_simple():
    # 如果不为空
    if proxy_url is not None:
        try:
            # 尝试获取代理ip
            proxy_ip = requests.get(proxy_url, verify=False).text.replace('\r\n', "")
            proxy = {
                "http": f'http://{proxy_ip}',
                "https": f'http://{proxy_ip}'
            }
            #  测试代理是否可用
            test_proxy = requests.get("https://ip.smartproxy.com/", verify=False, proxies=proxy)
            if test_proxy.status_code == 200:
                # 代理可用
                # 返回 ip:prot格式
                return proxy_ip
            else:
                #  代理不可用
                return None
        except:
            # 获取代理失败
            return None
    # 如果为空 返回None值 即不使用代理
    else:
        return None
