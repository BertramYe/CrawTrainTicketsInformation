# 本文件用来定义一些自定义的错误类型，和一些常见的错误处理方法
from PyQt5.QtWidgets import QMessageBox
import opreation_sqlite3

# 自定义的一些错误类型和错误代码
ERROR_CODE = {
    401:'站点不存在！',
    402:'输入的值为空值！',
    403:'输入的日期值早于当前时间！',
    404:'查询不到车票信息！',
    405:'车站信息下载失败,请重启软件后再尝试！',
    406:'车票信息查询出错！'
}


# 根据错误类型显示错误信息
def show_error_message(messg_title,message_code,plus_error_message=''):
    """ 
    根据错误类型显示错误信息,
    plus_error_message表示额外的需要补充的错误信息,选填,默认为空字符串
    """
    message_box = QMessageBox()
    for error_code,error_message in ERROR_CODE.items():
        if error_code == message_code:
            message_box.setWindowTitle(messg_title)
            message_box.setText(error_message + plus_error_message )
            message_box.exec_()


# 检查输入的站点是否有误
def check_and_transfer_input_station(station_chinese,error_title):
    """ 检查输入的站点信息是否有误,并输入转换的站点信息的英文代码 """
    # 输入的站点值不能为空值
    if station_chinese.strip().__len__() == 0:
        # 如果为空，打印错误信息
        show_error_message(error_title,402)
        return False
    else:
        # 否则查询战点是否在数据库中存在
        station_englist = opreation_sqlite3.transfer_station_name(station_chinese,0)
        # 如果不存在，显示错误信息
        if station_englist == None:
           show_error_message(error_title,401)
           return False
        else:
            return station_englist


# 检查输入的时间是否有误
def check_and_transfer_train_date(train_date,error_title):
    """ 比较需要查询的时间，其中当前时间可通过 train_date 自带的 currentDateTime() 方法进行获取，
        并且 train_date 和 current_date 同为date类型,可以直接相互比较,但是为了让用户能查到当天的数据，
        current_date 需要比train_date先获取到,因为比较时，会有时分秒的比较，导致当天数据无法查询
        """
    current_date = train_date.currentDateTime()
    # train_date.toString('yyyy-MM-dd') == current_date.toString('yyyy-MM-dd') 等价于只比较到当天
    # 是为了确保能查到当天时间的车票，因为我发现每次当前时间比默认的train_date总是晚几秒钟，导致无法查询当天的车票信息
    # 如果需要查询的车票信息时间早于当前时间，表示车票已经过期，就会有报错提示，车票查询只能查未来的车票
    if train_date > current_date or train_date.toString('yyyy-MM-dd') == current_date.toString('yyyy-MM-dd') :
        # 否则将日期格式化，并返回我们想要的日期结果
        train_date = train_date.toString('yyyy-MM-dd')
        return train_date
    else:
        show_error_message(error_title,403)
        return False
        

       
    