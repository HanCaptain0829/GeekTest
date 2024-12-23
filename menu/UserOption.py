# -*- coding: utf-8 -*-
import sys
from tkinter import messagebox
from data.CaseSql import query_column_all
from log.LogSql import log_input


# 登出功能的逻辑，登录页面退出隐藏，当前页面关闭
def logout(parent, menu_root,username):
    if messagebox.askokcancel("切换登录", "确定要切换登录账号吗？"):
        menu_root.destroy()
        parent.deiconify()
        log_input(username,'Exit',f'{username}登出系统,切换账号')

# 用于修改背景颜色
def bg_color(event, color):
    event.widget.config(bg=color)

# 用于修改字体颜色
def fg_color(event, color):
    event.widget.config(fg=color)

# 下拉框输入联想功能
def update_combobox(event, list_of_values):
    input_value = event.widget.get()
    filtered_values = [value for value in list_of_values if input_value.lower() in value.lower()]
    event.widget.config(values=filtered_values)
    event.widget.set(input_value)

#查询个人信息
def user_info(username):
    user_info_list=query_column_all("zt_user","realname,account,visits,ip",
                                "realname",username)
    return user_info_list

def exitsys(username):
    if messagebox.askokcancel("退出系统", "确定要退出系统吗？"):
        log_input(username,'Exit',f"{username}退出系统")
        sys.exit()
