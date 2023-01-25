"""
@Time ： 2023/1/20 19:13
@Auth ： Web3inFlare
@File ：query_matictest.py
@IDE ：PyCharm
@Motto: 咕咕嘎嘎
"""


from web3 import Web3, HTTPProvider


def get_balance(address):
    rpc = 'https://rpc.ankr.com/polygon_mumbai'
    checksum_address = Web3.toChecksumAddress(address)
    web3 = Web3(HTTPProvider(rpc))
    balance = web3.fromWei(web3.eth.get_balance(checksum_address), "ether")
    return balance


def run(address, *args):
    result = {
        'Name': 'query_matictest',
        'Author': 'web3inflare',
        'Type': 'query',
        'CreateDate': '2023-1-20',
        'UpdateDate': '2023-1-20',
        'Network': "testnet",
        'Description': "query matic(polygon) testnet balance",
        'Description_cn': "查询 matic(polygon) 测试网 余额",
        'Address': address,
        'Succeed': False,
        'Payload_msg': ''

    }
    try:
        result['Payload_msg'] = f'{get_balance(address)} Balance'
        result['Succeed'] = True
        return result
    except Exception as e:
        result['Payload_msg'] = e
        return result


if __name__ == '__main__':
    test = run("0x8dc847af872947ac18d5d63fa646eb65d4d99560")
    print(test['Payload_msg'])