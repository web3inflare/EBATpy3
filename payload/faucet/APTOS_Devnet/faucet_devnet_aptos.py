"""
@Time ： 2023/1/30 21:37
@Auth ： Web3inFlare
@File ：faucet_devnet_aptos.py
@IDE ：PyCharm
@Motto: 咕咕嘎嘎
"""
from aptos_sdk.client import RestClient, FaucetClient


def faucet(apt_wallet_address):
    # 初始化 RPC
    rest_client = RestClient("https://fullnode.devnet.aptoslabs.com/v1")
    faucet_client = FaucetClient("https://faucet.devnet.aptoslabs.com", rest_client)
    faucet_client.fund_account(apt_wallet_address, 10_0000000)
    return "Faucet 1 APT Succeed "


def payload_info():
    result = {
        'Name': 'faucet_devnet_aptos',
        'Author': 'web3inflare',
        'Type': 'faucet',
        'CreateDate': '2023-1-30',
        'UpdateDate': '2023-1-30',
        'Network': "devnet",
        'Description': "faucet APTos Devnet balance",
        'Description_cn': "领取 APTos 开发网 测试代币 ",
    }
    return result


def run(**kwargs):
    apt_wallet_address = kwargs['apt_wallet_address']
    result = {
        'Name': 'faucet_devnet_aptos',
        'Type': 'faucet',
        'Address': apt_wallet_address,
        'Succeed': False,
        'Payload_msg': ''
    }
    try:
        result['Payload_msg'] = faucet(apt_wallet_address)
        result['Succeed'] = True
        return result
    except Exception as e:
        result['Payload_msg'] = e
        return result


if __name__ == '__main__':
    test = run(wallet_address='xxxx')
