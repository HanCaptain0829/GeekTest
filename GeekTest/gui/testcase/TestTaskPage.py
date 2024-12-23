# -*- coding: utf-8 -*-
from tkinter import ttk, messagebox
import tkinter as tk
from tkcalendar import DateEntry
from data.TestTaskSql import query_people
import ctypes


def new_testtask(parent,taskdata,update_testtask_button):
    testtask_root = tk.Toplevel(parent)
    testtask_root.resizable(False, False)
    testtask_root.iconbitmap("picture/xmind.ico")
    testtask_root.title('测试单配置')
    # 设置testtask_root在最上层且锁定操作
    testtask_root.lift()
    testtask_root.grab_set()


        # 窗口大小和位置设置
    screen_width = testtask_root.winfo_screenwidth()
    screen_height = testtask_root.winfo_screenheight()
    window_width = 300
    window_height = 550
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))
    testtask_root.geometry(f'{window_width}x{window_height}+{x}+{y}')

    container = tk.Frame(testtask_root, bg="#f0f0f0", padx=20, pady=20)
    container.pack(fill=tk.BOTH, expand=True)
    # 添加负责人下拉框
    label_responsible = tk.Label(container, text="负责人:")
    label_responsible.pack(anchor=tk.W)
    responsible_var = tk.StringVar()
    responsible_combobox = ttk.Combobox(container, textvariable=responsible_var, values=query_people(),font=('微软雅黑',11))
    responsible_combobox.pack(anchor=tk.W)

    # 添加参与人多选下拉框
    # 创建并配置标签
    label_participant = ttk.Label(container, text="参与人:")
    label_participant.pack(anchor=tk.W)
    # 创建StringVar来存储选中的参与人
    selected_participants=[]
    listbox_height = 11  # 可见的行数
    # 创建Listbox作为多选下拉框
    participant_listbox = tk.Listbox(container, selectmode=tk.MULTIPLE, exportselection=0,height=listbox_height, font=('微软雅黑',11))
    participant_listbox.pack(anchor=tk.W)
    # 填充Listbox
    for person in query_people():
        participant_listbox.insert(tk.END, person)
        # 定义一个函数来更新选中的参与人
    def update_selected_participants(event=None):  # 注意：这里添加了event参数，但它在绑定时可以是None
        selected_indices = participant_listbox.curselection()
        # 更新选中参与人列表
        selected_participants.clear()  # 清空列表
        selected_participants.extend([participant_listbox.get(idx) for idx in selected_indices])
    participant_listbox.bind('<<ListboxSelect>>', update_selected_participants)
    # 添加开始时间选择框
    label_start_time = tk.Label(container, text="开始时间:")
    label_start_time.pack(anchor=tk.W)
    start_time_var = tk.StringVar()  # 添加一个StringVar来存储格式化后的日期
    start_time_combobox = DateEntry(container, width=12, background='darkblue',
                                    foreground='white', selectmode='day', date_pattern="yyyy-MM-dd")
    start_time_combobox.pack(anchor=tk.W)
    # 绑定一个函数到<<DateSelected>>事件
    start_time_combobox.bind("<<DateSelected>>", lambda e: update_date_display(start_time_var, start_time_combobox))

    # 添加一个标签来显示格式化后的日期
    start_time_label = tk.Label(container, textvariable=start_time_var)
    start_time_label.pack(anchor=tk.W)

    # 添加结束时间选择框
    label_end_time = tk.Label(container, text="结束时间:")
    label_end_time.pack(anchor=tk.W)
    end_time_var = tk.StringVar()  # 添加一个StringVar来存储格式化后的日期
    end_time_combobox = DateEntry(container, width=12, background='darkblue',
                                    foreground='white', selectmode='day', date_pattern="yyyy-MM-dd")
    end_time_combobox.pack(anchor=tk.W)
    # 绑定一个函数到<<DateSelected>>事件
    end_time_combobox.bind("<<DateSelected>>", lambda e: update_date_display(end_time_var, end_time_combobox))
    # 添加一个标签来显示格式化后的日期
    end_time_label = tk.Label(container, textvariable=end_time_var)
    end_time_label.pack(anchor=tk.W)

    def update_date_display(var, date_entry):
        date = date_entry.get_date()
        if date:
            formatted_date = date.strftime("%Y-%m-%d")
            var.set(formatted_date)
        else:
            var.set("")
    # 添加确定按钮
    def on_confirm(taskdata,update_testtask_button):
        responsible = responsible_var.get()
        if responsible:
            participant = selected_participants
            start_time = start_time_combobox.get_date()  # 获取日期对象
            if start_time:
                end_time = end_time_combobox.get_date()
                if end_time:# 获取日期对象
                    taskdata.clear()
                    start_time_str = start_time.strftime("%Y-%m-%d") if start_time else None
                    end_time_str = end_time.strftime("%Y-%m-%d") if end_time else None
                    # 这里 start_time 和 end_time 已经是 datetime.date 类型或者 None
                    taskdata.append(responsible)
                    taskdata.append(participant)
                    taskdata.append(start_time_str)
                    taskdata.append(end_time_str)
                    should_select =True
                    update_testtask_button(should_select)
                    testtask_root.destroy()

                else:
                    messagebox.showerror('错误', '请添加测试单结束时间')
            else:
                messagebox.showerror('错误', '请添加测试单开始时间')
        else:
            messagebox.showerror('错误', '请添加测试单负责人')
    confirm_button = tk.Button(container, text="确定", command=lambda: on_confirm(taskdata,update_testtask_button),font=('微软雅黑',12))
    confirm_button.pack(side=tk.BOTTOM, pady=10)


