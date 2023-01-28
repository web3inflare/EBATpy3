import argparse
from lib.utils.output import banner
from lib.console import EBATpy3_console


def get_parser():
    parser = argparse.ArgumentParser(usage="""\n      Python3 EBATpy3.py -t 10 -p all""",
                                     description='Web3 Blockchain Airdrop Task Script Rapid Response Framework Developed Based on Python3', )
    p = parser.add_argument_group('EBATpy3 Arguments')
    p.add_argument("-p", "--payload", type=str,
                   help='Specify a single payload type or single, multiple payloads to execute. Use (,) to separate multiple payloads')
    p.add_argument("-f", "--file", type=str, help="Wallet list", default="wallet.csv")
    p.add_argument("-t", "--thread", type=int, help="Specify the maximum concurrent number of thread pools",
                   default="10")
    p.add_argument("--show", action='store_true', help="List All Payloads")
    p.add_argument("--check", action='store_true', help="Detect the profile")
    args = parser.parse_args()
    return args


def main():
    banner()
    args = get_parser()
    EBATpy3_console(args)


if __name__ == '__main__':
    main()
