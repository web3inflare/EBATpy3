"""
@Time ： 2023/1/30 21:33
@Auth ： Web3inFlare
@File ：query_testnet_aptos.py
@IDE ：PyCharm
@Motto: 咕咕嘎嘎
"""
from aptos_sdk.client import RestClient


def get_balance(apt_wallet_address):
    # 初始化 RPC
    rest_client = RestClient("https://fullnode.testnet.aptoslabs.com/v1")
    # 如果没有余额 就会异常，我们直接捕获异常 返回这个钱包地址为0
    try:
        balance = rest_client.account_balance(f"{apt_wallet_address}")
    except:
        return '0'
    # 返回余额 转换格式
    return int(balance)/100000000


def payload_info():
    result = {
        'Name': 'query_testnet_aptos',
        'Author': 'web3inflare',
        'Type': 'query',
        'CreateDate': '2023-1-30',
        'UpdateDate': '2023-1-30',
        'Network': "testnet",
        'Description': "query APTos Testnet balance",
        'Description_cn': "查询 APTos 测试网 余额",
    }
    return result


def run(**kwargs):
    apt_wallet_address = kwargs['apt_wallet_address']
    result = {
        'Name': 'query_testnet_aptos',
        'Type': 'query',
        'Address': apt_wallet_address,
        'Succeed': False,
        'Payload_msg': ''
    }
    try:
        result['Payload_msg'] = f'{get_balance(apt_wallet_address)} Balance'
        result['Succeed'] = True
        return result
    except Exception as e:
        result['Payload_msg'] = e
        return result


if __name__ == '__main__':
    test = run(wallet_address='xxxx')
