# -*- coding: utf-8 -*-
import sys
import tkinter as tk
from tkinter import messagebox, ttk, PhotoImage
from datetime import datetime
from data.BugAmountSql import query_bugsum
from data.TaskAmountSql import query_tasksum
from log.LogSql import log_input
from login import Login


def statistics_page(parent,username):
    statistics_root = tk.Toplevel(parent)
    statistics_root.title("数据统计")

    # 设置窗口大小和位置
    screen_width = statistics_root.winfo_screenwidth()
    screen_height = statistics_root.winfo_screenheight()
    window_width = 400
    window_height = 350
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))
    statistics_root.geometry(f'{window_width}x{window_height}+{x}+{y}')
    container = tk.Frame(statistics_root)
    container.pack(fill=tk.BOTH, expand=True)

    # 设置窗口背景色
    statistics_root.configure(bg='#343a40')
    # 设置窗口不可改变大小
    statistics_root.resizable(False, False)
    # 设置窗口图标
    icon_path = "picture/xmind.png"
    icon_image = PhotoImage(file=icon_path)
    statistics_root.iconphoto(True, icon_image)

    statistics_root.lift()
    statistics_root.grab_set()
    # 自定义样式
    style = ttk.Style()
    style.configure('Custom.TLabel', background='#f8f9fa', foreground='#212529', font=("微软雅黑", 12, 'bold'))
    # 设置主框架
    main_frame = ttk.Frame(statistics_root)
    main_frame.pack(fill=tk.BOTH, expand=True)
    username_var = tk.StringVar(statistics_root)
    username_frame = tk.Frame(container, bg="white", pady=10)
    username_frame.pack(pady=(20, 0))
    username_label = tk.Label(username_frame, text="查询者:", font=("微软雅黑", 10), bg="white", padx=10)
    username_label.pack(side=tk.LEFT)
    if username=='刘正晗' or username =='罗青':
        username_combobox = ttk.Combobox(username_frame, textvariable=username_var, values=Login.qa_list, width=6,
                                     font=("微软雅黑", 11), state='readonly')
        username_combobox.pack(fill=tk.X, expand=True, padx=(8, 8), pady=0)
        username_combobox.config(justify='center')
        username_combobox.timer_id = None
        username_combobox.event_generate('<Button-1>')

    else:
        username_label=ttk.Label(username_frame, text=username)
        username_label.pack(fill=tk.X, expand=True, padx=(8, 8), pady=0)
        username_var.set(username)

    current_year = datetime.now().year
    recent_years = [current_year+1,current_year, current_year - 1, current_year - 2]
    year_var = tk.StringVar(statistics_root)
    year_var.set(current_year)
    year_frame = tk.Frame(container, bg="white", pady=25)
    year_frame.pack(pady=(20, 0))
    year_label = tk.Label(year_frame, text="年份:", font=("微软雅黑", 10), bg="white", padx=10)
    year_label.pack(side=tk.LEFT)

    year_combobox = ttk.Combobox(year_frame, textvariable=year_var, values=recent_years, width=28,
                                     font=("微软雅黑", 11), state='readonly')
    year_combobox.pack(fill=tk.X, expand=True, padx=(10, 10), pady=0)
    year_combobox.config(justify='center')
    year_combobox.timer_id = None
    year_combobox.event_generate('<Button-1>')

    quarter_var = tk.StringVar(statistics_root)
    quarter_var.set('Q4')
    quarter_frame = tk.Frame(container, bg="white", pady=25)
    quarter_frame.pack(pady=(0, 20))
    quarter_label = tk.Label(quarter_frame, text="季度:", font=("微软雅黑", 10), bg="white", padx=10)
    quarter_label.pack(side=tk.LEFT)

    quarter_combobox = ttk.Combobox(quarter_frame, textvariable=quarter_var, values=['Q1', 'Q2', 'Q3', 'Q4'], width=28,
                                 font=("微软雅黑", 11), state='readonly')
    quarter_combobox.pack(fill=tk.X, expand=True, padx=(10, 10), pady=0)
    quarter_combobox.config(justify='center')
    quarter_combobox.timer_id = None
    quarter_combobox.event_generate('<Button-1>')

    def on_query_button_click():
        querystart(username_var, year_var, quarter_var,username)
    #查询按钮
    query_button_frame = tk.Frame(container, pady=10)
    query_button_frame.pack(pady=(0, 20))
    query_button = tk.Button(query_button_frame, text="开始查询", command=on_query_button_click, font=("微软雅黑", 11),
                            bg="white", fg="black")
    query_button.pack(fill=tk.X, expand=True, padx=20, pady=10)

def querystart(username_var,year_var,quarter_var,username):
    def inner_function():
        tester = username_var.get()
        year = int(year_var.get())
        quarter = quarter_var.get()
        if tester:
            if year and quarter:
                bugsum=query_bugsum(tester,year,quarter)
                tasksum=query_tasksum(tester,year,quarter)
                messagebox.showinfo("查询结果",f"{tester}在{year}年的{quarter}季度,\n"
                                               f"建立BUG总数为：{bugsum},\n"
                                               f"完成任务总数为：{tasksum}")
                log_input(username,"Query",f"查询了{tester}在{year}年的{quarter}季度的bug总数和任务总数")
            else:
                messagebox.showerror('错误',"年份和季度为必填项")
        else:
            messagebox.showerror('错误', "请选择查询人")
    # 调用内部函数以执行查询
    inner_function()