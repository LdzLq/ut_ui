# import unittest
#
# from core.cores.test_loader import TestLoader
#
#
# csv_path = rf'D:/Code/github_projects/ut_ui/core/config/run_cases.csv'
# suites = TestLoader(rf'D:/Code/github_projects/ut_ui/core/TestCase/').load_tests(csv_path)
# runner = unittest.TextTestRunner()
# runner.run(suites)

from core.cores.main_ui import WelcomePage
import ttkbootstrap as ttk


root = ttk.Window(themename="litera")
WelcomePage(root)
root.mainloop()
