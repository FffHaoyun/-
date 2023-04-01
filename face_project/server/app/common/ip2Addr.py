# -*- coding: utf-8 -*-
import os
from app.common.ip2Region import Ip2Region

#定义一个IP转化地址的函数

def ip2addr(ip):
    ip_db_path = os.path.join(
        #IP地址库的路径
        os.path.dirname(
            os.path.dirname(__file__)
        ),
        'static/ip2region/ip2region.db'
    )
    # 实例化
    ip_to_addr = Ip2Region(ip_db_path)
    #地址信息
    addr_info = ip_to_addr.memorySearch(ip)
    return addr_info

if __name__ == '__main__':
    addr1 = ip2addr('115.239.211.112')
    print(
        addr1
    )
    print(
        "城市ID：{}，地址信息：{}".format(
            addr1['city_id'],
            addr1['region'].decode('utf-8')
        )
    )