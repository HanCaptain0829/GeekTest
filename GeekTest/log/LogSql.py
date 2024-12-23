# -*- coding: utf-8 -*-
from data import SqlConnect
from mysql.connector import Error

def log_input(username,type,data):
    try:
        connection = SqlConnect.connect_to_mariadb()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO testers_inputlog(tester,type,data,time) "
            "VALUES(%s,%s,%s,NOW())",
            (username,type,data))
        connection.commit()
    finally:
        cursor.close()
        connection.close()

def log_query(username):
    try:
        connection = SqlConnect.connect_to_mariadb()
        cursor = connection.cursor()
        if username =='刘正晗' or username=='罗青':
            cursor.execute('Select tester,type,data,time FROM testers_inputlog')
            logdata=cursor.fetchall()
            return logdata
        else:
            cursor.execute('Select tester,type,data,time FROM testers_inputlog WHERE tester = %s',(username,))
            logdata = cursor.fetchall()
            return logdata

    except Error as e:
        data=f'查询日志失败:{e}'
        log_input(username,'Error',data)
        return None

    finally:
        cursor.close()
        connection.close()
