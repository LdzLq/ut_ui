import unittest

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox

from core.cores.test_loader import TestLoader


class WelcomePage:
    def __init__(self, master):
        self.master = master
        self.set_window()  # 设置主窗体尺寸
        self.frame = self.setup_welcome_ui()  # 设置欢迎页面

    def set_window(self):
        """定义主窗体的尺寸"""
        self.master.title('Unittest自定义测试用例顺序')
        win_width, win_height = self.master.maxsize()
        self.master.geometry('750x500' + f'+{win_width // 2 - 375}+{win_height // 2 - 250}')
        self.master.resizable(width=True, height=True)

    def setup_welcome_ui(self):
        """设置欢迎页面"""
        frame = ttk.Frame(self.master)
        frame.pack(fill=BOTH, expand=YES)
        texts = \
            """
        欢迎使用Unittest扩展模块，
        支持自定义测试用例顺序，
        查看用例执行结果！
        """
        ttk.Label(frame, text=texts, font=('Arial', 20)).pack(side=ttk.TOP, pady=50)
        ttk.Button(frame, text='点此进入', command=self.switch_to_main, width=35).pack()
        return frame

    def switch_to_main(self):
        """销毁欢迎页面，加载主页面"""
        self.frame.destroy()
        MainPage(self.master)


class MainPage:
    def __init__(self, master):
        self.master = master
        self.main_frame = ttk.Frame(master)
        self.main_frame.pack(fill=BOTH, expand=YES)

        self.test_folder_path = ttk.StringVar()
        ttk.Label(self.main_frame, text='选择测试用例目录：', font=('Arial', 15)).place(x=50, y=20)
        ttk.Entry(self.main_frame, textvariable=self.test_folder_path, font=('Roman', 13), width=35, state='readonly').place(x=230, y=20)
        ttk.Button(self.main_frame, text='选择路径', command=self.get_train_path).place(x=580, y=20)

        self.json_folder_path = ttk.StringVar()
        ttk.Label(self.main_frame, text='选择测试数据目录：', font=('Arial', 15)).place(x=50, y=70)
        ttk.Entry(self.main_frame, textvariable=self.json_folder_path, font=('Roman', 13), width=35, state='readonly').place(x=230, y=70)
        ttk.Button(self.main_frame, text='选择路径', command=self.get_test_path).place(x=580, y=70)

        self.csv_folder_path = ttk.StringVar()
        ttk.Label(self.main_frame, text='选择csv文件目录：', font=('Arial', 15)).place(x=50, y=120)
        ttk.Entry(self.main_frame, textvariable=self.csv_folder_path, font=('Roman', 13), width=35, state='readonly').place(x=230, y=120)
        ttk.Button(self.main_frame, text='选择路径', command=self.weights_save).place(x=580, y=120)

        ttk.Label(self.main_frame, text='测试用执行顺序：', font=('Arial', 15)).place(x=50, y=170)
        self.var = ttk.IntVar()
        ttk.Radiobutton(self.main_frame, text="读取csv加载用例顺序", variable=self.var, value=1).place(x=230, y=178)
        ttk.Radiobutton(self.main_frame, text="自己选择用例顺序", variable=self.var, value=0).place(x=380, y=178)

        ttk.Button(self.main_frame, command=lambda: self.change(
            self.test_folder_path,
            self.json_folder_path,
            self.csv_folder_path,
            self.var
        ), text='开始测试', width=35).place(x=230, y=250)

    def get_train_path(self):
        path = filedialog.askdirectory(title='请选择一个目录')
        self.test_folder_path.set(path)

    def get_test_path(self):
        path = filedialog.askdirectory(title='请选择一个目录')
        self.json_folder_path.set(path)

    def weights_save(self):
        path = filedialog.askopenfilename(title='请选择一个csv文件')
        self.csv_folder_path.set(path)

    def change(self, test_folder_path, json_folder_path, csv_folder_path, driver_flag):
        if driver_flag.get() == 0:
            messagebox.showerror(title='出错了', message='该模式尚未完成，请选择csv载入！')
        else:
            test_py_folder_path = test_folder_path.get()
            csv_folder_path = csv_folder_path.get()
            suites = TestLoader(test_py_folder_path).load_tests(csv_folder_path)
            runner = unittest.TextTestRunner()
            runner.run(suites)
            messagebox.showinfo(title='测试结果', message='测试完成，请在IDEA中查看测试结果！')


if __name__ == '__main__':
    root = ttk.Window(themename="litera")
    WelcomePage(root)
    root.mainloop()
