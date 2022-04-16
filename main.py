import json
import math
import requests
from mysql import connector

# 通过接口获取券商代码
if __name__ == '__main__':
    connect = connector.connect(host='rm-wz96dr9a71u1pc0wono.mysql.rds.aliyuncs.com',
                                user='junxuchen', passwd='Cjx@123456', db='analyze-python')
    cursor = connect.cursor()
    page_total = math.ceil(4954 / 20)
    index = 1
    while index <= page_total:
        url = 'http://92.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112407958538666454928_1650094040204&' \
              'pn={page}&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,' \
              'm:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,' \
              'f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1650094040205'.format(page=index)
        response = requests.get(url)
        index = index + 1
        data = response.text
        str_test = json.loads(data[data.index('(') + 1:data.rindex(')')])
        data_list = str_test["data"]["diff"]
        for data_item in data_list:
            item = ()
            code = data_item["f12"]
            name = data_item["f14"]
            if code.startswith('60'):
                item = (code, name, "sh")
            elif code.startswith('00'):
                item = (code, name, "sz")
            elif code.startswith('30'):
                item = (code, name, "c")
            elif code.startswith('68'):
                item = (code, name, "k")
            else:
                item = (code, name, "j")
            cursor.execute('insert into `t_securities` (`code`, `name`, `market`) values (%s, %s, %s)', item)
            print('insert item: ', item)
            connect.commit()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
