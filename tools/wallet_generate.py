"""
@Time ： 2023/1/26 01:52
@Auth ： Web3inFlare
@File ：wallet_generate.py
@IDE ：PyCharm
@Motto: 咕咕嘎嘎
"""
import argparse
import csv
from tqdm import tqdm

from eth_account import Account


def generate(num, length):
    with open("wallet.csv", 'a', newline='') as file:
        # 表头
        field_name = ['wallet_address', 'wallet_key', 'wallet_mnemonic', 'twitter_user', 'twitter_pass',
                      'twitter_verify',
                      'discord_token', 'aws_key', 'aws_secret']
        # 写入字段名，当做表头
        writer = csv.DictWriter(file, fieldnames=field_name)
        writer.writeheader()
        print("[+] Start Generating Wallets")
        print(f"[+] Number of wallets:{num}")
        print(f"[+] mnemonic length :{length}")
        pbar = tqdm(range(num))
        for i in pbar:
            pbar.set_description(desc='Web3inflare')
            Account.enable_unaudited_hdwallet_features()
            account, mnemonic = Account.create_with_mnemonic(num_words=length)
            writer.writerow({'wallet_address': f'{account.address}', 'wallet_key': f'{account.key.hex()}',
                             'wallet_mnemonic': f'{mnemonic}'})


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
