
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
``` bash
# windows,mac,linux 
pip3 install -r requirements.txt
```
 - window OS:
 - web3 需要c++运行库
https://blog.51cto.com/u_8238263/6020380


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
# 检测配置文件
python3  EbATpy3.py --check 
```

## 常见问题
### proxy
```
# 配置 config.yaml
注册  https://doveproxy.net/ 
1.API 生成器
验证方式 -> 使用白名单
ip使用时间 -> 35 分钟
协议 -> http
输出格式  -> text
获取数量-> 1
-----
请添加ip进白名单！
点击生成API URL


```
###  验证码
```
# 配置 config.yaml
注册  https://2captcha.com/

```


###  运行出现 ImportError: cannot import name 'getargspec' from 'inspect'
查找到文件
windows:
C:\Users\Administrator\AppData\Local\Programs\Python\Python311\Lib\site-packages\parsimonious
```text
# expressions.py
修改为
# from inspect import getargspec
from inspect import getfullargspec

```

## 变更日志
### 2023.1.28
#### 添加
 -  添加 配置文件检测功能
#### 变更 
 - 添加 bridge 类型
### 2023.1.27
#### 变更 
 - 变更 payload 规范
 - 优化 文件读取
 - 调整目录
#### 添加
 - 添加 Scorll 水龙头 
 - 添加 Taiko 水龙头
 - 添加 Eth goerli 水龙头  (allthatnode.com)
 - 添加 node payload 类型
### 2023.1.26
#### 添加 
 - 添加 钱包生成器

### 2023.1.25 
 - 首次上传

## 待办事项
- [x]  优化钱包读取
- [x]  添加钱包生成器脚本
- [ ]  添加控制台模式
- [x]  修复 payload 规范
- [ ]  添加测试网节点类型 payload (使用 aws)


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

