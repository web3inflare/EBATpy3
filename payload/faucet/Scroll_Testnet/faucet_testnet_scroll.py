"""
@Time ： 2023/1/24 20:53
@Auth ： Web3inFlare
@File ：faucet_testnet_scroll.py
@IDE ：PyCharm
@Motto: 咕咕嘎嘎
"""

import requests
import yaml
from twocaptcha import TwoCaptcha
from lib.utils.proxy import get_proxy
# from lib.utils.proxy import proxy_test
with open('config.yaml', encoding='utf-8') as f:
    cont = f.read()
    config = yaml.load(cont, Loader=yaml.SafeLoader)

# 读取 配置文件

TwoCaptcha_Api = config['TwoCaptcha']['key']
solver = TwoCaptcha(TwoCaptcha_Api)


def faucet(address, token, proxies):
    payload = f"-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"address\"\r\n\r\n{address}\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"h-captcha-response\"\r\n\r\n{token}\r\n-----011000010111000001101001--\r\n\r\n"
    headers = {
        "authority": "prealpha-api.scroll.io",
        "accept": "*/*",
        "content-type": "multipart/form-data; boundary=---011000010111000001101001",
        "origin": "https://scroll.io",
        "referer": "https://scroll.io/",
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41",
        "Accept-Encoding": "deflate, gzip"
    }
    response = requests.request("POST", "https://prealpha-api.scroll.io/faucet/api/claim", data=payload,
                                headers=headers, proxies=proxies, verify=False)
    return response.text


def payload_info():
    result = {
        'Name': 'faucet_testnet_scroll',
        'Author': 'web3inflare',
        'Type': 'faucet',
        'CreateDate': '2023-1-24',
        'UpdateDate': '2023-1-27',
        'Network': "testnet",
        'Description': "faucet Scroll Testnet",
        'Description_cn': "领取 Scroll ",
    }
    return result


def run(**kwargs):
    wallet_address = kwargs['wallet_address']
    result = {
        'Name': 'faucet_testnet_scroll',
        'Type': 'faucet',
        'Address': wallet_address,
        'Succeed': False,
        'Payload_msg': ''

    }
    try:
        get_captcha_token = \
            solver.hcaptcha('65f2be91-305e-428f-a85e-347b038bf930', "https://scroll.io/prealpha/faucet")['code']
        faucet_result = faucet(wallet_address, get_captcha_token, get_proxy())
        if 'eth_tx_hash' in faucet_result:
            result['Payload_msg'] = 'Faucet Succeed'
            result['Succeed'] = True
            return result
        else:
            result['Payload_msg'] = faucet_result
            return result
    except Exception as e:
        result['Payload_msg'] = e
        return result


if __name__ == '__main__':
    test = run()
    print(test['Payload_msg'])
