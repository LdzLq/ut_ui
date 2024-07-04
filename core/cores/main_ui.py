import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog


class WelcomePage:
    def __init__(self, master):
        self.master = master
        # 定义主窗体的尺寸
        master.title('Unittest自定义测试用例顺序')
        win_width, win_height = master.maxsize()
        master.geometry('750x500' + f'+{win_width // 2 - 375}+{win_height // 2 - 250}')
        master.resizable(width=True, height=True)
        self.frame = ttk.Frame(master)
        self.frame.pack(fill=BOTH, expand=YES)
        self.setup_welcome_ui()

    def setup_welcome_ui(self):
        self.texts = \
            """
        欢迎使用Unittest扩展模块，
        支持自定义测试用例顺序，
        查看用例执行结果！
        """
        ttk.Label(self.frame, text=self.texts, font=('Arial', 20)).pack(side=ttk.TOP, pady=50)
        ttk.Button(self.frame, text='点此进入', command=self.switch_to_main, width=35).pack()

    def switch_to_main(self):
        # 销毁当前的WelcomePage界面
        self.frame.destroy()
        # 初始化并显示MainPage
        MainPage(self.master)


class MainPage:
    def __init__(self, master):
        self.master = master
        self.main_frame = ttk.Frame(master)
        self.main_frame.pack(fill=BOTH, expand=YES)

        self.test_folder_path = ttk.StringVar()
        ttk.Label(self.main_frame, text='选择测试用例目录：', font=('Arial', 15)).place(x=50, y=20)
        ttk.Entry(self.main_frame, textvariable=self.test_folder_path, font=('Roman', 13), width=35, state='readonly').place(x=230, y=25)
        ttk.Button(self.main_frame, text='选择路径', command=self.get_train_path).place(x=580, y=15)

        self.json_folder_path = ttk.StringVar()
        ttk.Label(self.main_frame, text='选择测试数据目录：', font=('Arial', 15)).place(x=50, y=70)
        ttk.Entry(self.main_frame, textvariable=self.json_folder_path, font=('Roman', 13), width=35, state='readonly').place(x=230, y=75)
        ttk.Button(self.main_frame, text='选择路径', command=self.get_test_path).place(x=580, y=65)

        self.csv_folder_path = ttk.StringVar()
        ttk.Label(self.main_frame, text='选择csv文件目录：', font=('Arial', 15)).place(x=40, y=120)
        ttk.Entry(self.main_frame, textvariable=self.csv_folder_path, font=('FangSong', 13), width=35, state='readonly').place(x=230, y=125)
        ttk.Button(self.main_frame, text='选择路径', command=self.weights_save).place(x=580, y=115)

        ttk.Label(self.main_frame, text='测试用执行顺序：', font=('Arial', 15)).place(x=80, y=320)
        self.var = ttk.IntVar()
        ttk.Radiobutton(self.main_frame, text="读取csv加载用例顺序", variable=self.var, value=1).place(x=225, y=320)
        ttk.Radiobutton(self.main_frame, text="自己选择用例顺序", variable=self.var, value=2).place(x=380, y=320)

        ttk.Button(self.main_frame, command=lambda: self.change(
            self.test_folder_path,
            self.json_folder_path,
            self.csv_folder_path,
            self.var
        ), text='开始测试').place(x=220, y=420)

    def get_train_path(self):
        path = filedialog.askdirectory(title='请选择一个目录')
        self.test_folder_path.set(path)

    def get_test_path(self):
        path = filedialog.askdirectory(title='请选择一个目录')
        self.json_folder_path.set(path)

    def weights_save(self):
        path = filedialog.askdirectory(title='请选择一个目录')
        self.csv_folder_path.set(path)


if __name__ == '__main__':
    root = ttk.Window(themename="litera")
    WelcomePage(root)
    root.mainloop()
