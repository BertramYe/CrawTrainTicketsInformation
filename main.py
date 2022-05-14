import windows
import crawl_station_name

if __name__ == '__main__':
    # 最好在显示窗口的逻辑执行之前
    # 将站点的英文名数据信息下载完成
    # 为了使得每次加载的车站数据都是最新的，都是每次重新加载里面的数据信息
    get_station_name_or_not = crawl_station_name.get_stations_name()
    # 显示窗口
    if not get_station_name_or_not:
        # 如果车站信息下载失败，那么主窗口不会弹出，反而会有错误的提示框显示出来
        windows.show_windows(False) 
    else:
        #否则显示窗口信息
        windows.show_windows(True)
     