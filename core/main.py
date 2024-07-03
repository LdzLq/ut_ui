import unittest

from core.cores.cores import UtUICore


core = UtUICore(rf'D:/Code/github_projects/ut_ui/', rf'core/TestCase/')
suites = core.load_tests(rf'core/config/run_cases.csv')
runner = unittest.TextTestRunner()
runner.run(suites)
