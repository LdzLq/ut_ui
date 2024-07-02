import unittest

from ddt import ddt, data, unpack

from core.utils.read_json import ReadJsoner


battle_data = ReadJsoner().read_json_file(rf'D:/ProgramData/Code/github_projects/ut_ui/core/TestData/Battle.json')


@ddt
class TestBattle(unittest.TestCase):

    @data(battle_data)
    @unpack
    def test_start_battle(self, case_info, d):
        """测试开始战斗

        :param case_info: 一个包含测试数据的字典
        :return:
        """
        # print(case_info)
        print(f"测试开始战斗，案例名称: {case_info['case_name']}")

    def test_skill_buff(self):
        """测试技能buff"""
        print("测试技能buff")

    def test_normal_attack(self):
        """测试普通攻击"""
        print("测试普通攻击")

    def test_get_battle_reward(self):
        """测试领取战斗奖励"""
        print("测试领取战斗奖励")
