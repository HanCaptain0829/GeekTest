# -*- coding: utf-8 -*-
import mysql.connector
from mysql.connector import Error

def connect_to_mariadb():
    """
    连接到MariaDB数据库。

    参数:
    - host_name: 数据库的主机名。
    - port: 数据库的端口号。
    - user_name: 数据库的用户名。
    - user_password: 数据库的密码。
    - db_name: 要连接的数据库名。

    返回:
    - connection: 一个连接到MariaDB的数据库连接对象。
    """
    connection = None
    try:
        connection = mysql.connector.connect(
            host="139.155.28.14",
            port=13306,
            user="root",
            passwd="Aa123456",
            database="zentao"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        data = f"连接到MariaDB时出错：{e}"
    return None


