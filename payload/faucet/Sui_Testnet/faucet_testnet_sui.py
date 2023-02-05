"""
@Time ： 2023/2/2 01:29
@Auth ： Web3inFlare
@File ：faucet_testnet_sui.py
@IDE ：PyCharm
@Motto: 咕咕嘎嘎
"""
import random
import string
import time

import requests
import yaml
from twocaptcha import TwoCaptcha
import websocket
import json
# from lib.utils.proxy import proxy_test  # 用于本地代理
from lib.utils.proxy import get_proxy

with open('config.yaml', encoding='utf-8') as f:
    cont = f.read()
    config = yaml.load(cont, Loader=yaml.SafeLoader)

TwoCaptcha_Api = config['TwoCaptcha']['key']
solver = TwoCaptcha(TwoCaptcha_Api, softId=16726159)


def finger():
    r = requests.get('https://discordapp.com/api/v9/experiments', proxies=get_proxy())
    if r.status_code == 200:
        fingerprint = r.json()['fingerprint']
        return fingerprint
    else:
        print('Error')


def get_headers(token):
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'en-GB',
        'authorization': token,
        'content-type': 'application/json',
        'origin': 'https://discord.com',
        'referer': 'https://discord.com/channels/@me',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'cookie': '__dcfduid=23a63d20476c11ec9811c1e6024b99d9; __sdcfduid=23a63d21476c11ec9811c1e6024b99d9e7175a1ac31a8c5e4152455c5056eff033528243e185c5a85202515edb6d57b0; locale=en-GB',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.1.9 Chrome/83.0.4103.122 Electron/9.4.4 Safari/537.36',
        'x-debug-options': 'bugReporterEnabled',
        'x-context-properties': 'eyJsb2NhdGlvbiI6IlVzZXIgUHJvZmlsZSJ9',
        'x-fingerprint': finger(),
        'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjAuMS45Iiwib3NfdmVyc2lvbiI6IjEwLjAuMTc3NjMiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiY2xpZW50X2J1aWxkX251bWJlciI6OTM1NTQsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9',
        'te': 'trailers',
    }
    return headers


def receive_json_response(ws):
    try:
        response = ws.recv()
        if response:
            return json.loads(response)
    except Exception as e:
        return f"Failed to get message {e}"


def heartbeat(ws):
    heartbeat_json = {"op": 1, "d": "null"}
    send_json_request(ws, heartbeat_json)


def send_json_request(ws, request):
    ws.send(json.dumps(request))


def click_verify_channel(token, proxies):
    """
    这个函数用于点击机器热验证按钮
    """
    url = "https://discord.com/api/v9/interactions"
    click_payload = {
        "type": 3,
        "nonce": None,
        "guild_id": "916379725201563759",
        "channel_id": "1032753438158749726",
        "message_flags": 0,
        "message_id": "1032754263555850330",
        "application_id": "908133353255997441",
        "session_id": "5d718ee1275f7ccd832cc0dff63c329c",
        "data": {
            "component_type": 2,
            "custom_id": "verify"
        }
    }
    # 返回状态码
    result = requests.post(url, headers=get_headers(token), json=click_payload,
                           proxies=proxies, timeout=20)
    return result.status_code


def joiner_server(token, proxies):
    """
    初始化 加入服务器
    :param proxies:
    :param token: discord token
    :return:
    """
    # 加入服务器
    join_request = requests.post(f"https://discord.com/api/v9/invites/sui", headers=get_headers(token=token), json={},
                                 proxies=proxies)

    # 判断是否有验证码
    # 如果有bypass 它
    if join_request.status_code == 400:
        try:
            site_key = join_request.json()['captcha_sitekey']
            bypass_captcha = solver.hcaptcha(site_key, "https://discord.com/channels/@me")['code']
        except Exception as e:
            return f'The Verification Code has Expired or There is no Balance : {e}'
        captcha_join_request = requests.post(f"https://discord.com/api/v9/invites/sui",
                                             headers=get_headers(token=token),
                                             json={"captcha_key": bypass_captcha})
        if captcha_join_request.status_code == 200:
            return captcha_join_request.status_code
        else:
            return captcha_join_request.text

    # 无需验证码
    elif join_request.status_code == 200:
        return join_request.status_code


def websocket_connect(token, proxies):
    # 使用websocket来读取验证机器人的消息
    # http常规请求是无法获取
    try:
        # 连接 discord的websocket服务器
        # 处理代理格式
        ws_proxy = proxies['http'].replace("http://", "").split(":")
        ws = websocket.WebSocket()
        ws.connect("wss://gateway.discord.gg/?v=9&encoding=json", http_proxy_host=f"{ws_proxy[0]}",
                   http_proxy_port=f"{ws_proxy[1]}",
                   proxy_type="http")
        # 发送登陆token
        payload_event = {"op": 2,
                         "d": {"token": token, "properties": {"$os": "linux", "$browser": "chrome", "$device": "pc"}}}
        heartbeat(ws)
        send_json_request(ws, payload_event)
        # 初始化 websocket 连接 discord 完毕
    except Exception as e:
        return f'websocket Unable to link {e}'
    # 发送验证按钮
    if click_verify_channel(token, proxies) == 204:
        event_dict = {}
        # 循环拿到机器人指定消息
        while True:
            try:
                event = receive_json_response(ws)
                if event['d']['author']['username'] == "Sui Verification":
                    event_dict.update(event)
                    break
            except:
                pass
        # 获取 验证图片地址
        captcha_url = event_dict['d']['embeds'][0]['image']['url']
        # 循环拿到验证选择项
        option_value = []
        for option in event_dict['d']['components'][0]['components'][0]['options']:
            value = option['value']
            option_value.append(value)
        # 构造bypass captcha
        try:
            # 验证码
            result_captcha = \
                solver.normal(f"{captcha_url}", hintText=f"Type green symbols only,options: {option_value}",
                              caseSensitive=1)['code']
        except Exception as e:
            return f' Bot Captcha bypass failed {e}'
        # 构造请求包
        url = "https://discord.com/api/v9/interactions"
        click_payload_1 = {
            "type": 3,
            "nonce": None,
            "guild_id": event_dict['d']['message_reference']['guild_id'],
            "channel_id": event_dict['d']['channel_id'],
            "message_flags": 64,
            "message_id": event_dict['d']['id'],
            "application_id": event_dict['d']['application_id'],
            "session_id": "55b0bf1483c78394d05e737bcdb8c9f4",
            "data": {
                "component_type": 3,
                "custom_id": "select",
                "type": 3,
                "values": [
                    f"{result_captcha}"
                ]
            }
        }
        # 发送验证码
        send_captcha = requests.post(url, headers=get_headers(token=token), json=click_payload_1,
                                     proxies=proxies, timeout=20)
        if send_captcha.status_code == 204:
            # 403 验证通过
            return 403
    else:
        # 403 验证通过
        return 403


def faucet(wallet_address, token, proxies):
    # 创建一个nonce  值
    nonce = ''.join(random.choices(string.digits, k=19))
    payload = {
        "content": f"!faucet {wallet_address}",
        "nonce": nonce,
        "tts": False,
        "flags": 0
    }
    # token值
    headers = {
        "authorization": token,
        "content-type": "application/json"
    }
    url = "https://discord.com/api/v9/channels/1037811694564560966/messages"
    response = requests.request("POST", url, json=payload, headers=headers, proxies=proxies, timeout=20)
    # 判断是否发送成功 成功返回200 失败返回内容
    if response.status_code == 200:
        return 200
    else:
        return response.text


def payload_info():
    result = {
        'Name': 'faucet_testnet_sui',
        'Author': 'web3inflare',
        'Type': 'faucet',
        'CreateDate': '2023-2-2',
        'UpdateDate': '2023-2-2',
        'Network': "testnet",
        'Description': "faucet Sui Testnet",
        'Description_cn': "领取 Sui 测试网 ",
    }
    return result


def run(**kwargs):
    wallet_address = kwargs['sui_address']
    token = kwargs['discord_token']
    result = {
        'Name': 'faucet_testnet_sui',
        'Type': 'faucet',
        'Address': wallet_address,
        'Succeed': False,
        'Payload_msg': ''

    }
    # 获取代理
    proxy = get_proxy()
    # proxy = proxy_test()
    # 判断代理是不是可以使用
    if proxy is None:
        # 如果不可用 直接退出程序
        result['Payload_msg'] = "A proxy is required"
        return result
    try:
        joiner_server_result = joiner_server(token=token, proxies=proxy)
        # 加入成功后我们开始判断
        if joiner_server_result == 200:
            # 开启一个websocket 来监听消息
            # 如果验证通过开始执行发送消息进行领水
            if websocket_connect(token, proxy) == 403:
                # 开始发送水龙头
                faucet_result = faucet(wallet_address, token, proxy)
                if faucet_result == 200:
                    result['Payload_msg'] = 'Sui faucet succeed'
                    result['Succeed'] = True
                    return result
                else:
                    result['Payload_msg'] = f'Sui faucet fail {faucet_result}'
                    return result
        else:
            result['Payload_msg'] = f'discord_token Login failed/Failed to join server| {joiner_server_result}'
            return result
    except Exception as e:
        result['Payload_msg'] = e
        return result


if __name__ == '__main__':
    test = run()
