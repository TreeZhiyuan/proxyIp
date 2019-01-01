"""
[ip,port,region]
"""


def org50Inserts(ips):
    sqls = []
    insert50Str = "insert into xc_proxy_ip values "
    values = [];
    dotSplit = ","
    for ip in ips:
        if values.count() == 50:
            sqls.append(insert50Str)
        values.append("(" + dotSplit.join([ip[0], ip[1], ip[2]]) + ")")

    return insert50Str


print(",".join(["a", "b", "c"]))
