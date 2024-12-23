# -*- coding: utf-8 -*-
import sys
import tkinter as tk
import subprocess
from tkinter import messagebox, ttk
from data.CaseSql import query_product, query_lib2, query_lib, delete_case
from data.InsertCaseSql import insert_case, insert_caselib
from data.TestTaskSql import insert_task
from gui.testcase.TestTaskPage import new_testtask
from log.LogSql import log_input
from menu.LoadCommonTest import load_commonttest
from menu.XmindUploadCase import daoruXmind
import webbrowser


def custom_treeview_style(style):
    # 自定义Treeview的边框样式
    style.element_create("Custom.Treeview.border", "from", "default")
    style.layout("Custom.Treeview", [
        ("Custom.Treeview.border", {'sticky': 'nswe', 'children': [
            ("Treeview.treearea", {'sticky': 'nswe'})
        ]})
    ])

    # 配置边框颜色及粗细（这里通过设置padding和borderwidth来模拟加粗边框）
    style.configure("Custom.Treeview.border", borderwidth=2, relief="solid", bordercolor="black")
    # 配置背景色等其他属性
    style.configure("Custom.Treeview", background="white")


def update_case_count(tree, case_count_label):
    # 获取Treeview中的用例条数
    case_count = len(tree.get_children())
    # 更新标签文本
    case_count_label.config(text=f"未提交一级用例条数: {case_count}")

def UpdatePage(parent, username, testcase, product_id, product_name_val):
    updateroot = tk.Toplevel(parent)
    updateroot.resizable(False, False)
    updateroot.title('上传到哪个用例库？')
    updateroot.iconbitmap("picture/xmind.ico")
    ttk.Style().theme_use('alt')
    style = ttk.Style()

    # 配置 Treeview 样式
    style.configure("Custom.Treeview", rowheight=30, font=('微软雅黑', 8))
    style.configure("Custom.Treeview.Heading", font=('微软雅黑', 11, 'bold'), background='lightblue')
    style.configure("Custom.Treeview", background='white')
    style.map("Custom.Treeview", background=[('selected', 'black')])  # 选中项的背景色

    # 创建Treeview小部件，应用自定义样式
    tree = ttk.Treeview(updateroot, columns=("title", "steps", "expected"),
                        style="Custom.Treeview")

    # 设置标题列
    tree.heading("title", text="用例标题")
    tree.heading("steps", text="步骤")
    tree.heading("expected", text="预期")

    # 配置列宽度
    tree.column("#0", width=0, stretch=False)  # 隐藏默认的层级列
    tree.column("title", width=400, minwidth=400, stretch=False, anchor='w')
    tree.column("steps", width=500, minwidth=500, stretch=False, anchor='w')
    tree.column("expected", width=500, minwidth=500, stretch=False, anchor='w')
    # 填充数据到Treeview

    sorted_testcase = sorted(testcase, key=lambda x: x.get_case_title())
    for case in sorted_testcase:
        if case.get_priority() == "1":
            step = case.get_case_steps()
            if step:
                tree.insert("", tk.END, values=(case.get_case_title(), step[0].get_step_value(),
                                                step[0].get_step_result()))
            else:
                tree.insert("", tk.END, values=(case.get_case_title(), "暂无",
                                                "暂无"))

    # 创建滚动条
    scrollbar = ttk.Scrollbar(updateroot, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    h_scrollbar = ttk.Scrollbar(updateroot, orient=tk.HORIZONTAL, command=tree.xview)
    tree.configure(xscrollcommand=h_scrollbar.set)

    # 将Treeview和滚动条放入主窗口
    tree.grid(row=0, column=0, sticky="nsew", pady=20, padx=20)
    scrollbar.grid(row=0, column=1, sticky="ns")
    h_scrollbar.grid(row=1, column=0, sticky="ew")

    frame = tk.Frame(updateroot)
    frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=20)

    style.configure("TButton", width=15, padding=(5, 0))
    submit_button = ttk.Button(frame, text="提交", style="TButton",
                               command=lambda: lib_choosepage(tree, parent, username, testcase, case_count_label))

    submit_button.grid(row=0, column=0, padx=10)

    close_button = ttk.Button(frame, text="关闭", style="TButton", command=updateroot.destroy)
    close_button.grid(row=0, column=1, padx=10)

    # 添加提示语标签
    hint_label = tk.Label(frame, text="点击用例选中可提交到对应用例库，按住SHIFT或Ctrl可以多选", fg="red",
                          font=("微软雅黑", 13, "bold"))
    hint_label.grid(row=1, column=0, columnspan=2, pady=10)

    # 添加用例条数标签
    font_style = ('微软雅黑', 10)
    font_color = 'blue'  # 字体颜色为红色
    case_count_label = tk.Label(updateroot, text=f"未提交一级用例条数: {len(tree.get_children())}", anchor='se',
                                font=font_style, foreground=font_color)
    case_count_label.grid(row=2, column=0, columnspan=2, sticky="se", pady=20, padx=30)

    # 删除用例函数
    def delete_testcases(tree):
        confirmation = messagebox.askokcancel("确认删除", "您确定要删除项目内所有用例吗？")
        if confirmation:
            for item in tree.get_children():
                tree.delete(item)
            case_count_label.config(text="未提交一级用例条数: 0")
            delete_case(product_id, username, product_name_val)
            close_updateroot(tree)

    delete_button = ttk.Button(frame, text="删除用例", style="TButton", command=lambda: delete_testcases(tree))
    delete_button.grid(row=0, column=2, padx=10, pady=10)
    def close_updateroot(tree):
        if len(tree.get_children())==0:
            updateroot.destroy()

    #跳转禅道函数
    def open_zentao():
        webbrowser.open_new(f"https://zentao.jksxb.cn/testcase-browse-{product_id}.html")

    open_zentao_button = ttk.Button(frame, text="跳转到禅道用例", width=15, command=open_zentao)
    open_zentao_button.grid(row=1, column=2, pady=5, padx=10)  # 调整位置以适应布局

    for i in range(3):  # 更新frame的列配置以适应新布局
        frame.grid_columnconfigure(i, weight=1)
    frame.grid_rowconfigure(0, weight=0)  # 提交、关闭和跳转到禅道按钮
    frame.grid_rowconfigure(1, weight=0)  # 删除用例按钮
    frame.grid_rowconfigure(2, weight=0)  # 保留空行（原用例条数标签位置已调整）

    case_count_label.grid(row=3, column=0, columnspan=2, sticky="se", pady=10, padx=30)
    # 让窗口的各个部分可以响应窗口大小的变化
    updateroot.grid_rowconfigure(0, weight=1)  # Treeview
    updateroot.grid_rowconfigure(1, weight=0)  # frame（包含按钮和标签）
    updateroot.grid_rowconfigure(2, weight=0)  # 用例条数标签
    updateroot.grid_columnconfigure(0, weight=1)

    def lib_choosepage(tree, parent, username, testcase, case_count_label):
        lib_root = tk.Toplevel(parent)
        lib_root.title("Xmind用例上传")
        lib_root.resizable(False, False)
        lib_root.iconbitmap("picture/xmind.ico")

        screen_width = lib_root.winfo_screenwidth()
        screen_height = lib_root.winfo_screenheight()
        window_width = 500
        window_height = 200  # 增加高度以适应按钮
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        lib_root.geometry(f'{window_width}x{window_height}+{x}+{y}')
        container = tk.Frame(lib_root, bg="#f0f0f0", padx=20, pady=20)
        container.pack(fill=tk.BOTH, expand=True)
        check_state = tk.BooleanVar(value=False)

        def update_lib2_options(*args):
            lib_id = get_listid(lib_li, lib_name.get())
            if lib_id is not None:
                lib2_li = query_lib2(lib_id)
                lib2name_list = [i[1] for i in lib2_li]
                lib2name_list.insert(0,"")
                if lib2name_list:
                    combobox_second_level.config(state="readonly")
                    combobox_second_level['values'] = lib2name_list
                    combobox_second_level.current(0)
                else:
                    combobox_second_level.config(state="disabled")
                    combobox_second_level['values'] = []
                    lib2_name.set("")
            else:
                combobox_second_level.config(state="disabled")
                combobox_second_level['values'] = []
                lib2_name.set("")

        lib_li = query_lib()
        libname_list = [i[1] for i in lib_li]
        lib_name = tk.StringVar()
        first_level_label = tk.Label(container, text="选择用例上传的一级用例库：", font=("微软雅黑", 12))
        first_level_label.grid(row=2, column=0, sticky="w", pady=(0, 30))

        combobox_first_level = ttk.Combobox(container, textvariable=lib_name, values=libname_list, state="readonly",
                                            font=("微软雅黑", 10))
        combobox_first_level.grid(row=2, column=1, sticky="ew", padx=(10, 0))
        combobox_first_level.bind("<<ComboboxSelected>>", update_lib2_options)

        lib2_name = tk.StringVar()
        second_level_label = tk.Label(container, text="选择用例上传的二级用例库：", font=("微软雅黑", 12))
        second_level_label.grid(row=3, column=0, sticky="w", pady=(0, 30))

        combobox_second_level = ttk.Combobox(container, textvariable=lib2_name, state="readonly", font=("微软雅黑", 10))
        combobox_second_level.grid(row=3, column=1, sticky="ew", padx=(10, 0))
        combobox_second_level.config(state="disabled")

        style = ttk.Style()
        style.configure('My.TButton', background='lightblue', foreground='black')

        # 添加提交和取消按钮
        def cancel():
            lib_root.destroy()

        submit_button = ttk.Button(container, text="提交",
                                   command=lambda: submit2(tree, username, lib_name, lib2_name,
                                                           testcase, case_count_label))
        submit_button.grid(row=4, column=0, pady=(30, 0), padx=(10, 0), sticky="e")
        cancel_button = ttk.Button(container, text="取消", command=cancel)
        cancel_button.grid(row=4, column=1, pady=(30, 0), padx=(10, 0), sticky="w")

        def submit2(tree, username, lib_name, lib2_name, testcase, case_count_label):
            selected_items = tree.selection()
            num = 0
            for item in selected_items:
                title = tree.item(item)['values'][0]
                lib_name_val = lib_name.get()
                lib2_name_val = lib2_name.get()
                lib_id = get_listid(lib_li, lib_name_val)[0]
                if lib2_name_val:
                    lib2_li = query_lib2([lib_id])
                    lib2_id = get_listid(lib2_li, lib2_name_val)[0]
                    insert_caselib(username, lib_id, lib2_id, testcase, title)
                    num = num + 1
                    tree.delete(item)

                else:
                    insert_caselib(username, lib_id, 0, testcase, title)
                    num = num + 1
                    tree.delete(item)
            messagebox.showinfo("提交成功", "选中的用例已成功提交！")
            if lib2_name.get():
                log_input(username, "Upload",
                          f'{username}上传了{num}条用例到用例库【{lib_name.get()}】下的【{lib2_name.get()}】')
            else:
                log_input(username, "Upload", f'{username}上传了{num}条用例到用例库【{lib_name.get()}】')
            update_case_count(tree, case_count_label)
            lib_root.destroy()
            close_updateroot(tree)


def update_combobox(event, list_of_values):
    input_value = event.widget.get()
    filtered_values = [value for value in list_of_values if input_value.lower() in value.lower()]
    event.widget.config(values=filtered_values)
    event.widget.set(input_value)


def get_listid(list, name):
    for item in list:
        if item[1] == name:
            return [item[0]]
    return None


def open_template_file():
    file_path = "picture/moban.xmind"  # 请替换为实际文件路径
    try:
        # 使用subprocess.Popen打开文件
        subprocess.Popen(
            ['open', file_path] if sys.platform == 'darwin' else ['xdg-open', file_path] if sys.platform.startswith(
                'linux') else ['start', file_path], shell=True)
    except Exception as e:
        print(f"无法打开文件: {e}")


def xmind_module_trigger(parent, username):
    taskdata = []
    testcase = daoruXmind()
    xmind_module_root = tk.Toplevel(parent)
    xmind_module_root.title("上传到哪个项目？")
    xmind_module_root.resizable(False, False)
    xmind_module_root.iconbitmap("picture/xmind.ico")

    screen_width = xmind_module_root.winfo_screenwidth()
    screen_height = xmind_module_root.winfo_screenheight()
    window_width = 400
    window_height = 250  # 增加高度以适应按钮
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))
    xmind_module_root.geometry(f'{window_width}x{window_height}+{x}+{y}')

    container = tk.Frame(xmind_module_root, bg="#f0f0f0", padx=20, pady=20)
    container.pack(fill=tk.BOTH, expand=True)
    check_state = tk.BooleanVar(value=False)

    def update_combobox_options():
        product_list = [i[1] for i in query_product(username, check_state.get())]
        combobox_product['values'] = product_list
        if product_list:
            combobox_product.current(0)

    # 创建变量和控件...

    product_name = tk.StringVar()
    product_list = [i[1] for i in query_product(username, check_state.get())]
    product_label = tk.Label(container, text="选择用例上传的项目：", font=("微软雅黑", 12))
    product_label.grid(row=0, column=0, sticky="w", pady=(0, 10))

    combobox_product = ttk.Combobox(container, textvariable=product_name, values=product_list,
                                    font=("微软雅黑", 10))
    combobox_product.grid(row=0, column=1, sticky="ew", padx=(10, 0))

    check_button = ttk.Checkbutton(container, text="是否只看自己参与的项目？", variable=check_state,
                                   command=update_combobox_options)
    check_button.grid(row=1, column=0, columnspan=2, sticky="w", pady=(10, 0))
    combobox_product.bind('<KeyRelease>', lambda event: update_combobox(event, product_list))
    combobox_product.event_generate('<Button-1>')
    check_state_testtask = tk.BooleanVar(value=False)
    libcase_state = tk.IntVar(value=1)
    libcase_button = ttk.Checkbutton(container, text="是否添加公共用例库用例？", variable=libcase_state)
    libcase_button.grid(row=3, column=0, columnspan=2, sticky="w", pady=(10, 0))


    def update_testtask_button(should_select):
        check_state_testtask.set(should_select)

    def libcase_state_button(should_select):
        libcase_state.set(should_select)

    def testtask_checked(event, parent, taskdata, check_state_testtask):
        if testtask_button.instate(['!selected']):
            check_state_testtask.set(False)
            new_testtask(parent, taskdata, update_testtask_button)

    testtask_button = ttk.Checkbutton(container, text="是否自动生成测试单？", variable=check_state_testtask,
                                      state='normal')
    testtask_button.grid(row=5, column=0, columnspan=2, sticky="w", pady=(10, 0))  # 将其放置在底部
    testtask_button.bind("<Button-1>",
                         lambda event: testtask_checked(event, parent, taskdata, check_state_testtask))

    # 添加提交和取消按钮
    def cancel():
        xmind_module_root.destroy()

    submit_button = ttk.Button(container, text="提交",
                               command=lambda: submit(username, product_name, check_state_testtask,libcase_state))
    submit_button.grid(row=7, column=0, pady=(30, 0), padx=(10, 0), sticky="e")
    cancel_button = ttk.Button(container, text="取消", command=cancel)
    cancel_button.grid(row=7, column=1, pady=(30, 0), padx=(10, 0), sticky="w")

    def submit(username, product_name, check_state_testtask,libcase_state):
        product_name_val = product_name.get()
        if product_name_val:
            product_id = get_listid(query_product(username, False), product_name_val)[0]
            insert_case(username, product_id, testcase)
            log_input(username, 'Upload', f'{username}上传了{len(testcase)}条用例到项目【{product_name_val}】')
            if check_state_testtask.get():
                insert_task(username, product_id, product_name_val, taskdata)
            if libcase_state.get():
                load_commonttest(username,product_id)
                log_input(username, "Upload",f"公共用例库下的全部用例导入到项目【{product_name_val}】")
            messagebox.showinfo("成功", f"成功导入{len(testcase)}个测试用例")
            UpdatePage(parent, username, testcase, product_id, product_name_val)
            xmind_module_root.destroy()
        else:
            messagebox.showerror("错误", f"选项{product_name_val}异常")

