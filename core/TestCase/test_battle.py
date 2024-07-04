import unittest

from ddt import ddt, data, unpack

from core.cores.data_driver import JsonReader


START_BATTLE = JsonReader(rf'D:/Code/github_projects/ut_ui/', rf'core/TestData/StartBattle.json').change_json_content_for_ddt()
SKILL_BUFF = JsonReader(rf'D:/Code/github_projects/ut_ui/', rf'core/TestData/SkillBuff.json').change_json_content_for_ddt()
GET_BATTLE_REWARD = JsonReader(rf'D:/Code/github_projects/ut_ui/', rf'core/TestData/GetBattleReward.json').change_json_content_for_ddt()


@ddt
class TestBattle(unittest.TestCase):

    @data(*START_BATTLE)
    def test_start_battle(self, test_data):
        """测试开始战斗"""
        print(f"测试开始战斗，：{test_data}")

    @data(*SKILL_BUFF)
    def test_skill_buff(self, test_data):
        """测试技能buff"""
        print(f"测试技能buff，：{test_data}")

    @data(*GET_BATTLE_REWARD)
    def test_get_battle_reward(self, test_data):
        """测试领取战斗奖励"""
        print(f"测试领取战斗奖励，：{test_data}")
