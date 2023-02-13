"""
@Time ： 2023/2/13 18:51
@Auth ： Web3inFlare
@File ：query_testnet_sui.py
@IDE ：PyCharm
@Motto: 咕咕嘎嘎
"""

from thirdlib.sui_python_sdk.rpc_tx_data_serializer import RpcTxDataSerializer


def get_balance(sui_address):
    try:
        rpc_url = "https://fullnode.testnet.sui.io/"
        serializer = RpcTxDataSerializer(rpc_url=rpc_url)
    except Exception as e:
        return f"Wallet initialization failed {e}"
    return serializer.get_balance(sui_address)


def payload_info():
    result = {
        'Name': 'query_testnet_sui',
        'Author': 'web3inflare',
        'Type': 'query',
        'CreateDate': '2023-1-22',
        'UpdateDate': '2023-1-27',
        'Network': "testnet",
        'Description': "query Sui Testnet   balance",
        'Description_cn': "查询 Sui 测试网 余额",
    }
    return result


def run(**kwargs):
    # sui_address = kwargs['sui_address']
    sui_address = '0x6b4e64d71fdfbb5b760ec37531221da153533d3f'
    result = {
        'Name': 'query_testnet_sui',
        'Type': 'query',
        'Address': sui_address,
        'Succeed': False,
        'Payload_msg': ''

    }
    try:
        result['Payload_msg'] = f'{get_balance(sui_address)} Balance'
        result['Succeed'] = True
        return result
    except Exception as e:
        result['Payload_msg'] = e
        return result


if __name__ == '__main__':
    test = run()
    print(test['Payload_msg'])
