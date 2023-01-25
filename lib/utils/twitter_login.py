"""
@Time ： 2023/1/24 23:21
@Auth ： Web3inFlare
@File ：twitter_login.py
@IDE ：PyCharm
@Motto: 咕咕嘎嘎
"""
from thirdlib.TwitterFrontendFlow.TwitterFrontendFlow import TwitterFrontendFlow

def tw_login(tw_user, tw_password, tw_verify, proxies):
    flow = TwitterFrontendFlow(proxies=proxies)
    flow.login_flow()
    flow.LoginJsInstrumentationSubtask()
    if "LoginEnterUserIdentifierSSO" in flow.get_subtask_ids():
        flow.LoginEnterUserIdentifierSSO(tw_user)
    if "LoginEnterPassword" in flow.get_subtask_ids():
        flow.LoginEnterPassword(tw_password)
    if "AccountDuplicationCheck" in flow.get_subtask_ids():
        flow.AccountDuplicationCheck()
    if "LoginAcid" in flow.get_subtask_ids():
        flow.LoginAcid(tw_verify)
    if "LoginSuccessSubtask" in flow.get_subtask_ids():
        token = flow.SaveCookies()
        return token

