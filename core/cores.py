import csv
import codecs
import os
import importlib.util
import inspect
import sys
import unittest


def get_test_py_files(folder_path):
    """
    获取指定文件夹下所有以'test'开头且后缀为'.py'的文件名。

    :param folder_path: 字符串，表示目标文件夹的路径。
    :return: 文件名列表，包含符合条件的所有文件名。
    """
    try:
        # 检查路径是否存在
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"路径 {folder_path} 不存在。")

        # 确保给定的是一个目录
        if not os.path.isdir(folder_path):
            raise NotADirectoryError(f"{folder_path} 不是一个目录。")

        # 使用列表推导式筛选出符合条件的文件
        test_py_files = [file for file in os.listdir(folder_path)
                         if file.startswith('test') and file.endswith('.py')]

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


def list_test_classes_and_methods(file_paths):
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

    return class_module_dict, function_class_dict


def load_tests(class_module_map, method_class_map, methods_list):
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
            package_path = os.path.join(os.getcwd(), 'TestCase')
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

    print(suites)

    return suites


def read_test_cases_from_csv(file_path):
    """
    读取CSV文件，每行数据转换为一个列表，如果一行中有多个测试用例名，则作为一个列表存储。

    :param file_path: CSV文件的路径。
    :return: 包含所有行数据的列表，每行数据为一个列表。
    """
    test_cases_list = []  # 存储所有行数据的列表

    try:
        with codecs.open(file_path, mode='r', encoding='utf-8-sig') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                # 这里假设CSV文件中的每一行数据都是用例名，直接将每一行读取并存储为列表
                # 如果一行中包含多个用例名，它们会自然地作为一个列表的元素存在
                test_cases_list.append([item for item in row if item])
    except FileNotFoundError:
        print(f"错误: 文件 {file_path} 未找到。")
    except PermissionError:
        print(f"错误: 没有权限读取文件 {file_path}。")
    except Exception as e:
        print(f"读取文件时发生未知错误: {e}")

    return test_cases_list


if __name__ == '__main__':
    csv_path = rf'D:\ProgramData\Code\github_projects\ut_ui\core\config\run_cases.csv'

    test_case_fld_path = rf'D:\ProgramData\Code\github_projects\ut_ui\core\TestCase'

    case_name_list = read_test_cases_from_csv(csv_path)

    test_case_file_list = get_test_py_files(test_case_fld_path)
    test_case_file_list = [rf'{test_case_fld_path}\{item}' for item in test_case_file_list]

    class_module_dict, function_class_dict = list_test_classes_and_methods(test_case_file_list)

    suite_list = load_tests(class_module_dict, function_class_dict, case_name_list)

    runner = unittest.TextTestRunner()

    runner.run(suite_list)
