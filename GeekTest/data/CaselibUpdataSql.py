# -*- coding: utf-8 -*-
from data import SqlConnect
from mysql.connector import Error
from data.CaseSql import query_column_single
from log.LogSql import log_input


def query_caselib(username):
    connection = SqlConnect.connect_to_mariadb()
    if connection is None:
        log_input(username, "Error", "数据库连接失败，无法执行查询。")
        return None
    try:
        cursor = connection.cursor()
        caseid_list = (f"select id,title,precondition,pri from zt_case where `lib` = 14 and  `product`=0 and `deleted` = '0'")
        cursor.execute(caseid_list)
        result = cursor.fetchall()
        return result
    except Error as e:
        log_input(username, "Error", f"查询时出错：{e}")
        return None
    finally:
        cursor.close()
        connection.close()

def insert_libproduct(username,product_id,case1):
    connection = SqlConnect.connect_to_mariadb()
    if connection is None:
        log_input(username, "Error", "数据库连接失败")
        return None
    try:
        num = 0
        cursor = connection.cursor()
        account = query_column_single("zt_user", "account", "realname", username)[0]
        cursor.execute("SELECT pp.project FROM zt_projectproduct pp "
                       "join zt_project pro on pp.project=pro.id "
                       "where pp.product = %s and deleted= '0'",
                       (product_id,))
        result = cursor.fetchall()[0]
        project_id = result[0]
        for case in case1:
            num = num + 1
            cursor.execute(
                "INSERT INTO zt_case(product,title,precondition,pri,openedBy,type,stage,zt_case.status,openedDate,version) "
                "VALUES(%s,%s,%s,%s,%s,'feature','system','normal',NOW(),1)",
                (product_id, case[0], case[1], case[2], account))
            cursor.execute('SET @last_id = LAST_INSERT_ID()')
            # 获取最后插入的ID
            cursor.execute("SELECT LAST_INSERT_ID()")
            last_id = cursor.fetchone()[0]
            cursor.execute("INSERT INTO zt_projectcase(project,product,`case`) "
                           "VALUES(%s,%s,%s)",
                           (project_id, product_id, last_id))
            steps = case[3]
            for step in steps:
                cursor.execute(
                    "INSERT INTO zt_casestep(zt_casestep.case,version,type,zt_casestep.desc,expect) "
                    "VALUES (%s,1,'step',%s,%s)",
                    (last_id, step[0], step[1]))
                connection.commit()
    except Error as e:
        data=f"导入用例到用例库时出错：{e}"
        log_input(username, 'Error', data)
        return None
    finally:
        cursor.close()
        connection.close()

def query_casestep(username,caseid):
    connection = SqlConnect.connect_to_mariadb()
    if connection is None:
        log_input(username, "Error", "数据库连接失败，无法执行查询。")
        return None
    try:
        cursor = connection.cursor()
        caseid_list = (f"select zt_casestep.desc,expect from zt_casestep where zt_casestep.case= %s")
        cursor.execute(caseid_list, (caseid,))
        result = cursor.fetchall()
        return result
    except Error as e:
        log_input(username, "Error", f"查询时出错：{e}")
        return None
    finally:
        cursor.close()
        connection.close()