# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox, Menu, PhotoImage

from gui.ChangePasswordPage import change_pswd
from gui.LogPage import log_page
from gui.UserinfoPage import userinfo_page
from gui.testcase.XmindUpdatePage import xmind_module_trigger
from log.LogSql import log_input
from menu import UserOption
from gui.StatisticsPage import statistics_page
from menu.UserOption import fg_color, exitsys, bg_color


def menu_page(parent, username):

    def on_closing():
        menu_root.grab_set()
        try:
            if messagebox.askokcancel("退出", "你确定要退出吗?"):
                log_input(username, 'Exit', f'{username}退出系统')
                parent.destroy()
            else:
                menu_root.grab_release()
        finally:
            pass


    menu_root = tk.Toplevel(parent)
    menu_root.title("GeekTest首页")
    # 设置窗口不可改变大小
    menu_root.resizable(False, False)
    # 设置窗口图标
    icon_path = "picture/xmind.png"
    icon_image = PhotoImage(file=icon_path)
    menu_root.iconphoto(True, icon_image)
    # 关闭按钮直接结束程序
    menu_root.protocol("WM_DELETE_WINDOW", on_closing)

    # 设置窗口大小和位置
    screen_width = menu_root.winfo_screenwidth()
    screen_height = menu_root.winfo_screenheight()
    window_width = 600
    window_height = 440
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))
    menu_root.geometry(f'{window_width}x{window_height}+{x}+{y}')
    container = tk.Frame(menu_root, bg="#f0f0f0", padx=0, pady=0)
    container.pack(fill=tk.BOTH, expand=True)

    # 标题部分
    title_frame = tk.Frame(container, bg="#0c1622", pady=10)
    title_frame.pack(fill=tk.X)
    title_label = tk.Label(title_frame, text="选择需要的功能", font=("微软雅黑", 25, "bold"), fg="white", bg="#0c1622",
                           padx=15)
    title_label.pack(side=tk.LEFT)

    # 添加用户名字展示
    text_label = tk.Label(title_frame, text=f"您好!", font=("微软雅黑", 10), fg="white", bg="#0c1622", padx=5, pady=0)
    text_label.pack(side=tk.RIGHT)

    user_label = tk.Label(title_frame, text=username, font=("微软雅黑", 11, "bold underline"), fg="white", bg="#0c1622",
                          padx=5, cursor="hand2", pady=0)
    user_label.pack(side=tk.RIGHT)
    user_label.bind("<Enter>", lambda event: fg_color(event, "#808080"))
    user_label.bind("<Leave>", lambda event: fg_color(event, "white"))

    def can_change_password(user):
        if  user=='罗青' or user=='刘正晗':
            return True  # 假设当前用户无权限
        else:
            return False

    user_menu = Menu(menu_root, tearoff=0)
    user_menu.add_command(label="个人信息", command=lambda: userinfo_page(parent, username))
    change_password_state = "disabled" if not can_change_password(username) else "normal"
    change_password_command = lambda: change_pswd(parent,username)
    user_menu.add_command(label="修改密码", command=change_password_command, state=change_password_state)
    user_menu.add_command(label="退出登录", command=lambda: UserOption.logout(parent, menu_root, username))

    def show_menu(event):
        try:
            user_menu.tk_popup(event.x_root, event.y_root)
        finally:
            user_menu.grab_release()

    user_label.bind("<Button-1>", show_menu)  # 绑定鼠标点击事件

    #创建模版
    def create_module(parent, module_name, row, column,font_color="black"):
        module_frame = tk.Frame(parent, relief=tk.RAISED, bg='#808080')
        module_frame.grid_propagate(False)
        module_frame.grid(row=row, column=column, sticky="nsew", padx=10, pady=10)

        label = tk.Label(module_frame, text=module_name, font=("微软雅黑", 17, "bold"), anchor="center", bg='#808080',
                         fg=font_color)
        label.pack(expand=True, fill="both", side="top", padx=10, pady=10)
        label.bind("<Button-1>", lambda event: module_frame.event_generate("<Button-1>"))
        label.bind("<Enter>", lambda event: bg_color(event, "#F0F0F0"))
        label.bind("<Leave>", lambda event: bg_color(event, "#808080"))
        return module_frame

    # 在container中添加四个模块
    module_frame_parent = tk.Frame(container, bg='#c0c0c0')
    module_frame_parent.pack(fill=tk.BOTH, expand=True, pady=20)  # 添加一些内边距以避免与标题重叠
    # 使用grid布局来管理模块
    module_frame_parent.grid_columnconfigure(0, weight=1)
    module_frame_parent.grid_columnconfigure(1, weight=1)
    module_frame_parent.grid_rowconfigure(0, weight=1)
    module_frame_parent.grid_rowconfigure(1, weight=1)
    # 创建四个模块
    casemodule = create_module(module_frame_parent, "用 例 上 传", 0, 0)
    mobanmodule = create_module(module_frame_parent, "*数 据 统 计", 0, 1,'red')
    projectmodule = create_module(module_frame_parent, "操 作 日 志", 1, 0)
    exit_sys = create_module(module_frame_parent, "退 出 系 统", 1, 1)

    casemodule.bind("<Button-1>", lambda event: xmind_module_trigger(parent, username))
    mobanmodule.bind("<Button-1>", lambda event: statistics_page(parent,username))
    projectmodule.bind("<Button-1>", lambda event: log_page(parent,username))
    exit_sys.bind("<Button-1>", lambda event: exitsys(username))

    # def open_template_file(username):
    #     file_path = "picture/moban.xmind"  # 请替换为实际文件路径
    #     try:
    #         # 使用subprocess.Popen打开文件
    #         subprocess.Popen(
    #             ['open', file_path] if sys.platform == 'darwin' else ['xdg-open', file_path] if sys.platform.startswith(
    #                 'linux') else ['start', file_path], shell=True)
    #         log_input(username,'Open',f"{username}查看了用例模版")
    #     except Exception as e:
    #         messagebox.showerror('错误',f'模版打开失败:{e}')
    #         log_input(username,'Error',f'模版打开失败:{e}')

