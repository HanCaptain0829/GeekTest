# -*- coding: utf-8 -*-
from data import SqlConnect
from mysql.connector import Error
from data.CaseSql import query_column_single
from log.LogSql import log_input


def insert_task(username,product_id,product_name_val,taskdata):
    connection = SqlConnect.connect_to_mariadb()
    if connection is None:
        log_input(username,"Error","数据库连接失败")
        return None
    try:
        cursor = connection.cursor()
        #准备数据:创建者,项目id,参与者,开始时间,结束时间
        account=query_column_single("zt_user","account","realname",username)[0]

        cursor.execute("select pp.project from zt_projectproduct pp join zt_project proj on pp.project=proj.id where pp.product=%s and proj.deleted = '0'",
                       (product_id,))
        projectid = cursor.fetchall()[0][0]
        participantlist=[]
        for i in taskdata[1]:
            canyu = query_column_single("zt_user", "account", "realname", i)
            participantlist.append(canyu[0])
        participant = ','.join(participantlist)
        start_time=taskdata[2]
        end_time=taskdata[3]

        #准备数据:负责人,测试单名称,执行阶段
        owner = query_column_single("zt_user", "account", "realname", taskdata[0])[0]
        name=product_name_val+"冒烟测试"
        cursor.execute("select id from zt_project "
                       "where project = %s and name ='冒烟测试'",
                       (projectid,))
        execution = cursor.fetchall()
        if execution!=[]:
            execution_id=execution[0][0]
        else:
            cursor.execute("select id from zt_project where project = %s and name ='项目测试'", (projectid,))
            execution_id=cursor.fetchall()[0][0]

        #插入数据
        cursor.execute("INSERT INTO zt_testtask(project,product,name,execution,type,owner,pri,begin,end,status,createdBy,createdDate,members)"
                        "VALUES(%s,%s,%s,%s,'system',%s,3,%s,%s,'wait',%s,NOW(),%s)",
                        (projectid,product_id,name,execution_id,owner,start_time,end_time,account,participant))
        log_input(username,'Create',f'{username}创建了测试单【{name}】')

    except Error as e:
        data=f'创建测试单失败:{e}'
        log_input(username,'Error',data)
        return None

    try:
        num=0
        # 获取最后插入的ID
        cursor.execute('SET @last_id = LAST_INSERT_ID()')
        cursor.execute("SELECT LAST_INSERT_ID()")
        lastd_id = cursor.fetchone()[0]

        cursor.execute("select id from zt_case "
                       "where `product` = %s and pri =1 and deleted ='0'",
                       (product_id,))
        caseid_list=cursor.fetchall()
        for i in caseid_list:
            cursor.execute("INSERT INTO zt_testrun(task,`case`,version,status)"
                           "VALUES(%s,%s,1,'normal')",
                           (lastd_id,i[0]))
            num=num+1
        log_input(username, 'Upload', f'测试单【{name}】关联了{num}条用例')
    except Error as e:
        data=f'测试单关联测试用例失败:{e}'
        log_input(username,'Error',data)
        return None

    finally:
        cursor.close()
        connection.close()

def query_people():
    connection = SqlConnect.connect_to_mariadb()
    if connection is None:
        return None
    try:
        cursor = connection.cursor()
        people_list = (f"select realname from zt_user "
                       f"where role in ('dev','td') and deleted = '0'")
        cursor.execute(people_list)
        result = []
        resultt = cursor.fetchall()
        for i in resultt:
            result.append(i[0])
        return result
    except Error as e:
        return None
    finally:
        cursor.close()
        connection.close()

