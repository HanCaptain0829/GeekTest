# -*- coding: utf-8 -*-
import sys
import tkinter as tk
from tkinter import messagebox, ttk, PhotoImage
from itertools import islice
from log.LogSql import log_query



def log_page(parent,username):
    log_root = tk.Toplevel(parent)
    log_root.title('操作日志')
    width=1300
    height=770
    icon_path="picture/xmind.png"
    icon_image = PhotoImage(file=icon_path)
    log_root.iconphoto(True, icon_image)

    # 设置 Treeview 样式
    ttk.Style().theme_use('alt')
    log_root.geometry('1300x770')
    # 获取屏幕宽度和高度
    screen_width = log_root.winfo_screenwidth()
    screen_height = log_root.winfo_screenheight()

    # 计算窗口应该出现的位置
    x = int((screen_width - width) / 2)
    y = int((screen_height - height) / 2)

    # 设置窗口的位置和大小
    log_root.geometry(f'{width}x{height}+{x}+{y}')
    style = ttk.Style()
    # 设置字体大小（这里设置为12，可以根据需要调整）
    style.configure('Treeview', font=('微软雅黑', 11))
    # 设置表头字体加粗和背景色（这里设置为灰色）
    style.configure('Treeview.Heading', font=('微软雅黑', 13, 'bold'), background='gray')
    tree = ttk.Treeview(log_root, columns=('operator', 'type', 'content', 'time'), show='headings', style='Treeview')
    # 禁用滚动条
    tree.configure(yscrollcommand=lambda: None, xscrollcommand=lambda: None)
    # 设置表头
    tree.heading('operator', text='操作人')
    tree.heading('type', text='类型')
    tree.heading('content', text='内容')
    tree.heading('time', text='时间')

    # 调整列宽（可选）
    tree.column('operator', width=100)
    tree.column('type', width=100)
    tree.column('content', width=800)
    tree.column('time', width=200)
    # 放置Treeview控件在窗口中
    tree.pack(fill=tk.Y, expand=True, pady=30, padx=30)
    log_list = log_query(username)
    # 原始数据备份，用于排序
    old_log_data = log_list[:]
    # 分页相关变量
    rows_per_page = 30  # 每页显示的行数
    current_page = 1  # 当前页码
    total_pages = len(log_list) // rows_per_page + (1 if len(log_list) % rows_per_page else 0)  # 总页数
    sort_column = None
    sort_ascending = None

    # 更新表格数据的函数
    def update_tree(event=None):
        # 清空当前表格内容
        for item in tree.get_children():
            tree.delete(item)

            # 根据筛选条件筛选数据
        start = (current_page - 1) * rows_per_page
        end = start + rows_per_page

        # 添加数据到表格中
        for row in islice(log_list, start, end):
            dt = row[3]
            # 检查日期是否为 None
            if dt is not None:
                formatted_dt = dt.strftime('%Y-%m-%d %H:%M:%S')
            else:
                # 处理日期为 None 的情况，这里使用空字符串作为示例
                formatted_dt = "日期未知"
            tree.insert('', tk.END, values=(row[0], row[1], row[2], formatted_dt))
        page_label.config(text=f"{current_page}/{total_pages}")

    def go_to_page(new_page):
        nonlocal current_page
        if 1 <= new_page <= total_pages:
            current_page = new_page
            update_tree()

    def sort_by_column(column_name):
        nonlocal sort_column, sort_ascending,log_list
        if column_name=='time':
            sort_ascending = not sort_ascending if sort_column == column_name else True
            sort_column = column_name
            # 使用lambda函数和itemgetter进行排序，这里假设log_list中的时间数据是datetime对象
            log_list.sort(key=lambda x: x[3], reverse=not sort_ascending)
            if sort_ascending:
                tree.heading('time', text='时间 △')
            else:
                tree.heading('time', text='时间 ▽')
                # 更新数据显示
            update_tree()
        else:
            pass

    def copy_to_clipboard(event=None):
        try:
            item = tree.selection()[0]  # 获取选中的第一项
            values = tree.item(item, "values")  # 获取该项的值
            # 将所有值连接成一个字符串，这里使用制表符作为分隔符
            text_to_copy = "\t".join(values)
            # 将文本复制到剪贴板
            log_root.clipboard_clear()
            log_root.clipboard_append(text_to_copy)
            # 可选：显示一个消息表示复制成功
            messagebox.showinfo("复制成功", "文本已复制到剪贴板")
        except IndexError:
            # 如果没有选中任何项，则显示错误消息
            messagebox.showerror("错误", "请选中一行进行复制")

            # 在树视图控件中绑定鼠标右键事件（或你可以选择其他事件，如键盘事件）

    tree.bind("<Button-3>", copy_to_clipboard)
    # 也可以绑定到键盘事件，例如 Ctrl+C
    tree.bind("<Control-c>", copy_to_clipboard)

    # 放置Treeview控件在窗口中
    tree.pack(fill=tk.BOTH, expand=True, pady=30, padx=30)

    # 为Treeview添加右键菜单（可选）
    menu = tk.Menu(log_root, tearoff=0)
    menu.add_command(label="复制", command=copy_to_clipboard)

    # 显示右键菜单
    def show_context_menu(event):
        try:
            tree.selection()[0]  # 检查是否有选中项
            menu.post(event.x_root, event.y_root)
        except IndexError:
            pass  # 如果没有选中项，则不显示菜单

    tree.bind("<Button-3>", show_context_menu)  # 绑定右键事件到显示菜单的函数

    for col in ('operator', 'type', 'content', 'time'):
        tree.heading(col, command=lambda c=col: sort_by_column(c))

    frame = tk.Frame(log_root)
    frame.pack(pady=10)

    total_records_label = tk.Label(frame, text=f"记录总计: {len(log_list)} 条")
    total_records_label.pack(side=tk.LEFT)

    prev_button = tk.Button(frame, text='上一页',padx=20, pady=10,
                            command=lambda: go_to_page(current_page - 1) if current_page > 1 else None)
    prev_button.pack(side=tk.LEFT)
    next_button = tk.Button(frame, text='下一页',padx=20, pady=10,
                            command=lambda: go_to_page(current_page + 1) if current_page < total_pages else None)
    next_button.pack(side=tk.RIGHT)
    page_label = tk.Label(frame, text=f"{current_page}/{total_pages}")

    page_label.pack(side=tk.RIGHT, padx=(20, 20))  # 在右侧显示，与按钮保持一定距离
    prev_button.pack(side=tk.LEFT, padx=(20, 0))
    page_label.pack(side=tk.LEFT, padx=(20, 20))  # 将 page_label 放在中间
    next_button.pack(side=tk.RIGHT, padx=(0, 20))
    total_records_label.pack(side=tk.RIGHT, padx=(20, 0))

    # 初始化表格数据
    update_tree()
