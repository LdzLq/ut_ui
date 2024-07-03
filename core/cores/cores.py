import os
import sys
import inspect
import unittest
import importlib.util

from .tool import is_integer
from .read_data import CSVReader


class UtUICore:

    def __init__(self, project_root_path, test_py_folder_path):
        self.root_path = project_root_path
        self.test_folder_path = test_py_folder_path

    def get_test_py_files(self):
        """
        获取指定文件夹下所有以test开头且后缀为.py的文件名。
        :return: 文件名列表，包含符合条件的所有文件名。
        """
        folder_path = os.path.join(self.root_path, self.test_folder_path)

        try:
            if not os.path.exists(folder_path):
                raise FileNotFoundError(f"路径 {folder_path} 不存在，不是基于 {self.root_path} 的相对路径，请修改！")

            if not os.path.isdir(folder_path):
                raise NotADirectoryError(f"{folder_path} 不是一个目录。")

            # 使用列表推导式筛选出符合条件的文件
            test_py_files = [file for file in os.listdir(folder_path) if str(file).startswith('test') and str(file).endswith('.py')]

            return test_py_files

        except FileNotFoundError as fnf_error:
            print(fnf_error)
            return []
        except NotADirectoryError as nd_error:
            print(nd_error)
            return []
        except PermissionError as perm_error:
            print(f"没有权限访问 {folder_path}: {perm_error}")
            return []
        except Exception as e:
            print(f"发生未知错误: {e}")
            return []

    def list_test_classes_and_methods(self, file_paths):
        """
        遍历提供的.py文件列表，打印出以'Test'开头的类名及其公共方法名。

        :param file_paths: 包含.py文件路径的列表。
        """
        class_module_dict = dict()
        function_class_dict = dict()

        for path in file_paths:
            # 确保文件路径以.py结尾
            if not path.endswith('.py'):
                print(f"警告：{path} 不是.py文件，跳过。")
                continue

            # 获取模块名（不带路径和扩展名）
            module_name = os.path.splitext(os.path.basename(path))[0]

            # 使用importlib.util.spec_from_file_location动态加载模块
            spec = importlib.util.spec_from_file_location(module_name, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # 遍历模块中的定义
            for name, obj in inspect.getmembers(module):
                # 检查是否为类且类名以'Test'开头
                if inspect.isclass(obj) and name.startswith('Test'):
                    class_module_dict[name] = module_name
                    # 获取并打印类的公共方法
                    for method_name, method in inspect.getmembers(obj, predicate=inspect.isfunction):
                        if not method_name.startswith('_') and method_name.startswith('test'):  # 过滤掉私有方法和特殊方法
                            function_class_dict[method_name] = name
        try:
            new_function_class_dict = {}
            for key, value in function_class_dict.items():
                parts = key.strip().split('_')
                last_char = parts[-1]
                if is_integer(last_char):
                    new_key = '_'.join(parts[:-1])
                    new_function_class_dict[new_key] = value
                else:
                    new_function_class_dict[key] = value
            function_class_dict = new_function_class_dict

        except IndexError as e:
            print(f"切割键值存在问题，请检查！：{e}")
            function_class_dict = dict()
        except KeyError as e:
            print(f"键名不可用，请检查：{e}")
            function_class_dict = dict()

        return class_module_dict, function_class_dict

    def add_tests(self, class_module_map, method_class_map, methods_list):
        """
        动态加载测试模块，创建测试用例并添加到测试套件中。

        :param class_module_map: 类名与模块名的字典。
        :param method_class_map: 方法名与类名的字典。
        :param methods_list: 双层列表，内层为多个方法名列表。
        :return: 包含所有测试用例的测试套件列表。
        """
        suites = unittest.TestSuite()  # 用于存储所有测试套件的列表
        loader = unittest.TestLoader()  # 创建测试加载器

        for method_group in methods_list:
            suite = unittest.TestSuite()  # 为每个方法组创建新的测试套件
            for method_name in method_group:
                # 根据方法名找到对应的类名
                if is_integer(method_name.strip().split('_')[-1]):
                    class_name = method_class_map.get('_'.join(method_name.strip().split('_')[0:-1]))
                else:
                    class_name = method_class_map.get(method_name)
                if class_name is None:
                    print(f"警告: 未找到方法 {method_name} 对应的类名，跳过。")
                    continue

                # 根据类名找到对应的模块名
                module_name = class_module_map.get(class_name)
                if module_name is None:
                    print(f"警告: 未找到类 {class_name} 对应的模块名，跳过。")
                    continue

                # 动态导入模块
                package_path = os.path.join(self.root_path, self.test_folder_path)
                if package_path not in sys.path:
                    sys.path.append(package_path)
                module = importlib.import_module(module_name)

                # 获取类并创建测试用例实例
                test_class = getattr(module, class_name, None)
                if test_class is None:
                    print(f"警告: 在模块 {module_name} 中未找到类 {class_name}，跳过。")
                    continue

                # 根据方法名添加测试用例到当前套件
                test_case = loader.loadTestsFromNames([(module_name + '.' + class_name + '.' + method_name)])
                if test_case is not None:
                    suite.addTest(test_case)
                else:
                    print(f"警告: 无法加载测试 {module_name}.{class_name}.{method_name}。")

            if suite._tests:  # 如果该套件中有测试用例，将其添加到总列表中
                suites.addTest(suite)

        return suites

    def load_tests(self, csv_path):
        """动态加载测试用例"""
        test_py_file_list = self.get_test_py_files()

        test_folder_abs_path = os.path.join(self.root_path, self.test_folder_path)

        test_py_file_abs_path_list = []
        for file in test_py_file_list:
            test_py_file_abs_path_list.append(os.path.join(test_folder_abs_path, file))

        class_module_dict, function_class_dict = self.list_test_classes_and_methods(test_py_file_abs_path_list)

        csv_reader = CSVReader(os.path.join(self.root_path, csv_path))
        test_case_name_list = csv_reader.read_test_cases_from_csv()

        test_suites = self.add_tests(class_module_dict, function_class_dict, test_case_name_list)

        return test_suites
