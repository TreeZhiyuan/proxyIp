import ProxyBase
from ProxyBase import KuaiProxy, XiciProxy
from DBPool import PooL

"""
爬取页码
"""
maximum = 3

'''
IP地址 端口 服务器地址 是否匿名 类型 速度 连接时间 存活时间 验证时间
<class 'list'>: ['101.251.216.103', '8080', 'HTTP', '透明', '北京', '66%', '89%', '30天', '18-12-06 13:03']'''


def getXiciIps():
    proxy = XiciProxy(typeproxy=ProxyBase.INTERNAL_HIGHANONYMITY_PROXY)
    proxy.Go(maxPage=maximum)
    xcIpList = proxy.toList()
    print(xcIpList)
    return xcIpList


def getKuaiIps():
    proxy = KuaiProxy(typeproxy=ProxyBase.INTERNAL_HTTP_PROXY)
    proxy.Go(maxPage=maximum)
    xcIpList = proxy.toList()
    print(xcIpList)
    return xcIpList


if __name__ == '__main__':
    xcIps = getXiciIps()
    conn = PooL.connection()
    cursor = conn.cursor()
    for xcIp in xcIps:
        ip = xcIp[0]
        port = xcIp[1]
        region = xcIp[4]
        cursor.execute("select count(*) from xc_proxy_ip where ip=%s", [ip])
        result = cursor.fetchone()
        if result[0] == 0:
            cursor.execute("insert into xc_proxy_ip values (%s,%s,%s)", [ip, port, region])
        else:
            continue
    conn.commit()
    cursor.close()
    pass
