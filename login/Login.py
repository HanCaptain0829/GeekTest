# -*- coding: utf-8 -*-
import hashlib
from data.CaseSql import query_column_single
from log.LogSql import log_input


# 数据库获得qa的人员名单
qa_list = query_column_single("zt_user", "realname", "role", "qa")

#核对密码
def login_verify(username, input_password):
    #查询数据库内对应密码
    try:
        password=query_column_single("zt_user", "password", "realname", username)[0]
        if not input_password:
            return 1
        #判断密码是否相等
        elif (my_md5(input_password)==password) or input_password==password:
            return 0
        else:
            return 2
    except Exception as e:
        data=f'登录信息验证失败:{e}'
        log_input(username, 'Error', data)

#加密密码
def my_md5(data: str):
    md5 = hashlib.md5()
    md5.update(data.encode("utf-8"))
    return md5.hexdigest()

