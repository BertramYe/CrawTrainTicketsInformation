import sqlite3

"""" 以下为操作数据库的行为  """


def save_station_name_infor(data):
    """ 往数据库里面存储信息,如果没有数据库就创建一个sqlit3,并且创建对应的存储表格 """
    drop_table_sql = 'drop table if EXISTS station_name;'
    create_table_sql = 'CREATE TABLE if not EXISTS station_name(chinese_name varchar(20), english_name vachar(10));'
    conn = sqlite3.connect('sqlite3')
    cours = conn.cursor()
    # 删除已存在的表
    cours.execute(drop_table_sql)
    # 重新建表
    cours.execute(create_table_sql)
    # 开始批量插入数据
    for k,v in data.items():
        # 往数据库里面插入数据时最好将数据的左右空格去除
        insert_data_sql = f"insert into station_name(chinese_name,english_name) values('{k.strip()}','{v.strip()}');"
        cours.execute(insert_data_sql)
    cours.execute('commit;')
    cours.close()
    conn.close()

def transfer_station_name(input_station_name,transfer_type):
    """   
    将目标站点的中英文名进行转换,
    其中transfer_type 为 0 表示 将中文站点名转换为英文站点名
                      为 1 表示 将英文站点名转换为中文站点名
    """
    # 清除传入的数据左右的空格
    target_name = input_station_name.strip()
    # 主要是利用数据库，最根本的区别就是执行两个不同的sql语句而已
    sql_list = [f"select english_name from station_name where chinese_name = '{target_name}';",
                f"select chinese_name from station_name where english_name = '{target_name}';"
                ]
    # 默认将返回的目标站点名结果设置为None
    output_station_name = None
    if target_name.__len__() > 0:
        conn = sqlite3.connect('sqlite3')
        cur = conn.cursor()
        results = cur.execute(sql_list[transfer_type]).fetchall()
        cur.close()
        conn.close()
        if results.__len__() > 0:
            # 默认只返回查询到的结果集的第一位
            output_station_name = results[0][0]   
    return output_station_name


# 获取所有的中文名列表，用于用户下拉框的选择出发地和目的地
def get_all_staion_chinese_name():
    result_list = []
    sql = 'select chinese_name from station_name order by chinese_name; '
    conn = sqlite3.connect('sqlite3')
    cours = conn.cursor()
    # 执行查询语句
    results = cours.execute(sql).fetchall()
    # 查询完成后关闭游标和数据库的连接信息
    cours.close()
    conn.close()
    if results.__len__() > 0:
        # 默认得到的列表结果集是列表里面包含元组，所以需要处理一下
        for chinese_station_name_tuple in results:
            chinese_station_name = chinese_station_name_tuple[0]
            result_list.append(chinese_station_name)
    # 最终返回查询的结果列表
    return result_list

         


