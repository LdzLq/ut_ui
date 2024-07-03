import re


def is_integer(string):
    """
    判断字符串是否为整数
    :param string: 字符串
    :return: True/False
    """
    pattern = r'^\d+$'

    if re.match(pattern, string):
        return True
    else:
        return False

