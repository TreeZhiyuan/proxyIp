import random
import requests

IPAgents = [
    "61.176.223.7:58822",
]


def isValidTelnet():
    # -*- coding: utf-8 -*-
    import telnetlib

    print('------------------------connect---------------------------')
    # 连接Telnet服务器
    try:
        tn = telnetlib.Telnet('	121.61.0.127', port='9999', timeout=20)
    except:
        print('该代理IP  无效')
    else:
        print('该代理IP  有效')

    print('-------------------------end----------------------------')


def isProxyIpValid():
    isValid = False
    try:
        requests.adapters.DEFAULT_RETRIES = 3
        IP = random.choice(IPAgents)
        thisProxy = "https://" + IP
        thisIP = "".join(IP.split(":")[0:1])
        head = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
            'Connection': 'keep-alive'}
        print(thisIP)
        res = requests.get(url="http://icanhazip.com/", headers=head, timeout=10, proxies={"HTTPS": thisProxy})
        print(res.text)
        proxyIP = res.text
        if proxyIP == thisProxy:
            print("代理IP:'" + proxyIP + "'有效！")
            isValid = True
        else:
            print("代理IP无效！")
    except:
        print("代理IP无效！")
    return isValid


isValidTelnet()

