# -*- coding: utf-8 -*-
from collections import Counter
import easygui
import jsonpath
import sys
import urllib3
import xmindparser
from typing import List
from tkinter import messagebox
from urllib3.connectionpool import InsecureRequestWarning

urllib3.disable_warnings(InsecureRequestWarning)
xmindparser.config = {
    'logName': __name__,
    'logLevel': None,
    'logFormat': '%(asctime)s %(levelname)-8s: %(message)s',
    'showTopicId': False,
    'hideEmptyValue': False
}


class TestCase:
    def __init__(self, case_title, case_steps, priority, precondition):
        self._case_title = case_title
        self._case_steps = case_steps
        self._priority = priority
        self._precondition = precondition

        # Getters

    def get_case_title(self):
        return self._case_title

    def get_case_steps(self):
        return self._case_steps

    def get_priority(self):
        return self._priority

    def get_precondition(self):
        return self._precondition

class TestCaseStep:
    def __init__(self, step_num, step_value, step_result):
        self._step_num = step_num
        self._step_value = step_value
        self._step_result = step_result

        # Getters

    def get_step_num(self):
        return self._step_num

    def get_step_value(self):
        return self._step_value

    def get_step_result(self):
        return self._step_result

class TestSuite:

    module_tags = "flag-red"

    def __init__(self):
        self.xmind_data = None
        self.get_xmind()
        self.get_product_info()

    def get_xmind(self):
        path = easygui.fileopenbox("请选择要导入的xmind文件", filetypes=["*.xmind"])
        #校验上传格式是否为.xmind
        if path is None:
            pass
        if not path.endswith('.xmind'):
            messagebox.showerror('错误','不是哥们儿,你搁这儿传啥文件呢?')

        self.xmind_data = xmindparser.xmind_to_dict(path)[0]
        self.modules = jsonpath.jsonpath(self.xmind_data, f'$..topics[?(@.makers && "{TestSuite.module_tags}" in @.makers)]')


    def get_product_info(self):
        product_names = jsonpath.jsonpath(self.xmind_data, '$.topic.title')
        if product_names:
            pass
        else:
            messagebox.showerror("错误",f"项目名称为空：{product_names}")

    @staticmethod
    def verify_case_topic(case_topic):
        makers = jsonpath.jsonpath(case_topic, '$..makers')
        if TestSuite.module_tags in str(makers):
            return False
        else:
            return True

    def get_case(self, case_topic: dict, module_name: str):
        case_title = f"【{module_name}】{case_topic.get('title', '未命名测试用例')}"
        makers = case_topic.get('makers', [])
        precondition = case_topic.get('note', '')
        if not precondition:
            precondition = "暂无"
        if makers:
            priority = makers[0][-1]
        else:
            priority = "3"
        case_steps = []
        case_step_topics = case_topic.get("topics", [])
        if case_step_topics:
            step_num = 1
            for case_step_topic in case_step_topics:
                step_value = case_step_topic.get('title', '')
                case_result_topics = case_step_topic.get("topics", [])
                if case_result_topics:
                    case_result = "||".join(jsonpath.jsonpath(case_result_topics, f'$..title'))
                else:
                    case_result = "暂无"
                case_step = TestCaseStep(step_num, step_value, case_result)
                case_steps.append(case_step)
                step_num += 1
        return TestCase(case_title, case_steps, priority, precondition)

    def get_cases(self) -> List[TestCase]:
        test_cases = []
        for module in self.modules:
            modules_name = module.get("title", None)
            # print(f"模块名：{modules_name}")
            if modules_name is None:
                messagebox.showerror("错误",f"部分模块名为空")
                sys.exit(0)
            else:
                module_name = modules_name
            case_topics = module.get("topics", [])
            if not case_topics:
                continue
            for case_topic in case_topics:
                if TestSuite.verify_case_topic(case_topic):
                    test_case = self.get_case(case_topic, module_name)
                    test_cases.append(test_case)
        return test_cases


def verify_case(fn):
    def inner_import_case(self, test_cases: List[TestCase]):
        case_titles = [x.case_title for x in test_cases]
        case_title_dict = Counter(case_titles)
        err_case = {x: y for x, y in case_title_dict.items() if y > 1}
        if err_case:
            messagebox.showerror('导入失败',f"含有重复的测试用例名称：{err_case},请检查后再导入")
        else:
            fn(self, test_cases)
    return inner_import_case


# 假设的TestCaseManager类，有一个需要导入测试用例的方法
class TestCaseManager:
    def __init__(self):
        self.test_cases = []

        # 使用verify_case装饰器来验证测试用例

    def import_case(self, test_cases):
        self.test_cases.extend(test_cases)

    # 主函数

def daoruXmind() -> List[TestCase]:
    test_suite = TestSuite()
    test_cases = test_suite.get_cases()
    test_case_manager = TestCaseManager()
    test_case_manager.import_case(test_cases)
    return test_case_manager.test_cases
