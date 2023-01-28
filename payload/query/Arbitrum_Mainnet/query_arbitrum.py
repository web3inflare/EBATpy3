"""
@Time ： 2023/1/20 19:19
@Auth ： Web3inFlare
@File ：query_arbitrum.py
@IDE ：PyCharm
@Motto: 咕咕嘎嘎
"""

from web3 import Web3, HTTPProvider


def get_balance(address):
    rpc = 'https://rpc.ankr.com/arbitrum'
    checksum_address = Web3.toChecksumAddress(address)
    web3 = Web3(HTTPProvider(rpc))
    balance = web3.fromWei(web3.eth.get_balance(checksum_address), "ether")
    return balance


def payload_info():
    result = {
        'Name': 'query_arbitrum',
        'Author': 'web3inflare',
        'Type': 'query',
        'CreateDate': '2023-1-20',
        'UpdateDate': '2023-1-27',
        'Network': "mainnet",
        'Description': "query arbitrum balance",
        'Description_cn': "查询 arbitrum  余额",
    }
    return result


def run(**kwargs):
    wallet_address = kwargs['wallet_address']
    result = {
        'Name': 'query_arbitrum',
        'Type': 'query',
        'Address': wallet_address,
        'Succeed': False,
        'Payload_msg': ''
    }
    try:
        result['Payload_msg'] = f'{get_balance(wallet_address)} Balance'
        result['Succeed'] = True
        return result
    except Exception as e:
        result['Payload_msg'] = e
        return result


if __name__ == '__main__':
    test = run(wallet_address='xxxx')
