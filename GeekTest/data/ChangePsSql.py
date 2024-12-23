# -*- coding: utf-8 -*-
from data import SqlConnect
from mysql.connector import Error
from log.LogSql import log_input
def update_password(username2,username,password):
    connection = SqlConnect.connect_to_mariadb()
    if connection is None:
        log_input(username,"Error","数据库连接失败")
        return None
    try:
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE `zt_user` SET `password` = %s where `realname` = %s",
            (password,username2))
        log_input(username,'Update',f"修改{username2}的密码成功")
    except Error as e:
        data = f"修改密码时出错：{e}"
        log_input(username, 'Error', data)
        return None
    finally:
        cursor.close()
        connection.close()