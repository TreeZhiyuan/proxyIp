from DBPool import PooL


# 批量删除已经失效的代理ip地址
def delInvalidIps(iplists):
    conn = PooL.connection()
    cursor = conn.cursor()
    ips = ','.join(iplists)
    sql = "delete from xc_proxy_ip where ip in (%s)"
    cursor.execute(sql, [ips])
    conn.commit()
    cursor.close()
    conn.close()


# 删除已经失效的代理ip地址
def delInvalidIps(ip):
    conn = PooL.connection()
    cursor = conn.cursor()
    sql = "delete from xc_proxy_ip where ip=%s"
    cursor.execute(sql, [ip])
    conn.commit()
    cursor.close()
    conn.close()


# 登录验证
def check(user_name, user_pwd):
    flag = False
    args = (user_name, user_pwd)
    conn = PooL.connection()
    cursor = conn.cursor()
    cursor.execute('select count(*) from zy_account where name=%s and password=%s and status=1', args)
    result = cursor.fetchone()
    if result[0] == 1:
        flag = True
    cursor.close()
    conn.close()
    return flag


# 分页获取代理ip
def fetchByPage(pageNo=0, pageSize=10, searchText=''):
    sql = "select CONCAT(ip, ':', CONVERT(port,char), '@', region) from xc_proxy_ip "
    if searchText == '':
        tail = "limit %s, %s"
        args = (pageNo, pageSize)
    else:
        tail = "where region like %s limit %s, %s"
        args = (("%" + searchText + "%"), pageNo, pageSize)

    sql += tail
    conn = PooL.connection()
    cursor = conn.cursor()
    cursor.execute(sql, args)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    list1 = []
    for (row,) in list(result):
        list1.append(row)
    return list1
