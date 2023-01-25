
# EBApy3
[![Python 3.x](https://img.shields.io/badge/python-3.x-yellow.svg)](https://www.python.org/)[![Twitter](https://img.shields.io/badge/twitter-@web3inflare-blue.svg)](https://twitter.com/web3inflare)

[英语](./README.md)
## 概述
基于Python3开发的Web3区块链空投任务脚本快速响应框架

## 特征

- 有效负载脚本可以在 'query'、“faucet”、“swap”模式下以不同的方式运行
- 支持队列多线程池模式
- 支持代理，验证码绕过，钱包生成器



## 技术栈

**python** 


## 要求
- Python 3.7+
- Works on Linux, Windows, Mac OSX, BSD, etc.
## 安装

Install EBATpy3

``` bash
# windows,mac,linux 
pip3 install -r requirements.txt
```
## 使用示例

``` bash
# 显示所有 payload
python3  EBATpy3.py --show
# 使用所有 payload
python3 EBATpy3.py -p all 
# 使用单个payload
python3 EBATpy3.py -p faucet_scrolltest 
# 使用多个 payload
python3 EBATpy3.py -p faucet_scrolltest,faucet_taikotest
# 使用 faucet 类型的 payload
python3 EBATpy3.py -p faucet 
# 设置线程池大小
python3 EBATpy3.py -p all -t 100
```

## 常见问题
### proxy
```
注册  https://doveproxy.net/ 
1.goto API Builder
Proxy Authentication Methods -> use ip whitelist
Service duration -> 35 minutes
Protocol -> http
Output Format  -> text
Get quantity -> 1
Simulation of Proxy Generator
get Proxy API

请添加ip进白名单！

```
***配置 config.yaml***
###  验证码
```
注册  https://2captcha.com/

```
***配置 config.yaml***

###  运行出现 ImportError: cannot import name 'getargspec' from 'inspect'
查找到文件
windows:
C:\Users\Administrator\AppData\Local\Programs\Python\Python311\Lib\site-packages\parsimonious
```text
# parsimonious.py
修改为
from inspect import getfullargspec

```

## 待办事项
- [ ]  优化钱包读取
- [ ]  添加钱包生成器脚本
- [ ]  添加控制台模式

## 支持
如有bug 等问题，请打开issue 

如需支持 请发送邮件到我的 web3inflare.root@proton.me 或者推特 (@web3inflare)


## 贡献


随意贡献，可用打开Issue 或者PRs 提交申请


## 作者

- [@web3inflare](https://www.github.com/web3inflare)


## 鸣谢

 - xiaoxiping


## License

[MIT](https://choosealicense.com/licenses/mit/)

