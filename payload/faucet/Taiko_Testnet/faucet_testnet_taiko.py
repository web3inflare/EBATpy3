"""
@Time ： 2023/1/24 23:25
@Auth ： Web3inFlare
@File ：faucet_testnet_taiko.py
@IDE ：PyCharm
@Motto: 咕咕嘎嘎
"""
import json

import requests
import websocket

from lib.utils.twitter_login import tw_login
from lib.utils.proxy import get_proxy


def tw_post(token, add, proxy):
    tweet_text = "I'm requesting Ether from the Ethereum (Taiko's Private L1) faucet to my " \
                 "0x0000000000000000000000000000000000000000 address. Learn more at https://taiko.xyz/docs/intro. ".replace(
        "0x0000000000000000000000000000000000000000", str(add))
    post = {
        "variables": {
            "tweet_text": f"{tweet_text}",
            "dark_request": False,
            "media": {
                "media_entities": [],
                "possibly_sensitive": False
            },
            "withDownvotePerspective": False,
            "withReactionsMetadata": False,
            "withReactionsPerspective": False,
            "withSuperFollowsTweetFields": True,
            "withSuperFollowsUserFields": True,
            "semantic_annotation_ids": []
        },
        "features": {
            "view_counts_public_visibility_enabled": True,
            "view_counts_everywhere_api_enabled": True,
            "tweetypie_unmention_optimization_enabled": True,
            "responsive_web_uc_gql_enabled": True,
            "vibe_api_enabled": True,
            "responsive_web_edit_tweet_api_enabled": True,
            "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
            "interactive_text_enabled": True,
            "responsive_web_text_conversations_enabled": False,
            "responsive_web_twitter_blue_verified_badge_is_enabled": True,
            "verified_phone_label_enabled": False,
            "standardized_nudges_misinfo": True,
            "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": False,
            "responsive_web_graphql_timeline_navigation_enabled": True,
            "responsive_web_enhance_cards_enabled": False
        },
        "queryId": "lsEClsEs3-SvhoORo0zyqg"
    }
    cookie = {
        "auth_token": f'{token}',
        "ct0": requests.get("https://twitter.com/i/release_notes", proxies=proxy, verify=False).cookies.get("ct0")
    }
    headers = {
        "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
        "x-csrf-token": cookie["ct0"],
        "x-twitter-active-user": "yes",
        "x-twitter-auth-type": "OAuth2Session",
        "x-twitter-client-language": "ja",
    }

    check = requests.post(f"https://api.twitter.com/graphql/lsEClsEs3-SvhoORo0zyqg/CreateTweet", cookies=cookie,
                          headers=headers,
                          json=post, proxies=proxy, verify=False)
    res_json = check.json()
    if 'errors' not in res_json.keys():
        return res_json['data']['create_tweet']['tweet_results']['result']['rest_id']
    else:
        return None


def payload_info():
    result = {
        'Name': 'faucet_testnet_taiko',
        'Author': 'web3inflare',
        'Type': 'faucet',
        'CreateDate': '2023-1-24',
        'UpdateDate': '2023-1-24',
        'Network': "testnet",
        'Description': "faucet Taiko Testnet",
        'Description_cn': "领取 Taiko ",

    }
    return result


def run(**kwargs):
    wallet_address = kwargs['wallet_address']
    twitter_user = kwargs['twitter_user']
    twitter_pass = kwargs['twitter_pass']
    twitter_verify = kwargs['twitter_verify']
    result = {
        'Name': 'faucet_testnet_taiko',
        'Type': 'faucet',
        'Address': wallet_address,
        'Succeed': False,
        'Payload_msg': ''

    }
    try:
        # 获取一次 proxy 保持登陆和发送推文使用同一个ip
        proxy = get_proxy()
        # 推特登陆需要代理，如果代理为空 退出不执行payload
        if proxy is None:
            result['Payload_msg'] = 'need proxy'
            return result
        # 尝试获取登陆成功的token
        try:
            token = tw_login(twitter_user, twitter_pass, twitter_verify, proxy)
        except Exception as e:
            result['Payload_msg'] = e
            return result
        # 尝试发送推文
        try:
            rest_id = tw_post(token, wallet_address, proxy)
            if rest_id is not None:
                tweeter_url = f"https://twitter.com/{twitter_user}/status/{rest_id}"
                # 得到推文链接 开始领水
                # 处理proxy 格式 得到 ip prot 格式
                # 尝试发送
                try:
                    ws_proxy = proxy['http'].replace("http://", "").strip(":")
                    ws = websocket.WebSocket()
                    ws.connect("wss://l1faucet.a1.taiko.xyz/api",
                               http_proxy_host=f"{ws_proxy[0]}", http_proxy_port=f"{ws_proxy[1]}",
                               proxy_type="http")
                    login_msg = {"url": f"{tweeter_url}", "tier": 0}
                    login_msg_json = json.dumps(login_msg)
                    ws.send(login_msg_json)
                    result['Payload_msg'] = 'Faucet Succeed'
                    result['Succeed'] = True
                except Exception as e:
                    result['Payload_msg'] = e
                    return result
            else:
                result['Payload_msg'] = 'Failed to send a tweet The account may be banned'
                return result
        except Exception as e:
            result['Payload_msg'] = e
            return result
    except Exception as e:
        result['Payload_msg'] = e
        return result


if __name__ == '__main__':
    test = run("0x8dc847af872947ac18d5d63fa646eb65d4d99560")
    print(test['Payload_msg'])
