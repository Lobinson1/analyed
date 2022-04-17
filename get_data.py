import configparser
import datetime
import logging

import baostock as bs
import pandas as pd
from mysql import connector


def get_daily_info():
    begin_time = datetime.datetime.now()
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_format)
    cp = configparser.ConfigParser()
    cp.read('configuration_local.ini', encoding='UTF-8')
    # cp.read('configuration.ini', encoding='UTF-8')
    mysql_config = dict(cp.items('mysql'))
    connect = connector.connect(host=mysql_config["host"],
                                user=mysql_config["user"],
                                passwd=mysql_config["passwd"],
                                db=mysql_config["db"],
                                port=mysql_config["port"])
    cursor = connect.cursor()
    # 登陆系统
    lg = bs.login()
    current_date = datetime.date.today().__str__()
    # 显示登陆返回信息
    print('login respond error_code:' + lg.error_code)
    print('login respond  error_msg:' + lg.error_msg)
    # 获取沪深A股历史K线数据 ####
    # 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。“分钟线”不包含指数。
    # 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
    # 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg
    insert_sql = 'INSERT INTO `t_securities_daily`( `securities_id` , `day` , `begin` , `high` , `low` , `end` , ' \
                 '`pre_end` , `turnover_rate` , `is_top` , `is_last` , `turnover` , `turnover_number` , `is_st` , ' \
                 '`percent` , `pe_ttm`, `trade_status` ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ' \
                 '%s, %s, %s) '
    cursor.execute("select id,code,market from t_securities where market in ('sh','sz')")
    code_list = cursor.fetchall()
    error_count = 0
    insert_count = 0
    for code_item in code_list:
        try:
            code = code_item[2] + '.' + code_item[1]
            rs = bs.query_history_k_data_plus(code,
                                              "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,"
                                              "tradestatus,pctChg,isST,peTTM",
                                              start_date='2022-01-01', end_date=current_date,
                                              frequency="d", adjustflag="3")
            if rs.error_code != '0':
                print('query_history_k_data_plus respond error_code:' + rs.error_code)
                print('query_history_k_data_plus respond error_msg:' + rs.error_msg)

            # 打印结果集 ####
            data_list = []
            while (rs.error_code == '0') & rs.next():
                # 获取一条记录，将记录合并在一起
                data_list.append(rs.get_row_data())
            result = pd.DataFrame(data_list, columns=rs.fields)
            if len(data_list) > 0:
                item_list = []
                for index in range(len(result.get('code'))):
                    data = {"securities_id": code_item[0],
                            "day": result.get('date').values[index],
                            "begin": result.get('open').values[index],
                            "high": result.get('high').values[index],
                            "low": result.get('low').values[index],
                            "end": result.get('close').values[index],
                            "pre_end": result.get('preclose').values[index],
                            "turnover_rate": result.get('turn').values[index],
                            "is_top": result.get('close').values[index] == result.get('high').values[index],
                            "is_last": result.get('close').values[index] == result.get('low').values[index],
                            "turnover": result.get('volume').values[index],
                            "turnover_number": result.get('amount').values[index],
                            "is_st": result.get('isST').values[index] == '1',
                            "percent": result.get('pctChg').values[index],
                            "pe_ttm": result.get('peTTM').values[index],
                            "trade_status": result.get('tradestatus').values[index] == '1'}
                    item_list.append(build_item(data))
                insert_count += len(item_list)
                cursor.executemany(insert_sql, item_list)
                connect.commit()
                logging.info('insert item: %s', item_list)
        except BaseException as e:
            error_count += 1
            logging.error('insert daily info error %s', e)
            logging.error(e)
    logging.info('insert: %s, error: %s, time: %s', insert_count, error_count, datetime.datetime.now() - begin_time)
    # 登出系统 ####
    bs.logout()


def build_item(data: dict):
    item = (data["securities_id"],
            data["day"],
            data["begin"],
            data["high"],
            data["low"],
            data["end"],
            data["pre_end"],
            0.0 if data["turnover_rate"] == '' else data["turnover_rate"],
            data["is_top"],
            data["is_last"],
            0.0 if data["turnover"] == '' else data["turnover"],
            0.0 if data["turnover_number"] == '' else data["turnover_number"],
            data["is_st"],
            0.0 if data["percent"] == '' else data["percent"],
            data["pe_ttm"],
            data["trade_status"])
    return item


if __name__ == '__main__':
    get_daily_info()
