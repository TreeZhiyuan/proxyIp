import ProxyBase
from ProxyBase import KuaiProxy, XiciProxy

"""
爬取页码
"""
maximum = 1

'''
IP地址 端口 服务器地址 是否匿名 类型 速度 连接时间 存活时间 验证时间
<class 'list'>: ['101.251.216.103', '8080', 'HTTP', '透明', '北京', '66%', '89%', '30天', '18-12-06 13:03']'''


def getXiciIps():
    proxy = XiciProxy(typeproxy=ProxyBase.INTERNAL_HTTP_PROXY)
    proxy.Go(maxPage=maximum)
    xcIpList = proxy.toList()
    for item in xcIpList:
        print(item)


if __name__ == '__main__':
    getXiciIps()

    pass
