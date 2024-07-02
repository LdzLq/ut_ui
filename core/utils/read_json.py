import json


class ReadJsoner:

    @staticmethod
    def read_json_file(json_path):
        return json.load(open(json_path, 'r', encoding='utf-8'))
