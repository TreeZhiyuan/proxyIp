import pymysql
from DBUtils.PooledDB import PooledDB

dbUrl = "hdm515540417.my3w.com"
dbPasswd = "Xl19870721/"
dbRoot = "hdm515540417"
dbName = "hdm515540417_db"
dbPort = 3306

PooL = PooledDB(
    creator=pymysql,  # 使用链接数据库的模块
    maxconnections=6,  # 连接池允许的最大连接数，0和None表示没有限制
    mincached=2,  # 初始化时，连接池至少创建的空闲的连接，0表示不创建
    maxcached=5,  # 连接池空闲的最多连接数，0和None表示没有限制
    maxshared=3,  # 连接池中最多共享的连接数量，0和None表示全部共享，
    # ps:其实并没有什么用，因为pymsql和MySQLDB等模块中的threadsafety都为1，所有值无论设置多少，_maxcahed永远为0，所以永远是所有链接共享
    blocking=True,  # 链接池中如果没有可用共享连接后，是否阻塞等待，True表示等待，False表示不等待然后报错
    setsession=[],  # 开始会话前执行的命令列表
    ping=0,  # ping Mysql 服务端，检查服务是否可用
    host=dbUrl,
    port=dbPort,
    user=dbRoot,
    password=dbPasswd,
    database=dbName,
    charset='utf8'
)


def funcFetch():
    conn = PooL.connection()
    cursor = conn.cursor()
    cursor.execute('select ip,port,region from xc_proxy_ip')
    result = cursor.fetchall()
    print(result)


def funcInsert():
    conn = PooL.connection()
    cursor = conn.cursor()
    cursor.execute('insert into xc_proxy_ip values(\'12.234.22.32\',\'790\',\'上32322海\')')
    conn.commit()
    cursor.close()
    conn.close()


if __name__ == '__main__':
    funcFetch()

    pass
