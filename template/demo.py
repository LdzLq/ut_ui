import threading
import tkinter
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

import dataset
from train import BeginTrain
from predict import Predict


class FirstPage:
    def __init__(self, other_frame):
        self.other_frame = other_frame
        other_frame.title('人工智能分类器')
        win_width, win_height = other_frame.maxsize()
        other_frame.geometry('750x500' + f'+{win_width // 2 - 375}+{win_height // 2 - 250}')
        other_frame.resizable(width=False, height=False)

        InitPage(self.other_frame)

class InitPage:
    def __init__(self, master):
        self.master = master
        self.initface = tkinter.Frame(self.master)
        self.initface.pack()
        self.texts = \
        """
        欢迎使用人工智能分类器
        内置集成了很多现有模型
          及优化器和损失函数
        无须注册，未使用数据库
          不必担心信息泄露！
          \n\n\n
        """
        tkinter.Label(self.initface, text=self.texts, font=('华文彩云', 20)).pack()
        tkinter.Button(self.initface, text='点此进入', command=self.change, width=25).pack()
        tkinter.Label(self.initface, text='\n\n版本： 0.1.0\n创始人： 马硕\n未经授权，不得转载！', font=('华文彩云', 15)).pack()

    def change(self):
        self.initface.destroy()
        MainPage(self.master)

class MainPage:
    def __init__(self, root):
        self.root = root
        self.mainface = tkinter.Frame(self.root)
        self.mainface.pack()

        tkinter.Label(root, text='选择训练集目录：', font=('华文彩云', 15)).place(x=50, y=20)
        tkinter.Label(root, text='选择测试集目录：', font=('华文彩云', 15)).place(x=50, y=70)
        tkinter.Label(root, text='选择权重保存目录：', font=('华文彩云', 15)).place(x=40, y=120)

        self.train_path = tkinter.StringVar()
        entry = tkinter.Entry(root, textvariable=self.train_path, font=('FangSong', 13), width=35, state='readonly')
        entry.place(x=230, y=25)  # 训练集
        self.test_path = tkinter.StringVar()
        entry = tkinter.Entry(root, textvariable=self.test_path, font=('FangSong', 13), width=35, state='readonly')
        entry.place(x=230, y=75)  # 测试集
        self.save_weights = tkinter.StringVar()
        entry = tkinter.Entry(root, textvariable=self.save_weights, font=('FangSong', 13), width=35, state='readonly')
        entry.place(x=230, y=125)  # 权重

        tkinter.Button(root, text='选择路径', command=self.get_train_path, font=('FangSong', 15)).place(x=580, y=15)
        tkinter.Button(root, text='选择路径', command=self.get_test_path, font=('FangSong', 15)).place(x=580, y=65)
        tkinter.Button(root, text='选择路径', command=self.weights_save, font=('FangSong', 15)).place(x=580, y=115)

        # 模型选择
        tkinter.Label(root, text='模型选择：', font=('华文彩云', 15)).place(x=100, y=170)
        self.models_text = tkinter.StringVar()
        models_list = ['swin_tiny_patch4_window7_224',
                       'swin_small_patch4_window7_224',
                       'swin_base_patch4_window7_224',
                       'swin_base_patch4_window7_224_in22k',
                       'convnext_tiny',
                       'convnext_small',
                       'convnext_base',
                       'efficientnet-b0',
                       'efficientnet-b1',
                       'efficientnet-b2',
                       'efficientnet-b3',
                       'efficientnet-b4',
                       'efficientnet-b5',
                       'efficientnet-b6',
                       'efficientnet-b7',
                       'RNN'
                       ]
        self.model_box = ttk.Combobox(root,
                                      font=('FangSong', 10),
                                      textvariable=self.models_text,
                                      values=models_list,
                                      state='readonly',
                                      width=20)
        self.model_box.place(x=230, y=170)

        # 损失函数选择
        tkinter.Label(root, text='损失函数：', font=('华文彩云', 15)).place(x=100, y=220)
        self.loss_text = tkinter.StringVar()
        self.loss_list = ['MSELoss',
                          'CrossEntropyLoss',
                          'NLLLoss'
                          ]
        self.loss_box = ttk.Combobox(root,
                                     font=('FangSong', 10),
                                     textvariable=self.loss_text,
                                     values=self.loss_list,
                                     state='readonly',
                                     width=20)
        self.loss_box.current(1)  # 默认选中项目（索引）
        self.loss_box.place(x=230, y=220)

        # 优化器选择
        tkinter.Label(root, text='优化器：', font=('华文彩云', 15)).place(x=120, y=270)
        self.optim_text = tkinter.StringVar()
        self.optim_list = ['SGD',
                           'RMSprop',
                           'Adam'
                           ]
        self.optim_box = ttk.Combobox(root,
                                      font=('FangSong', 10),
                                      textvariable=self.optim_text,
                                      values=self.optim_list,
                                      state='readonly',
                                      width=20)
        self.optim_box.current(0)
        self.optim_box.place(x=230, y=270)

        # batch_size
        tkinter.Label(root, text='batch_size：', font=('华文彩云', 15)).place(x=430, y=220)
        self.bs_text = tkinter.StringVar()
        self.bs_list = [
            '5',
            '10',
            '15',
            '20',
            '25',
            '30',
            '35',
            '40',
            '45',
            '50'
        ]
        self.bs_box = ttk.Combobox(root,
                                      font=('FangSong', 10),
                                      textvariable=self.bs_text,
                                      values=self.bs_list,
                                      state='readonly',
                                      width=20)
        self.bs_box.current(4)
        self.bs_box.place(x=550, y=222)

        # 数据增强
        tkinter.Label(root, text='数据增强：', font=('华文彩云', 15)).place(x=80, y=320)
        self.check_text1 = tkinter.IntVar()
        self.check_text2 = tkinter.IntVar()
        self.check_text3 = tkinter.IntVar()
        self.check_text4 = tkinter.IntVar()
        self.check_text5 = tkinter.IntVar()
        self.check_text6 = tkinter.IntVar()
        ttk.Checkbutton(root, variable=self.check_text1, text='ToTensor',
                        onvalue=1, offvalue=0).place(x=225, y=320)
        ttk.Checkbutton(root, variable=self.check_text2, text='ReSize(224,224)',
                        onvalue=1, offvalue=0).place(x=380, y=320)
        ttk.Checkbutton(root, variable=self.check_text3, text='RandomHorizontalFlip',
                        onvalue=1, offvalue=0).place(x=550, y=320)
        ttk.Checkbutton(root, variable=self.check_text4, text='RandomResizedCrop',
                        onvalue=1, offvalue=0).place(x=225, y=370)
        ttk.Checkbutton(root, variable=self.check_text5, text='RandomVerticalFlip',
                        onvalue=1, offvalue=0).place(x=380, y=370)
        ttk.Checkbutton(root, variable=self.check_text6, text='Normalize', onvalue=1,
                        offvalue=0).place(x=550, y=370)
        # 开始训练
        self.bu = tkinter.Button(root, command=lambda: self.change(
            self.models_text,
            self.loss_text,
            self.optim_text,
            self.train_path,
            self.test_path,
            self.save_weights,
            self.bs_text
        ), font=('FangSong', 15), text='开始训练')
        self.bu.place(x=220, y=420)

        # 启用测试
        self.test_bu = tkinter.Button(root, command=self.test_image, font=('FangSong', 15), text='启用测试')
        self.test_bu.place(x=420, y=420)

    def get_train_path(self):
        """注意，以下列出的方法都是返回字符串而不是数据流"""
        # 返回一个字符串，且只能获取文件夹路径，不能获取文件的路径。
        path = filedialog.askdirectory(title='请选择一个目录')
        self.train_path.set(path)

    def get_test_path(self):
        """注意，以下列出的方法都是返回字符串而不是数据流"""
        # 返回一个字符串，且只能获取文件夹路径，不能获取文件的路径。
        path = filedialog.askdirectory(title='请选择一个目录')
        self.test_path.set(path)

    def weights_save(self):
        """注意，以下列出的方法都是返回字符串而不是数据流"""
        # 返回一个字符串，且只能获取文件夹路径，不能获取文件的路径。
        path = filedialog.askdirectory(title='请选择一个目录')
        self.save_weights.set(path)

    def change(self, models, losses, optims, train_path_, test_path_, save_weights_, bs_text_):
        model = models.get()
        loss = losses.get()
        optim = optims.get()
        train_path = train_path_.get()
        test_path = test_path_.get()
        save_weights = save_weights_.get()
        bs_text = bs_text_.get()
        batch_size = int(bs_text)

        transforms = {
            'ToTensor': self.check_text1.get(),
            'ReSize': self.check_text2.get(),
            'RandomHorizontalFlip': self.check_text3.get(),
            'RandomResizedCrop': self.check_text4.get(),
            'RandomVerticalFlip': self.check_text5.get(),
            'Normalize': self.check_text6.get()
        }

        if model != '' and loss != '' and optim != '' \
                and train_path != '' and save_weights != '':
            TrainPage(model, loss, optim, train_path, test_path, save_weights, transforms, batch_size)
        else:
            messagebox.showerror(title='出错了', message='信息填写不能有空！！！')

    def test_image(self):
        test_path = self.test_path.get()

        if test_path != '':
            Predict(test_path)
        else:
            messagebox.showerror(title='出错了', message='请填写预测的目录！！')


class TrainPage:
    def __init__(self, model, loss, optim, train_path, test_path, save_weights, transforms, batch_size):
        self.top = tkinter.Toplevel()
        self.top.title(model)
        win_width, win_height = self.top.maxsize()
        self.top.geometry('750x500' + f'+{win_width // 2 - 375}+{win_height // 2 - 250}')
        self.top.resizable(width=False, height=False)
        run = BeginTrain(self.top, model, loss, optim, train_path, test_path, save_weights, transforms, batch_size)
        th1 = threading.Thread(target=run.pre_train)
        num_classes = dataset.get_num_classes(train_path)
        tkinter.Label(self.top, text=f'epochs: 30\nnum_classes: {num_classes}', font=('华文彩云', 25)).place(x=290, y=0)
        text = \
        """
        注： 模型训练时间可能很长，这取决于你的配置！
        分类器支持多模型同时训练，如无需要，请勿使用！
        """
        tkinter.Label(self.top, text=text, font=('FangSong', 15)).place(x=30, y=100)
        th1.start()
        self.top.mainloop()


if __name__ == '__main__':
    base = tkinter.Tk()
    FirstPage(base)
    base.mainloop()
