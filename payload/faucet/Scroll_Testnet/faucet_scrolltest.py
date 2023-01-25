"""
@Time ： 2023/1/24 20:53
@Auth ： Web3inFlare
@File ：faucet_scrolltest.py
@IDE ：PyCharm
@Motto: 咕咕嘎嘎
"""


import requests
import yaml
from twocaptcha import TwoCaptcha
from lib.utils.proxy import get_proxy

with open('config.yaml', encoding='utf-8') as f:
    cont = f.read()
    config = yaml.load(cont, Loader=yaml.SafeLoader)

# 读取 配置文件

TwoCaptcha_Api = config['TwoCaptcha']['key']
solver = TwoCaptcha(TwoCaptcha_Api)


def faucet(address, get_recaptcha_token, proxies):
    payload = f"-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"address\"\r\n\r\n{address}\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"h-captcha-response\"\r\n\r\n{get_recaptcha_token}\r\n-----011000010111000001101001--\r\n\r\n"
    headers = {
        "Accept": "*/*",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "multipart/form-data; boundary=---011000010111000001101001",
        "Origin": "https://scroll.io",
        "Pragma": "no-cache",
        "Referer": "https://scroll.io/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    }
    response = requests.request("POST", "https://prealpha-api.scroll.io/faucet/api/claim", data=payload, headers=headers, proxies=proxies, verify=False)
    return response.text


def run(address, *args):
    result = {
        'Name': 'faucet_scrolltest',
        'Author': 'web3inflare',
        'Type': 'faucet',
        'CreateDate': '2023-1-24',
        'UpdateDate': '2023-1-24',
        'Network': "testnet",
        'Description': "faucet Scroll Testnet",
        'Description_cn': "领取 Scroll ",
        'Address': address,
        'Succeed': False,
        'Payload_msg': ''

    }
    try:
        get_recaptcha_token = \
            solver.hcaptcha('541838f2-e585-4726-b398-24102b1d4df8', "https://scroll.io/prealpha/faucet")['code']
        faucet_result = faucet(address, get_recaptcha_token, get_proxy())
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
    test = run("0x8dc847af872947ac18d5d63fa646eb65d4d99560")
    print(test['Payload_msg'])
