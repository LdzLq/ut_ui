import tkinter
from tkinter import filedialog
from tkinter import messagebox
import os
import RNNS
import torch
import torch.nn as nn
from PIL import Image, ImageTk
from torchvision.transforms import *
from efficientnet_pytorch import EfficientNet
from swin import swin_tiny_patch4_window7_224, swin_small_patch4_window7_224, \
    swin_base_patch4_window7_224, swin_base_patch4_window7_224_in22k
from convnext import convnext_tiny, convnext_small, convnext_base

class Predict:
    def __init__(self, test_path):
        self.top = tkinter.Toplevel()
        self.now_img_path = ''
        self.test_path = test_path
        self.images_path = []
        self.__get_images()
        self.top.title('测试模式')
        win_width, win_height = self.top.maxsize()
        self.top.geometry('750x500' + f'+{win_width // 2 - 375}+{win_height // 2 - 250}')
        self.top.resizable(width=False, height=False)

        self.now_count = 0
        self.all_imgs = len(os.listdir(self.test_path))
        self.image = None
        self.photo = None

        self.get_weight = 0

        tkinter.Label(self.top, text='选择参数位置：', font=('华文彩云', 15)).place(x=50, y=20)

        tkinter.Label(self.top, text='预测结果：', font=('华文彩云', 15)).place(x=210, y=110)

        self.weight_path = tkinter.StringVar()
        entry = tkinter.Entry(self.top,
                              textvariable=self.weight_path, font=('FangSong', 13), width=35, state='readonly')
        entry.place(x=230, y=25)  # 训练集

        tkinter.Button(self.top, text='选择路径', command=self.get_weights_path, font=('FangSong', 15)).place(x=580, y=15)

        tkinter.Button(self.top, text='上一张', command=self.before, font=('FangSong', 15)).place(x=100, y=105)
        tkinter.Button(self.top, text='下一张', command=self.up, font=('FangSong', 15)).place(x=580, y=105)

        tkinter.Button(self.top, text='预测', command=self.open_predict, font=('FangSong', 15)).place(x=320, y=450)

        # 显示图片
        self.img_gif = tkinter.PhotoImage(file=self.now_img_path)
        self.label_img = tkinter.Label(self.top, image=self.img_gif, background='blue', width=650, height=270)
        self.label_img.place(x=50, y=150)
        self.top.mainloop()

    def get_weights_path(self):
        weights_path = filedialog.askopenfilename(title='请选择文件')

        if '.pth' not in weights_path:
            messagebox.showerror(title='出错了', message='请检查你的权重路径是否正确！！！')
        else:
            self.get_weight = 1
            self.weight_path.set(weights_path)

    def __get_images(self):
        images_list = os.listdir(self.test_path)

        for i in images_list:
            path = self.test_path + '/' + i
            self.images_path.append(path)

        self.now_img_path = self.images_path[0]

    def before(self):
        if self.now_count > 0:
            self.now_count -= 1
            self.now_img_path = self.images_path[self.now_count]

            self.img_gif = tkinter.PhotoImage(file=self.now_img_path)
            self.label_img.configure(image=self.img_gif)

    def up(self):
        if self.now_count < self.all_imgs:
            self.now_count += 1
            self.now_img_path = self.images_path[self.now_count]

            self.img_gif = tkinter.PhotoImage(file=self.now_img_path)
            self.label_img.configure(image=self.img_gif)

    def open_predict(self):
        if self.weight_path.get() == '':
            messagebox.showerror(title='出错了', message='请检查你的权重路径是否正确！！！')
        else:
            num_classes = int(self.weight_path.get().split('+')[-2])
            model = self.weight_path.get().split('+')[-3]

            device = torch.device('cuda' if torch.cuda.is_available() else "cpu")

            model_dict = {
                'swin_tiny_patch4_window7_224':
                    swin_tiny_patch4_window7_224(num_classes=num_classes).to(device),
                'swin_small_patch4_window7_224':
                    swin_small_patch4_window7_224(num_classes=num_classes).to(device),
                'swin_base_patch4_window7_224':
                    swin_base_patch4_window7_224(num_classes=num_classes).to(device),
                'swin_base_patch4_window7_224_in22k':
                    swin_base_patch4_window7_224_in22k(num_classes=num_classes).to(device),
                'convnext_tiny':
                    convnext_tiny(num_classes=num_classes).to(device),
                'convnext_small':
                    convnext_small(num_classes=num_classes).to(device),
                'convnext_base':
                    convnext_base(num_classes=num_classes).to(device),
                'efficientnet-b0':
                    self.makemodel_efficientnet(0, device, num_classes),
                'efficientnet-b1':
                    self.makemodel_efficientnet(1, device, num_classes),
                'efficientnet-b2':
                    self.makemodel_efficientnet(2, device, num_classes),
                'efficientnet-b3':
                    self.makemodel_efficientnet(3, device, num_classes),
                'efficientnet-b4':
                    self.makemodel_efficientnet(4, device, num_classes),
                'efficientnet-b5':
                    self.makemodel_efficientnet(5, device, num_classes),
                'efficientnet-b6':
                    self.makemodel_efficientnet(6, device, num_classes),
                'efficientnet-b7':
                    self.makemodel_efficientnet(7, device, num_classes),
                'RNN':
                    RNNS.RNNimc(input_dim=224, output_dim=num_classes).to(device)
            }

            model = model_dict[model]
            model.load_state_dict(torch.load(self.weight_path.get(), map_location=device))

            transform = Compose([
                Resize((224, 224)),
                ToTensor()
            ])

            image = Image.open(self.now_img_path)
            image = transform(image)
            image = torch.unsqueeze(image, dim=0)
            output = model(image.to(device))
            pre_lab = torch.argmax(output, 1)

            tkinter.Label(self.top, text=str(int(pre_lab)), font=('FangSong', 20)).place(x=350, y=105)

    def makemodel_efficientnet(self, num, device, num_classes):
        model = EfficientNet.from_name(f'efficientnet-b{num}').to(device)
        feature = model._fc.in_features
        model._fc = nn.Linear(in_features=feature, out_features=num_classes, bias=True).to(device)
        return model
