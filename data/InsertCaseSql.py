# -*- coding: utf-8 -*-
from data import SqlConnect
from mysql.connector import Error
from data.CaseSql import query_column_single
from log.LogSql import log_input

# 配置日志


def insert_case(username,product_id,testcase):
    connection = SqlConnect.connect_to_mariadb()
    if connection is None:
        log_input(username,"Error","数据库连接失败")
        return None
    try:
        num=0
        cursor = connection.cursor()
        account=query_column_single("zt_user","account","realname",username)[0]
        cursor.execute("SELECT pp.project FROM zt_projectproduct pp "
                       "join zt_project pro on pp.project=pro.id "
                       "where pp.product = %s and deleted= '0'",
                       (product_id,))
        result = cursor.fetchall()[0]
        project_id=result[0]
        for case in testcase:
            num=num+1
            cursor.execute(
                "INSERT INTO zt_case(product,title,precondition,pri,openedBy,type,stage,zt_case.status,openedDate,version) "
                "VALUES(%s,%s,%s,%s,%s,'feature','system','normal',NOW(),1)",
                (product_id,case.get_case_title(),case.get_precondition(),case.get_priority(),account))
            cursor.execute('SET @last_id = LAST_INSERT_ID()')
            # 获取最后插入的ID
            cursor.execute("SELECT LAST_INSERT_ID()")
            last_id = cursor.fetchone()[0]
            cursor.execute("INSERT INTO zt_projectcase(project,product,`case`) "
                           "VALUES(%s,%s,%s)",
                           (project_id,product_id,last_id))

            steps = case.get_case_steps()
            for step in steps:
                cursor.execute(
                    "INSERT INTO zt_casestep(zt_casestep.case,version,type,zt_casestep.desc,expect) "
                    "VALUES (%s,1,'step',%s,%s)",
                    (last_id,step.get_step_value(),step.get_step_result()))
        connection.commit()

    except Error as e:
        data=f"导入用例到项目时出错：{e}"
        log_input(username, 'Error', data)
        return None
    finally:
        cursor.close()
        connection.close()


def insert_caselib(username,lib_id, lib2_id,testcase,title):
    connection = SqlConnect.connect_to_mariadb()
    if connection is None:
        log_input(username,"Error","数据库连接失败")
        return None
    try:
        cursor = connection.cursor()
        account = query_column_single("zt_user", "account", "realname", username)[0]
        for case in testcase:
            if int(case.get_priority())== 1 and case.get_case_title()==title:
                cursor.execute(
                    "INSERT INTO zt_case(lib,module,title,precondition,pri,openedBy,type,stage,status,openedDate,version) "
                    "VALUES(%s,%s,%s,%s,%s,%s,'feature','system','normal',NOW(),1)",
                    (lib_id,lib2_id, case.get_case_title(), case.get_precondition(), case.get_priority(), account))
                cursor.execute('SET @last_id = LAST_INSERT_ID()')
                # 获取最后插入的ID
                cursor.execute("SELECT LAST_INSERT_ID()")
                last_id = cursor.fetchone()[0]
                steps = case.get_case_steps()
                for step in steps:
                    cursor.execute("INSERT INTO zt_casestep(zt_casestep.case,version,type,zt_casestep.desc,expect) "
                                   "VALUES (%s,1,'step',%s,%s)",
                                   (last_id, step.get_step_value(), step.get_step_result()))
        connection.commit()

    except Error as e:
        data=f"导入用例到用例库时出错：{e}"
        log_input(username, 'Error', data)
        return None
    finally:
        cursor.close()
        connection.close()

