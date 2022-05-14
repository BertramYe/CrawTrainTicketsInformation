import re
import requests
import opreation_sqlite3


def get_stations_name():
    """ 获取所有的车站英文名以及对应的缩写,并将数据存储在sqlite数据库里面 """
    # 获取车站英文缩写名称的接口地址
    url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9229'
    resp = requests.get(url,verify=True)
    # 利用正则获取目标站点信息
    stations = re.findall('[\u4e00-\u9fa5]+\|[A-Z]+',resp.text)
    stations_name_diction = {}
    for i in stations:
        item = i.split('|')
        ky = item[0].strip()
        vl = item[1].strip()
        stations_name_diction.update({ky:vl})
    # 其实在这一步已经拿到了我们想要车站信息的格式，而且已经转换成了字典，很方便我们进行查找和使用
    # 当然你一可以不用字典返回数据，也可以将当前数据存到一个文本文件或者一个小型的数据库，比如sqlite,都可以
    # print(stations_name_diction)
    if stations_name_diction.__len__() > 0:
        opreation_sqlite3.save_station_name_infor(stations_name_diction)
        # 如果存储完成返回True
        return True
    else:
        # 否则表示车站名称并未获取得到
        return False
    




