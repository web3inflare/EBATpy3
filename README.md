
# EBApy3
[![Python 3.x](https://img.shields.io/badge/python-3.x-yellow.svg)](https://www.python.org/)[![Twitter](https://img.shields.io/badge/twitter-@web3inflare-blue.svg)](https://twitter.com/web3inflare)

[简体中文](./README_cn.md)
## Overview
Web3 Blockchain Airdrop Task Script Rapid Response Framework Developed Based on Python3

## Features

- Payload scripts can be run in different ways in `query`, `faucet`, `swap` mode
- Support for Queue Multithreaded Pool mode
- Support Proxy, Captcha Bypass,Wallet generator



## Tech Stack

**python** 


## Requirements
- Python 3.7+
- Works on Linux, Windows, Mac OSX, BSD, etc.
## Installation


``` bash
# windows,mac,linux 
pip3 install -r requirements.txt
```
 - window OS:
 - web3 Requires the C++ runtime
https://visualstudio.microsoft.com/
## Usage/Examples

``` bash
# Show all payload
python3  EBATpy3.py --show
# Use all payload
python3 EBATpy3.py -p all 
# Specify a single payload
python3 EBATpy3.py -p faucet_scrolltest 
# Using multiple payloads
python3 EBATpy3.py -p faucet_scrolltest,faucet_taikotest
# Use the specified type payload
python3 EBATpy3.py -p faucet 
# Set thread pool (default 10 threads)
python3 EBATpy3.py -p all -t 100
# Detect the profile
python3  EbATpy3.py --check 
```

## FAQ
### proxy
```
Configure config.yaml
Registration  https://doveproxy.net/ 
1.goto API Builder
Proxy Authentication Methods -> use ip whitelist
Service duration -> 35 minutes
Protocol -> http
Output Format  -> text
Get quantity -> 1
Simulation of Proxy Generator
get Proxy API

note: Add the IP address to the whitelist
```
###  Captcha
```
Configure config.yaml
Registration  https://2captcha.com/
```


###  ImportError: cannot import name 'getargspec' from 'inspect'
windows:
C:\Users\Administrator\AppData\Local\Programs\Python\Python311\Lib\site-packages\parsimonious
```text
# expressions.py
Amend to
# from inspect import getargspec
from inspect import getfullargspec

```
## Changelog
### 2023.1.31
#### Added
 - add Sui , APTos Wallet generator
 - add APTOS Mainnet/Devnet/Testnet balance query
### 2023.1.29
#### Added
 -  Add Scroll Bridge L1 to L2 payload
#### Changed 
 - Fix requirements
 - Fix some details
### 2023.1.28
#### Added
 -  Adds profile detection
#### Changed 
 - Add a bridge type
### 2023.1.27
#### Changed 
 - Fix the payload specification
 - Fixed file read
 - Fix the file directory
#### Added
 - Add Scorll faucet 
 - Add Taiko faucet
 - add Eth goerli faucet  (allthatnode.com)
 - Add Node payload type
### 2023.1.26
#### Added 
 - Add  Wallet Generator 

### 2023.1.25 
 - First upload

## TODO
- [x]  Optimize reading wallet list
- [x]  Add wallet generator
- [ ]  Add console mode
- [x]  Fix the payload specification
- [ ]  Add a testnet node type payload (using AWS)

## Support
If you have a bug, please file an issue

For support, please contact me at web3inflare.root@proton.me
Twitter(@web3inflare)


## Contributing

Feel free to dive in! Open an issue or submit PRs.


## Authors

- [@web3inflare](https://www.github.com/web3inflare)


## Acknowledgements

 - xiaoxiping


## License

[MIT](https://choosealicense.com/licenses/mit/)

