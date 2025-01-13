# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk,PhotoImage
from menu.UserOption import user_info

def userinfo_page(parent,username):
    userinfo_root = tk.Toplevel(parent)
    userinfo_root.title(username+"个人信息")

    # 设置窗口大小和位置
    screen_width = userinfo_root.winfo_screenwidth()
    screen_height = userinfo_root.winfo_screenheight()
    window_width = 400
    window_height = 300
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))
    userinfo_root.geometry(f'{window_width}x{window_height}+{x}+{y}')
    container = tk.Frame(userinfo_root)
    container.pack(fill=tk.BOTH, expand=True)

    # 设置窗口背景色
    userinfo_root.configure(bg='#343a40')

    # 设置窗口不可改变大小
    userinfo_root.resizable(False, False)
    # 设置窗口图标
    icon_path = "picture/xmind.png"
    icon_image = PhotoImage(file=icon_path)
    userinfo_root.iconphoto(True, icon_image)

    userinfo_root.lift()
    userinfo_root.grab_set()

    # 自定义样式
    style = ttk.Style()
    style.configure('Custom.TLabel', background='#f8f9fa', foreground='#212529',font=("微软雅黑", 12, 'bold'))

    # 设置主框架
    main_frame = ttk.Frame(userinfo_root, padding=20)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # 使用Grid布局管理器
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=3)

    # 定义一个生成器来跟踪行索引
    def row_generator():
        i = 0
        while True:
            yield i
            i += 1

    row_iter = row_generator()

    # 定义展示数据的函数
    def display_info(label_text, value):
        row = next(row_iter)
        label = ttk.Label(main_frame, text=label_text, style='Custom.TLabel')
        label.grid(row=row, column=0, sticky='e', padx=(0, 10), pady=(10, 0))
        value_label = ttk.Label(main_frame, text=value, background='#e9ecef', foreground='#495057', font=("微软雅黑", 12))
        value_label.grid(row=row, column=1, sticky='w', padx=(0, 20), pady=(10, 0))


    # 展示数据
    user_list=user_info(username)

    display_info("姓名:", user_list[0])
    display_info("用户名:", user_list[1])

    # 添加分隔符
    ttk.Separator(main_frame, orient='horizontal').grid(row=next(row_iter), columnspan=2, sticky='ew', pady=10)
    display_info("部门:", "测试组")
    display_info("职位:", "测试")
    # 再次添加分隔符
    ttk.Separator(main_frame, orient='horizontal').grid(row=next(row_iter), columnspan=2, sticky='ew', pady=10)
    display_info("禅道访问次数:", user_list[2])
    display_info("IP地址:", user_list[3])

