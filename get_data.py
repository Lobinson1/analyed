import baostock as bs
import pandas as pd
import datetime
from mysql import connector


def get_daily_info(self):
    connect = connector.connect(host='rm-wz96dr9a71u1pc0wono.mysql.rds.aliyuncs.com',
                                user='junxuchen', passwd='Cjx@123456', db='analyze-python')
    cursor = connect.cursor()
    # 登陆系统\
    lg = bs.login()
    # current_date = '2022-04-15'
    current_date = datetime.date.today().__str__()
    # 显示登陆返回信息
    print('login respond error_code:' + lg.error_code)
    print('login respond  error_msg:' + lg.error_msg)
    # 获取沪深A股历史K线数据 ####
    # 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。“分钟线”不包含指数。
    # 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
    # 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg
    insert_sql = 'INSERT INTO `t_securities_daily`( `securities_id` , `day` , `begin` , `height` , `low` , `end` , ' \
                 '`pre_end` , `turnover_rate` , `is_top` , `is_last` , `turnover` , `turnover_number` , `is_st` , ' \
                 '`percent` , `pe_ttm` ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    cursor.execute("select id,code,market from t_securities where market in ('sh','sz')")
    code_list = cursor.fetchall()
    for code_item in code_list:
        try:
            code = code_item[2] + '.' + code_item[1]
            rs = bs.query_history_k_data_plus(code,
                                              "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,"
                                              "tradestatus,pctChg,isST,peTTM",
                                              start_date='2022-04-14', end_date=current_date,
                                              frequency="d", adjustflag="3")
            print('query_history_k_data_plus respond error_code:' + rs.error_code)
            print('query_history_k_data_plus respond  error_msg:' + rs.error_msg)

            # 打印结果集 ####
            data_list = []
            while (rs.error_code == '0') & rs.next():
                # 获取一条记录，将记录合并在一起
                data_list.append(rs.get_row_data())
            result = pd.DataFrame(data_list, columns=rs.fields)
            if len(data_list) > 0:
                item_list = []
                for index in range(len(result.get('code'))):
                    item = (code_item[0], current_date, result.get('open').values[0],
                            result.get('high').values[0], result.get('low').values[0], result.get('close').values[0],
                            result.get('preclose').values[0], result.get('turn').values[0],
                            result.get('close').values[0] == result.get('high').values[0],
                            result.get('close').values[0] == result.get('low').values[0],
                            result.get('volume').values[0], result.get('amount').values[0],
                            result.get('isST').values[0] == '1', result.get('pctChg').values[0],
                            result.get('peTTM').values[0])
                    item_list.append(item)
                cursor.executemany(insert_sql, item_list)
                print('insert item: ', item_list)
        except BaseException as e:
            print('insert daily info error', e)

    # 登出系统 ####
    bs.logout()


if __name__ == '__main__':
    get_daily_info(None)
