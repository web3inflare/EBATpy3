"""
@Time ： 2023/1/26 01:52
@Auth ： Web3inFlare
@File ：wallet_generate.py
@IDE ：PyCharm
@Motto: 咕咕嘎嘎
"""
import argparse
import csv
import hashlib

import bip_utils
from aptos_sdk.account import Account as Apt_Account
from eth_account import Account
from tqdm import tqdm


def sui_generate_wallet():
    sui_mnemonic = bip_utils.Bip39MnemonicGenerator().FromWordsNumber(bip_utils.Bip39WordsNum.WORDS_NUM_12).ToStr()
    sui_bip39_seed = bip_utils.Bip39SeedGenerator(sui_mnemonic).Generate()
    sui_bip39_ctx = bip_utils.Bip32Slip10Ed25519.FromSeed(sui_bip39_seed)
    sui_bip39_der_ctx = sui_bip39_ctx.DerivePath("m/44'/784'/0'/0'/0'")
    sui_private_key: bytes = sui_bip39_der_ctx.PrivateKey().Raw().ToBytes()
    sui_public_key: bytes = sui_bip39_der_ctx.PublicKey().RawCompressed().ToBytes()
    sui_address: str = "0x" + hashlib.sha3_256(sui_bip39_der_ctx.PublicKey().RawCompressed().ToBytes()).digest().hex()[
                              :40]
    # 钱包地址，钱包公钥，钱包私钥，钱包助记词
    return sui_address, sui_public_key, sui_private_key, sui_mnemonic


def generate(num, length):
    with open("wallet.csv", 'a', newline='') as file:
        # 表头
        field_name = ['wallet_address', 'wallet_key', 'wallet_mnemonic', 'apt_wallet_address', 'apt_wallet_key',
                      'sui_address', 'sui_public_key', 'sui_private_key', 'sui_mnemonic', 'twitter_user',
                      'twitter_pass',
                      'twitter_verify',
                      'discord_token', 'aws_key', 'aws_secret']
        # 写入字段名，当做表头
        writer = csv.DictWriter(file, fieldnames=field_name)
        writer.writeheader()
        print("[+] Start Generating Wallets")
        print("[*] Support wallet types: EVM,APTos,Sui")
        print(f"[+] EVM Number of wallets:{num}")
        print(f"[+] EVM mnemonic length:{length}")
        print(f"[+] APTos wallet: {num}")
        print(f"[+] Sui wallet: {num}")
        pbar = tqdm(range(num))
        for i in pbar:
            pbar.set_description(desc='Web3inflare')
            Account.enable_unaudited_hdwallet_features()
            account, mnemonic = Account.create_with_mnemonic(num_words=length)
            apt_account = Apt_Account.generate()
            sui_address, sui_public_key, sui_private_key, sui_mnemonic = sui_generate_wallet()
            writer.writerow({'wallet_address': f'{account.address}', 'wallet_key': f'{account.key.hex()}',
                             'wallet_mnemonic': f'{mnemonic}', 'apt_wallet_address': f'{apt_account.address()}',
                             'apt_wallet_key': f'{apt_account.private_key}', 'sui_address': f'{sui_address}',
                             'sui_public_key': f'{sui_public_key}', 'sui_private_key': f'{sui_private_key}',
                             'sui_mnemonic': f'{sui_mnemonic}'})


def get_parser():
    parser = argparse.ArgumentParser(usage="""\n      Python3 wallet_generate.py -t 10 -m 24""",
                                     description='Wallet generator', )
    p = parser.add_argument_group('Wallet generator Arguments')
    p.add_argument("-t", type=int, help="Number of wallets",
                   default="10")
    p.add_argument("-m", type=int, help="mnemonic length",
                   default="24")
    args = parser.parse_args()
    return args


def main():
    args = get_parser()
    generate(args.t, args.m)
    print("[*] The Wallet is Generated")


if __name__ == '__main__':
    main()
