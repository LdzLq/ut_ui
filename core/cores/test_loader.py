import os
import sys
import inspect
import unittest
import importlib.util

from .data_driver import CSVDriver


class TestLoader:

    def __init__(self, test_folder_absolute_path):
        self.test_folder_path = test_folder_absolute_path

    def __get_test_py_files_path(self):
        """获取测试用例文件夹内所有测试文件的路径"""
        if not os.path.exists(self.test_folder_path):
            raise FileNotFoundError(f"路径 {self.test_folder_path} 不存在，请传入绝对路径！")
        if not os.path.isdir(self.test_folder_path):
            raise NotADirectoryError(f"{self.test_folder_path} 不是一个目录。")

        test_py_absolute_path_list = []
        for folder_path, dirs, files in os.walk(self.test_folder_path):
            for file in files:
                if str(file).startswith('test') and str(file).endswith('.py'):
                    test_py_absolute_path_list.append(os.path.join(folder_path, file))

        return test_py_absolute_path_list

    def __load_test_py_module(self):
        """加载测试用例执行文件模块"""
        test_py_absolute_path_list = self.__get_test_py_files_path()

        module_dict = dict()
        for path in test_py_absolute_path_list:
            if not path.endswith('.py'):
                print(f"警告：{path} 不是.py文件，跳过。")
                continue

            module_name = os.path.splitext(os.path.basename(path))[0]

            spec = importlib.util.spec_from_file_location(module_name, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            module_dict[module_name] = module

        return module_dict

    def __list_test_classes_and_methods(self):
        """遍历提供的.py文件列表，打印出以'Test'开头的类名及其公共方法名"""
        class_module_dict = function_class_dict = dict()

        module_dict = self.__load_test_py_module()
        for module_name, module in module_dict.items():
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and name.startswith('Test'):
                    class_module_dict[name] = module_name
                    for method_name, method in inspect.getmembers(obj, predicate=inspect.isfunction):
                        if not method_name.startswith('_') and method_name.startswith('test'):
                            function_class_dict[method_name] = name

        return class_module_dict, function_class_dict

    def __add_tests(self, case_name_lists):
        """动态加载测试模块，创建测试用例并添加到测试套件中"""
        suites = unittest.TestSuite()
        loader = unittest.TestLoader()

        class_module_dict, function_class_dict = self.__list_test_classes_and_methods()

        for case_name_list in case_name_lists:
            suite = unittest.TestSuite()
            for case_name in case_name_list:
                class_name = function_class_dict.get(case_name)
                if class_name is None:
                    print(f"警告: 未找到方法 {case_name} 对应的类名，跳过。")
                    continue

                module_name = class_module_dict.get(class_name)
                if module_name is None:
                    print(f"警告: 未找到类 {class_name} 对应的模块名，跳过。")
                    continue

                if self.test_folder_path not in sys.path:
                    sys.path.append(self.test_folder_path)
                module = importlib.import_module(module_name)

                test_class = getattr(module, class_name, None)
                if test_class is None:
                    print(f"警告: 在模块 {module_name} 中未找到类 {class_name}，跳过。")
                    continue

                test_case = loader.loadTestsFromNames([(module_name + '.' + class_name + '.' + case_name)])
                if test_case is not None:
                    suite.addTest(test_case)
                else:
                    print(f"警告: 无法加载测试 {module_name}.{class_name}.{case_name}。")

            if suite._tests:
                suites.addTest(suite)

        return suites

    def get_test_case_names(self):
        """用例不存在json测试数据时，测试方法名即为测试用例名"""
        class_module_dict, function_class_dict = self.__list_test_classes_and_methods()

        return list(function_class_dict.keys())

    def load_tests(self, csv_file_absolute_path):
        """动态加载测试用例"""
        test_case_lists = CSVDriver(csv_file_absolute_path).read_test_cases_from_csv()

        if not test_case_lists:
            test_case_lists = self.get_test_case_names()

        test_suites = self.__add_tests(test_case_lists)

        return test_suites
