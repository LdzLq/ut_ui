import csv
import codecs
import json
import os.path


class CSVDriver:

    def __init__(self, csv_path):
        self.csv_path = csv_path

    def read_test_cases_from_csv(self):
        """读取CSV文件，每行数据转换为一个列表，如果一行中有多个测试用例名，则作为一个列表存储。"""
        test_cases_list = []

        with codecs.open(self.csv_path, mode='r', encoding='utf-8-sig') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                test_cases_list.append([item for item in row if item])

        return test_cases_list

    def write_test_result_from_csv(self, test_result_list):
        """将测试结果写入csv文件中"""
        with open(self.csv_path, mode='w', newline='', encoding='utf-8-sig') as csvfile:
            csv_writer = csv.writer(csvfile)
            for row in test_result_list:
                csv_writer.writerow(row)


class JsonDriver:

    def __init__(self, json_path):
        self.json_path = json_path
        self.is_folder = os.path.isdir(json_path)

    def _read_single_json_file(self, file_path):
        """读取单个json文件内容"""
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if isinstance(data, dict):
            return data
        else:
            raise TypeError(f"路径为：{file_path}的json文件，内容格式不正确，请检查并修改！")

    def read_json_contents(self):
        """读取json文件或文件夹内容，返回内容列表"""
        if self.is_folder:
            content = []
            for root, dirs, files in os.walk(self.json_path):
                for file in files:
                    if str(file).endswith('.json'):
                        file_path = os.path.join(root, file)
                        content.append(self._read_single_json_file(file_path))
            return content
        else:
            return [self._read_single_json_file(self.json_path)]

    def change_json_content_for_ddt(self):
        """将json内容，修改成合适ddt使用的类型"""
        json_content = []

        contents = self.read_json_contents()
        if contents:
            for content in contents:
                for value in content.values():
                    json_content.append(value)

        return json_content

    def get_json_file_key_list(self):
        """获取json文件的键list"""
        keys, key_list = [], []

        contents = self.read_json_contents()
        for content in contents:
            if isinstance(content, dict):
                keys.append(list(content.keys()))

        for key in keys:
            for case in key:
                key_list.append(case)

        return key_list
