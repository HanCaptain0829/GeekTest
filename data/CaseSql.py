# -*- coding: utf-8 -*-
from data import SqlConnect
from mysql.connector import Error
from log.LogSql import log_input


def query_case(username):
    connection = SqlConnect.connect_to_mariadb()
    if connection is None:
        log_input(username, "Error", "数据库连接失败，无法执行查询。")
        return None
    try:
        cursor = connection.cursor()
        account= query_column_single("zt_user","account","realname",username)
        caseid_list = (f"SELECT c.id,c.title,p.name,c.pri,u.realname,c.openedDate,c.status FROM zt_case c "
                       f"INNER JOIN zt_user u ON c.lastRunner = u.account "
                       f"INNER JOIN zt_product p ON c.product = p.id "
                       f"WHERE openedBy = %s")
        cursor.execute(caseid_list, (account[0],))
        result = cursor.fetchall()
        return result
    except Error as e:
        log_input(username, "Error", f"查询时出错：{e}")
        return None
    finally:
        cursor.close()
        connection.close()


def query_product(username,choose):
    connection = SqlConnect.connect_to_mariadb()
    account = query_column_single("zt_user", "account", "realname", username)
    if choose:
        try:
            cursor = connection.cursor()
            caseid_list = (f"SELECT prod.id, prod.name FROM zt_projectproduct pp "
                           f"JOIN zt_project proj ON pp.project = proj.id JOIN zt_product prod ON pp.product = prod.id " 
                           f"WHERE proj.id in (select project from zt_project where PM=%s and name='项目测试' and status !='closed' and deleted = '0') "
                           f"and prod.deleted ='0' and prod.program !=0 ")
            cursor.execute(caseid_list, (account[0],))
            result = cursor.fetchall()
            return result
        except Error as e:
            log_input(username, "Error", f"查询时出错：{e}")
            return None
        finally:
            cursor.close()
            connection.close()

    else:
        try:
            cursor = connection.cursor()
            caseid_list = (f"SELECT prod.id, prod.name FROM zt_projectproduct pp "
                           f"JOIN zt_project proj ON pp.project = proj.id JOIN zt_product prod ON pp.product = prod.id " 
                           f"WHERE proj.id in (select project from zt_project where name='项目测试' and status !='closed' and deleted ='0') "
                           f"and prod.deleted ='0' and prod.program !=0 ")
            cursor.execute(caseid_list)
            result = cursor.fetchall()
            return result
        except Error as e:
            log_input(username, "Error", f"查询时出错:{e}")
            return None
        finally:
            cursor.close()
            connection.close()

def query_lib():
    connection = SqlConnect.connect_to_mariadb()
    if connection is None:
        log_input('root', "error", "数据库连接失败，无法执行查询")
        return None
    try:
        cursor = connection.cursor()
        lib_list = (f"SELECT id,name FROM zt_testsuite "
                    f"where deleted= '0'")
        cursor.execute(lib_list)
        result = cursor.fetchall()
        return result
    except Error as e:
        log_input('root', "Error", f"查询时出错：{e}")
        return None
    finally:
        cursor.close()
        connection.close()

def query_lib2(lib_id):
    connection = SqlConnect.connect_to_mariadb()
    if connection is None:
        log_input('root', "Error", "数据库连接失败，无法执行查询")
        return None
    try:
        cursor = connection.cursor()
        lib2_list = (f"SELECT id,name FROM zt_module "
                     f"where type='caselib' and  deleted= '0' and root=%s")
        cursor.execute(lib2_list,lib_id)
        result = cursor.fetchall()
        return result
    except Error as e:
        log_input('root', "Error", f"查询时出错:{e}")
        return None
    finally:
        cursor.close()
        connection.close()

#查询单个数据
def query_column_single(table_name, query_column, condition_column, condition_value):
    connection =  SqlConnect.connect_to_mariadb()
    if connection is None:
        log_input('root', "Error", "数据库连接失败，无法执行查询。")
        return None

    try:
        cursor = connection.cursor()
        query = f"SELECT {query_column} FROM {table_name} WHERE {condition_column} = %s"
        cursor.execute(query, (condition_value,))
        result = cursor.fetchall()
        return [row[0] for row in result]  # 提取查询结果中的第一列值
    except Error as e:
        log_input('root', "Error", f"查询时出错：{e}")
        return None
    finally:
        cursor.close()
        connection.close()

#查询多个数据
def query_column_all(table_name, query_column, condition_column, condition_value):
    connection = SqlConnect.connect_to_mariadb()
    if connection is None:
        log_input('root', "Error", "数据库连接失败，无法执行查询。")
        return None

    try:
        cursor = connection.cursor()
        query = f"SELECT {query_column} FROM {table_name} WHERE {condition_column} = %s"
        cursor.execute(query, (condition_value,))
        result = cursor.fetchall()
        return result[0]  # 提取查询结果中的第一列值
    except Error as e:
        log_input('root', "Error", f"查询时出错：{e}")
        return None
    finally:
        cursor.close()
        connection.close()

def delete_case(product_id,username,product_name_val):
    connection = SqlConnect.connect_to_mariadb()
    if connection is None:
        log_input("root", "Error", "数据库连接失败，无法执行查询。")
        return None
    try:
        cursor = connection.cursor()
        update = f"UPDATE zt_case SET deleted = '1' where product = %s"
        cursor.execute(update, (product_id,))
        log_input(username,"Delete",f"{username}删除了项目【{product_name_val}】下的所有用例")
    except Error as e:
        log_input(username, "Error", f"删除用例时出错：{e}")
        return None
    finally:
        cursor.close()
        connection.close()