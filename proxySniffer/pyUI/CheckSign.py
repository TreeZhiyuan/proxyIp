from DBPool import PooL


def check(user_name, user_pwd):
    flag = False
    args = (user_name, user_pwd)
    conn = PooL.connection()
    cursor = conn.cursor()
    cursor.execute('select count(*) from zy_account where name=%s and password=%s', args)
    result = cursor.fetchone()
    if result[0] == 1:
        flag = True
    conn.close()
    return flag

def fetchAllProxyIps():
    conn = PooL.connection()
    cursor = conn.cursor()
    cursor.execute('select ip,port,region from xc_proxy_ip')
    proxyIps = cursor.fetchall()
    conn.close()
    return proxyIps
