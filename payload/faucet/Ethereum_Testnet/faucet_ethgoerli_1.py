"""
@Time ： 2023/1/24 19:16
@Auth ： Web3inFlare
@File ：faucet_ethgoerli_1.py
@IDE ：PyCharm
@Motto: 咕咕嘎嘎
"""

import requests
import yaml
from twocaptcha import TwoCaptcha
from lib.utils.proxy import get_proxy

requests.packages.urllib3.disable_warnings()

with open('config.yaml', encoding='utf-8') as f:
    cont = f.read()
    config = yaml.load(cont, Loader=yaml.SafeLoader)

# 读取 配置文件

TwoCaptcha_Api = config['TwoCaptcha']['key']
solver = TwoCaptcha(TwoCaptcha_Api)


def faucet(address, get_recaptcha_token, proxies):
    url = "https://www.allthatnode.com/FaucetSvl.dsrv"
    querystring = {"protocol": "ETHEREUM", "network": "GOERLI", "address": f"{address}",
                   "recaptcha": f"{get_recaptcha_token}"}
    headers = {
        "Accept": "application/json, text/plain, */*",
    }
    response = requests.request("GET", url, headers=headers, params=querystring, proxies=proxies)

    return response.text


def run(address, *args):
    result = {
        'Name': 'faucet_ethgoerli_1',
        'Author': 'web3inflare',
        'Type': 'faucet',
        'CreateDate': '2023-1-24',
        'UpdateDate': '2023-1-24',
        'Network': "testnet",
        'Description': "faucet ethgoerli use (allthatnode.com) get 0.025 ETH",
        'Description_cn': "领取 ethgoerli 使用 allthatnode.com 获得 0.025 ETH",
        'Address': address,
        'Succeed': False,
        'Payload_msg': ''

    }
    try:
        get_recaptcha_token = solver.recaptcha('6Lf4qnYfAAAAAMHpsGAYma_WEWH6I9YCfrx7yLNb', "https://www.allthatnode.com/faucet/ethereum.dsrv")['code']
        faucet_result = faucet(address, get_recaptcha_token, get_proxy())
        if 'true' in faucet_result:
            if 'limited' in faucet_result:
                result['Payload_msg'] = faucet_result
                return result
            else:
                result['Payload_msg'] = faucet_result
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
