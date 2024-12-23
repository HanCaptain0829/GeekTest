# -*- coding: utf-8 -*-
from data import SqlConnect
from mysql.connector import Error
from data.CaseSql import query_column_single
from log.LogSql import log_input
from datetime import datetime

def query_bugsum(username,year,quarter):
    #根据季度筛选完成起始时间和完成截止时间
    if quarter == 'Q1':
        startTime = datetime(year, 1, 15, 00, 00, 0)
        endTime = datetime(year, 4, 14, 23, 59, 59)
    elif quarter == 'Q2':
        startTime = datetime(year, 4, 15, 00, 00, 0)
        endTime = datetime(year, 7, 14, 23, 59, 59)
    elif quarter == 'Q3':
        startTime = datetime(year, 7, 15, 00, 00, 0)
        endTime = datetime(year, 10, 14, 23, 59, 59)
    elif quarter == 'Q4':
        startTime = datetime(year, 10, 15, 00, 00, 0)
        endTime = datetime(year+1, 1, 14, 23, 59, 59)
    else:
        log_input(username, "Error", "无效的季度参数")
        return None

    connection = SqlConnect.connect_to_mariadb()
    if connection is None:
        log_input(username, "Error", "数据库连接失败")
        return None
    try:
        cursor = connection.cursor()
        account = query_column_single("zt_user", "account", "realname", username)[0]
        cursor.execute("SELECT count(id) FROM `zentao`.`zt_bug`"
                        "WHERE `openedBy` = %s AND `deleted` = '0'"
	                    "AND `openedDate` >= %s"
	                    "AND `openedDate` <= %s",
                        (account,startTime,endTime))
        result= cursor.fetchall()[0][0]
        return result
    except Error as e:
        data=f"查询{year}年{quarter}季度BUG数量异常：{e}"
        log_input(username, 'Error', data)
        return None
    finally:
        cursor.close()
        connection.close()
