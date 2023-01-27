"""
@Time ： 2023/1/20 17:35
@Auth ： Web3inFlare
@File ：query_testnet_eth_goerli.py
@IDE ：PyCharm
@Motto: 咕咕嘎嘎
"""
from web3 import Web3, HTTPProvider


def get_balance(address):
    rpc = 'https://rpc.ankr.com/eth_goerli'
    checksum_address = Web3.toChecksumAddress(address)
    web3 = Web3(HTTPProvider(rpc))
    balance = web3.fromWei(web3.eth.get_balance(checksum_address), "ether")
    return balance


def payload_info():
    result = {
        'Name': 'query_testnet_eth_goerli',
        'Author': 'web3inflare',
        'Type': 'query',
        'CreateDate': '2023-1-19',
        'UpdateDate': '2023-1-27',
        'Network': "testnet",
        'Description': "query eth goerli balance",
        'Description_cn': "查询 eth goerli 余额",
    }
    return result


def run(**kwargs):
    wallet_address = kwargs['wallet_address']
    result = {
        'Name': 'query_testnet_eth_goerli',
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
    test = run("0x8dc847af872947ac18d5d63fa646eb65d4d99560")
    print(test['Payload_msg'])
