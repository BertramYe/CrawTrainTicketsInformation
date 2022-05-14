import requests
import opreation_sqlite3


def filter_train_infor_with_train_type(train_type_checked_or_not_list,all_tickets_info_list):
    """ 
      自定义一个函数用来处理一些被勾选的车次类型
        G    : G-高铁
        D    : D-动车
        Z    : Z-直达
        T    : T-特快
        K    : K-快速
    """
    # # 默认假设是都没勾选的
    # 处理我们需要获取的车次类型的代码，因为不同车次类型的名称就开头都是不一样的
    target_train_type_list = [] 
    for k,v in train_type_checked_or_not_list.items():
        if v:
            target_train_type_list.append(k)
    if target_train_type_list.__len__() != 0:
        # 如果某些车次被勾选，就将原数据被勾选的内容挑出来，放在一个新的数列里面all_tickets_info_list_new，并将其返回
        # 其实还有一种思路，就是将不要的数据从当前的list里面剔除出去
        all_tickets_info_list_new = []
        for item in all_tickets_info_list:
            for target_train_type in target_train_type_list:
                if item[0].startswith(target_train_type.strip()):
                    all_tickets_info_list_new.append(item)
        all_tickets_info_list = all_tickets_info_list_new
        return all_tickets_info_list
    else:
        # 否则的话，不处理原数据，直接进行返回
        return all_tickets_info_list






# 定义一个函数用于加工获取到的车票信息
def format_tickets_infor(tickets_infor_list):
    """ 获取车票信息 """
    """  0:加密信息,1:车票预售时间,2:车次的加密代码(唯一代码),3:车次名称,4:车次的始发站名 5:车次的终点站名  6:我们搭乘的出发地 7:我们到达的目的地
    # 8:车次的出发时间 9:车次的到达时间 10:本次车次历时 21:高级软卧 24:软座  26:无座 28 硬卧 29:硬座 30:二等座 31 一等座 32:商务特等座 33:动卧   """
    # 定义一个空集合用于返回我们的所想要的所有的结果数据
    all_of_ticket_infor_list = []
    # 我们想要的每个车次目标信息的索引列表
    target_infor_index_list = [3,6,7,8,9,10,32,31,30,21,24,33,28,24,29,26]
    for tickets_infor_details in tickets_infor_list:
        # 自定义一个空列表用于返回我们想要的每次车票的详细信息
        target_tickets_infor_list = []
        # 由于每个车次的信息以|隔开，所以按|将信息转化为一个list对象
        tickets_infor_details_list = tickets_infor_details.split('|')
        for target_infor_index in target_infor_index_list:
            # 如果我们想要的位置信息为空我们就用 "--"表示
            if tickets_infor_details_list[target_infor_index] == "":
                tickets_infor_details_list[target_infor_index] = '--'
            # 同时，将英文的站点代码转换中文的
            elif target_infor_index == 6 or target_infor_index == 7:
                tickets_infor_details_list[target_infor_index] = opreation_sqlite3.transfer_station_name(tickets_infor_details_list[target_infor_index],1)
            target_tickets_infor_list.append(tickets_infor_details_list[target_infor_index])
        # 将每个车次处理好的信息存放到一个集合里面
        all_of_ticket_infor_list.append(target_tickets_infor_list)
    # 最终返回信息列表
    return all_of_ticket_infor_list


# 获取车票信息
def get_tickets_infor(from_station,to_station,train_date):
    """ 查询车票信息 """
    """  0:加密信息,1:车票预售时间,2:车次的加密代码(唯一代码),3:车次名称,4:车次的始发站名 5:车次的终点站名  6:我们搭乘的出发地 7:我们到达的目的地
    # 8:车次的出发时间 9:车次的到达时间 10:本次车次历时 21:高级软卧 24:软座  26:无座 28 硬卧 29:硬座 30:二等座 31 一等座 32:商务特等座 33:动卧   """

    # 模仿；浏览器的headers信息，注意此时User-Agent和Cookie这两个参数一个都不能少
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
                'Cookie':"_uab_collina=164960356237596763319356; JSESSIONID=91F0437B5F9987456A0302086E2669EA; BIGipServerotn=1440284938.50210.0000; BIGipServerpassport=988283146.50215.0000; guidesStatus=off; highContrastMode=defaltMode; cursorStatus=off; RAIL_EXPIRATION=1649894349342; RAIL_DEVICEID=MQ0pRFlsGXxSX2Yg6uWHfoM3XcBiSlEv6XBDNw6SZ7AjcNp1J-EHq5nbX-Kn_4gqKPrvzNE1kDsdyS5vyXscCeDNGYfqUojzmhgWACH2AqbY_kLBon2YZHvJItVVzdFtdFB4pC32vWcIAqpyB3LX_9sSaFwc-S62; route=c5c62a339e7744272a54643b3be5bf64; _jc_save_fromStation=%u5408%u80A5%2CHFH; _jc_save_toStation=%u5317%u4EAC%2CBJP; _jc_save_toDate=2022-04-10; _jc_save_wfdc_flag=dc; _jc_save_fromDate=2022-04-14"
              }
    # 拼接查询链接字符串
    url = f'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={train_date}&leftTicketDTO.from_station={from_station}&leftTicketDTO.to_station={to_station}&purpose_codes=ADULT'
    # 利用requests开始爬取信息
    # 以下是模拟了chrome浏览器在爬取信息，因为加入了headers，如果没有headers,由于12306的反扒机制，得到的是乱码
    resp = requests.get(url,verify=True,headers=headers).json()
    # 12306的请求接口返回的是json数据，其中result对应的是一个list对象
    # 其中这个list里面每一条对应一个车次的信息
    tickets_infor_list = resp['data']['result']
    # 取其中的某一条做实验,发现每个车次的信息以|隔开，其中我们按|将信息转化为一个list对象，然后我们得到list对应的索引和对应的信息类型分别为
    # 0：加密信息，1：车票预售时间，2：车次的加密代码（唯一代码），3：车次名称，4：车次的始发站名 5：车次的终点站名  6：我们搭乘的出发地 7：我们到达的目的地
    # 8：车次的出发时间 9：车次的到达时间 10：本次车次历时 21：高级软卧 24：软座 26:无座 28 硬卧 29:硬座 30：二等座 31 一等座 32：商务特等座 33：动卧 
    # 故而整理一下，我们想要的信息分别为第 3，6，7，8，9，10，32，31，30，21，24，33，28，24，29，26 位的信息，假设如果这些位置的信息为空我们就用 "--"表示，
    # 从而完成我们所有信息的处理和获取
    all_of_ticket_infor_list = format_tickets_infor(tickets_infor_list)
    
    return all_of_ticket_infor_list
    



