# -*- coding: utf-8 -*-
import hashlib
import tkinter as tk
from tkinter import messagebox,PhotoImage

from data.ChangePsSql import update_password
from tkinter import ttk
from PIL import Image, ImageTk
from login import Login
from menu.UserOption import bg_color, update_combobox



# 下拉框输入联想功能
def update_combobox(event, list_of_values):
    input_value = event.widget.get()
    filtered_values = [value for value in list_of_values if input_value.lower() in value.lower()]
    event.widget.config(values=filtered_values)
    event.widget.set(input_value)


def change_pswd(parent,username):
    password_root = tk.Toplevel(parent)
    password_root.title("修改密码")
    # 设置窗口不可改变大小
    password_root.resizable(False, False)
    # 设置窗口图标

    icon_path = "picture/xmind.png"
    icon_image = PhotoImage(file=icon_path)
    password_root.iconphoto(True, icon_image)

    # 设置窗口大小和位置
    screen_width = password_root.winfo_screenwidth()
    screen_height = password_root.winfo_screenheight()
    window_width = 500
    window_height = 250
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))
    password_root.geometry(f'{window_width}x{window_height}+{x}+{y}')

    container = tk.Frame(password_root, bg="#f0f0f0", padx=0, pady=0)
    container.pack(fill=tk.BOTH, expand=True)

    # 账号选择
    username_var = tk.StringVar(password_root)
    username_var.set(username)
    username_frame = tk.Frame(container, bg="white", pady=5)
    username_frame.pack(pady=(40, 0))
    username_label = tk.Label(username_frame, text="要修改的用户:", font=("微软雅黑", 12), bg="white", padx=16)
    username_label.pack(side=tk.LEFT)

    username_combobox = ttk.Combobox(username_frame, textvariable=username_var, values=Login.qa_list, width=28,
                                     font=("微软雅黑", 12), state='readonly')
    username_combobox.pack(fill=tk.X, expand=True, padx=(10, 10), pady=0)
    username_combobox.config(justify='center')
    username_combobox.timer_id = None
    username_combobox.bind('<KeyRelease>', lambda event: update_combobox(event, Login.qa_list))
    username_combobox.event_generate('<Button-1>')

    #修改密码部分
    # 密码输入部分
    password_frame = tk.Frame(container, bg="white", pady=15)
    password_frame.pack(pady=0)
    password_label = tk.Label(password_frame, text="修改后的密码:", font=("微软雅黑", 12), bg="white", padx=1)
    password_label.grid(row=0, column=0, sticky=tk.W, padx=(16, 12))
    password_entry = tk.Entry(password_frame, show="*", width=24, font=("微软雅黑", 14), bd=2, relief='groove')
    password_entry.grid(row=0, column=1, sticky=tk.W + tk.E, padx=(14, 14), pady=2)

    # 加载图片
    def load_resized_image(image_path, size):
        original_image = Image.open(image_path)
        resized_image = original_image.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(resized_image)

    show_password_var = tk.BooleanVar(value=False)
    show_image = load_resized_image("picture/zhanshi.png", (24, 24))
    hide_image = load_resized_image("picture/yingcang.png", (24, 24))
    # 使用图片创建按钮
    show_password_button = tk.Button(password_frame, image=show_image,
                                     command=lambda: toggle_password(password_entry, show_password_button,
                                                                     show_password_var, show_image, hide_image))
    show_password_button.grid(row=0, column=1, sticky=tk.E, padx=(0, 10))

    # 修改toggle_password函数以处理图片切换
    def toggle_password(entry, button, var, show_image, hide_image):
        if var.get():
            entry.config(show="")
            button.config(image=hide_image)
        else:
            entry.config(show="*")
            button.config(image=show_image)
        var.set(not var.get())

    # 提交按钮
    submit_button = tk.Button(container, text="确认修改", font=("微软雅黑", 13), bg="#222222", fg="#ffffff", padx=10,
                              pady=4)
    submit_button.pack(pady=30)
    submit_button.bind("<Enter>", lambda event: bg_color(event, "#808080"))
    submit_button.bind("<Leave>", lambda event: bg_color(event, "#222222"))
    submit_button.config(command=lambda: submit_credentials(username_var, password_entry))

    # 为根窗口绑定回车键事件
    def on_return_key(event):
        if password_entry == password_entry.focus_get():  # 检查焦点是否在密码输入框上
            submit_button.invoke()  # 触发提交按钮的点击事件

    password_root.bind("<Return>", on_return_key)  # 绑定回车键事件

    # 点击登录后的处理
    def submit_credentials(username_var, password_entry):
        def my_md5(data: str):
            md5 = hashlib.md5()
            md5.update(data.encode("utf-8"))
            return md5.hexdigest()

        username2 = username_var.get()
        password = password_entry.get()

        if Login.login_verify(username2, password) == 1:
            messagebox.showerror("错误", "密码不能为空！")
        elif Login.login_verify(username2, password) == 0:
            messagebox.showerror("错误", f"密码不能和旧密码相同")
        else:
            update_password(username2, username, my_md5(password))
            password_root.destroy()
            messagebox.showinfo("成功", f"{username2}的密码修改成功")
