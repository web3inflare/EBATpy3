"""
@Time ： 2023/1/28 22:09
@Auth ： Web3inFlare
@File ：bridge_testnet_scroll_l1.py
@IDE ：PyCharm
@Motto: 咕咕嘎嘎
"""

from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
from lib.utils.proxy import get_proxy_simple


def transfer_bridge_eth(w3, wallet_address, wallet_key):
    try:
        # 校正地址
        from_address = Web3.toChecksumAddress(wallet_address)
        # 合约地址
        target_address = Web3.toChecksumAddress('0x47c02b023b6787ef4e503df42bbb1a94f451a1c0')
        # 获取nonce值
        nonce = w3.eth.getTransactionCount(wallet_address)
        # 获取余额
        balance = w3.eth.getBalance(wallet_address)
        transfer_balance = balance - round(1.3 * 122355 * w3.eth.gas_price)
        # 开始一个构造事务
        params = {
            'from': from_address,
            'nonce': nonce,
            'data': '0x5358fbda0000000000000000000000000000000000000000000000000000000000000000',
            'to': target_address,
            'value': transfer_balance,
            'chainId': w3.eth.chain_id,
            'gas': 122355,
            'gasPrice': w3.eth.gas_price
        }
        # 构造完毕我们开始发送
        signed_tx = w3.eth.account.signTransaction(params, private_key=wallet_key)
        # 获取tx
        txn = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        # 返回tx 和发送余额
        return w3.toHex(txn), w3.fromWei(transfer_balance, "ether")
    except Exception as e:
        return e


def bridge(wallet_address, wallet_key):
    try:
        # 检测是否使用代理
        # 使用代理发送
        if get_proxy_simple() is not None:
            # 获取代理链接
            w3_proxy = get_proxy_simple()
            # 构造代理连接rpc
            w3 = Web3(HTTPProvider('https://prealpha.scroll.io/l1', request_kwargs={
                "proxies": {'https': f"http://{w3_proxy}", 'http': f"http://{w3_proxy}"}}))
            w3.middleware_onion.inject(geth_poa_middleware, layer=0)
            # 获取l1网络上的余额
            get_balance = w3.eth.getBalance(wallet_address)
            # 余额是否大于l1网络上的gas
            if get_balance > 1.3 * 21000 * w3.eth.gas_price:
                # 开始bridge
                # 得到返回值
                transfer_bridge_eth_result = transfer_bridge_eth(w3, wallet_address, wallet_key)
            else:
                return 'Insufficient balance'
            return f'Use a proxy,bridge Succeed tx: https://l1scan.scroll.io/tx/{transfer_bridge_eth_result[0]},Send balance: {transfer_bridge_eth_result[1]} ETH'
        # 不使用代理发送
        else:
            # 导入rpc接口
            w3 = Web3(HTTPProvider('https://prealpha.scroll.io/l1'))
            # poa链
            w3.middleware_onion.inject(geth_poa_middleware, layer=0)
            # 获取l1网络上的余额
            get_balance = w3.eth.getBalance(wallet_address)
            # 余额是否大于l1网络上的gas
            if get_balance > 1.3 * 21000 * w3.eth.gas_price:
                # 开始bridge
                transfer_bridge_eth_result = transfer_bridge_eth(w3, wallet_address, wallet_key)
            else:
                return 'Insufficient balance'
            return f'No use proxy,bridge Succeed tx: https://l1scan.scroll.io/tx/{transfer_bridge_eth_result[0]},Send balance: {transfer_bridge_eth_result[1]} ETH'
    except Exception as e:
        return e


def payload_info():
    result = {
        'Name': 'bridge_testnet_scroll_l1',
        'Author': 'web3inflare',
        'Type': 'bridge',
        'CreateDate': '2023-1-20',
        'UpdateDate': '2023-1-28',
        'Network': "testnet",
        'Description': "Scroll testnet bridge L1 to L2",
        'Description_cn': "Scroll 测试网 桥 L1 到 L2",
    }
    return result


def run(**kwargs):
    wallet_address = kwargs['wallet_address']
    wallet_key = kwargs['wallet_key']
    result = {
        'Name': 'bridge_testnet_scroll_L1',
        'Type': 'bridge',
        'Address': wallet_address,
        'Succeed': False,
        'Payload_msg': ''
    }
    try:
        bridge_result = bridge(wallet_address, wallet_key)
        if 'Succeed' in bridge_result:
            result['Payload_msg'] = bridge_result
            result['Succeed'] = True
            return result
        else:
            result['Payload_msg'] = bridge_result
            return result
    except Exception as e:
        result['Payload_msg'] = e
        return result


if __name__ == '__main__':
    test = run(wallet_address='xxxx')
