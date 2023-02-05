"""
@Time ： 2023/2/3 06:55
@Auth ： Web3inFlare
@File ：mint_testnet_sui.py
@IDE ：PyCharm
@Motto: 咕咕嘎嘎
"""
import base64
import time

import uuid
from typing import Optional

import bip_utils
import hashlib
from thirdlib.sui_python_sdk.wallet import SuiWallet
from thirdlib.sui_python_sdk.provider import SuiJsonRpcProvider
from thirdlib.sui_python_sdk.rpc_tx_data_serializer import RpcTxDataSerializer
from thirdlib.sui_python_sdk.signer_with_provider import SignerWithProvider
from thirdlib.sui_python_sdk.models import TransferObjectTransaction, TransferSuiTransaction, MoveCallTransaction


def payload_info():
    result = {
        'Name': 'mint_testnet_sui',
        'Author': 'web3inflare',
        'Type': 'mint',
        'CreateDate': '2023-2-3',
        'UpdateDate': '2023-2-3',
        'Network': "testnet",
        'Description': "Sui Testnet mint",
        'Description_cn': "Sui Testnet mint",
    }
    return result


def run(**kwargs):
    sui_address = kwargs['sui_address']
    sui_mnemonic = kwargs['sui_mnemonic']
    result = {
        'Name': 'mint_testnet_sui',
        'Type': 'mint',
        'Address': sui_address,
        'Succeed': False,
        'Payload_msg': ''
    }
    try:
        my_wallet = SuiWallet(mnemonic=sui_mnemonic)
        faucet_url = "https://faucet.testnet.sui.io/gas"
        rpc_url = "https://fullnode.testnet.sui.io"
        provider = SuiJsonRpcProvider(rpc_url=rpc_url, faucet_url=faucet_url)
        serializer = RpcTxDataSerializer(rpc_url=rpc_url)
        signer = SignerWithProvider(provider=provider, serializer=serializer, signer_wallet=my_wallet)
        tmp_move_call = MoveCallTransaction(
            package_object_id="0x2",
            module="devnet_nft",
            function="mint",
            type_arguments=[],
            arguments=[
                "web3inflare", "by web3inflare",
                "https://gateway.pinata.cloud/ipfs/QmS3rQmQvZzVgnrpTbNSiRMLGyTGU8bhoSKpRFe3U2Yy9p?_gl=1"
            ],
            gas_budget=1000,
            gas_payment=None,
        )
        mint_result = signer.execute_move_call(tx_move_call=tmp_move_call)
        # 这个返回值真的是又臭又长
        if 'success' in mint_result.get('result').get('EffectsCert').get('effects').get('effects').get('status').get('status'):
            result['Payload_msg'] = "mint success"
            result['Succeed'] = True
            return result
        else:
            result['Payload_msg'] = f"mint fail {mint_result}"
            return result
    except Exception as e:
        result['Payload_msg'] = e
        return result


if __name__ == '__main__':
    test = run(wallet_address='xxxx')
