# coding:utf-8
import datetime, time, calendar


def ts2time(ts):
    timeArray = time.localtime(ts)
    return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    # time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def get_time():
    return ('-').join(ts2time(time.time()).split(' '))


def months(dt, months):   # 这里的months 参数传入的是正数表示往后 ，负数表示往前
    month = dt.month - 1 + months
    year = dt.year + month / 12
    month = month % 12 + 1
    day = min(dt.day, calendar.monthrange(year, month)[1])
    dt = dt.replace(year=year, month=month, day=day)

    return str(dt.replace(year=year, month=month, day=day)).replace('-', '')

if __name__ == '__main__':
    time_temp = '20170228'
    dt = datetime.date(int(time_temp[0:4]), int(time_temp[4:6]), int(time_temp[6:8]))
    print '一个月前的今天是', months(dt, -1)
    print '6个月前的今天是', months(dt, -6)
