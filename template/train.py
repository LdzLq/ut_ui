import tkinter
from tkinter import ttk
import torch
import torch.nn as nn
from torchvision.transforms import *
from efficientnet_pytorch import EfficientNet
from swin import swin_tiny_patch4_window7_224, swin_small_patch4_window7_224, \
    swin_base_patch4_window7_224, swin_base_patch4_window7_224_in22k
from convnext import convnext_tiny, convnext_small, convnext_base
import dataset
import RNNS
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder
from tkinter import messagebox

class BeginTrain:
    def __init__(self, top, model, loss, optim, train_path, test_path, save_weights, transforms, batch_size):
        self.top = top
        self.models = model
        self.loss = loss
        self.optim = optim
        self.train_path = train_path
        self.test_path = test_path
        self.save_weights = save_weights
        self.transforms = transforms
        self.batch_size = batch_size
        self.device = torch.device('cuda' if torch.cuda.is_available() else "cpu")
        self.num_classes = dataset.get_num_classes(self.train_path)
        model_dict = {
            'swin_tiny_patch4_window7_224':
                swin_tiny_patch4_window7_224(num_classes=self.num_classes).to(self.device),
            'swin_small_patch4_window7_224':
                swin_small_patch4_window7_224(num_classes=self.num_classes).to(self.device),
            'swin_base_patch4_window7_224':
                swin_base_patch4_window7_224(num_classes=self.num_classes).to(self.device),
            'swin_base_patch4_window7_224_in22k':
                swin_base_patch4_window7_224_in22k(num_classes=self.num_classes).to(self.device),
            'convnext_tiny':
                convnext_tiny(num_classes=self.num_classes).to(self.device),
            'convnext_small':
                convnext_small(num_classes=self.num_classes).to(self.device),
            'convnext_base':
                convnext_base(num_classes=self.num_classes).to(self.device),
            'efficientnet-b0':
                self.makemodel_efficientnet(0),
            'efficientnet-b1':
                self.makemodel_efficientnet(1),
            'efficientnet-b2':
                self.makemodel_efficientnet(2),
            'efficientnet-b3':
                self.makemodel_efficientnet(3),
            'efficientnet-b4':
                self.makemodel_efficientnet(4),
            'efficientnet-b5':
                self.makemodel_efficientnet(5),
            'efficientnet-b6':
                self.makemodel_efficientnet(6),
            'efficientnet-b7':
                self.makemodel_efficientnet(7),
            'RNN':
                RNNS.RNNimc(input_dim=224, output_dim=self.num_classes).to(self.device)
        }

        self.model = model_dict[self.models]

        loss_dict = {
            'MSELoss': nn.MSELoss(),
            'CrossEntropyLoss': nn.CrossEntropyLoss(),
            'NLLLoss': nn.NLLLoss()
        }

        self.criterion = loss_dict[self.loss]

        optim_dict = {
            'SGD': torch.optim.SGD(self.model.parameters(), lr=0.001, momentum=0.5),
            'RMSprop': torch.optim.RMSprop(self.model.parameters(), lr=0.001, momentum=0.5),
            'Adam': torch.optim.Adam(self.model.parameters(), lr=0.001)
        }

        self.optimizer = optim_dict[self.optim]
        if self.optim == 'SGD':
            self.scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(self.optimizer, T_max=5, eta_min=1e-5)

        transforms_list = []
        if self.transforms['ToTensor'] == 1:
            transforms_list.append(ToTensor())
        if self.transforms['ReSize'] == 1:
            transforms_list.append(Resize((224, 224)))
        if self.transforms['RandomHorizontalFlip'] == 1:
            transforms_list.append(RandomHorizontalFlip(p=0.5))
        if self.transforms['RandomResizedCrop'] == 1:
            transforms_list.append(RandomResizedCrop((224, 224)))
        if self.transforms['RandomVerticalFlip'] == 1:
            transforms_list.append(RandomVerticalFlip(p=0.5))
        if self.transforms['Normalize'] == 1:
            transforms_list.append(ToTensor())
        self.open_transform = Compose(transforms_list)

        try:
            # 加载数据
            train_data = ImageFolder(
                self.train_path,
                transform=self.open_transform
            )

            # 加载训练集和验证集
            self.train_dataloader = DataLoader(train_data, batch_size=self.batch_size,
                                               shuffle=True)
        except:
            messagebox.showerror(title='出错了', message='训练集路径有误！！！')

        self.batch_num = len(self.train_dataloader)
        self.train_batch_num = round(self.batch_num * 0.8)

        # 全局参数
        self.train_loss = []
        self.val_loss = []

    def pre_train(self):
        tkinter.Label(self.top, text='总进度：', font=('FangSong', 15)).place(x=45, y=250)
        progressbar = tkinter.ttk.Progressbar(self.top, length=450)
        progressbar.place(x=150, y=255)
        progressbar['maximum'] = 30
        progressbar['value'] = 0

        try:
            # 训练
            for step, epoch in enumerate(range(1, 30 + 1)):
                tkinter.Label(self.top, text=f'epoch {step + 1}/30：', font=('FangSong', 13)).place(x=30, y=200)
                progressbarOne = tkinter.ttk.Progressbar(self.top, length=450)
                progressbarOne.place(x=150, y=205)
                progressbarOne['maximum'] = len(self.train_dataloader)
                progressbarOne['value'] = 0
                self.open_train(progressbarOne)

                torch.save(self.model.state_dict(),
                           self.save_weights + "\\+{}+{}+{}.pth".format(self.models, self.num_classes, epoch))

                progressbar['value'] += 1
                self.top.update()

            # 清空使用过的gpu缓冲区
            torch.cuda.empty_cache()

            # 训练结束
            messagebox.showinfo(title='人工智能训练器', message='训练完成')
        except RuntimeError:
            messagebox.showerror(title='出错了', message='配置不足，请选择较小的batch_size！')

    def makemodel_efficientnet(self, num):
        model = EfficientNet.from_name(f'efficientnet-b{num}').to(self.device)
        feature = model._fc.in_features
        model._fc = nn.Linear(in_features=feature, out_features=self.num_classes, bias=True).to(self.device)
        return model

    def open_train(self, progressbarOne):
        for step, (data, target) in enumerate(self.train_dataloader):
            data, target = data.to(self.device), target.to(self.device)
            if step < self.train_batch_num:
                self.model.train()
                self.optimizer.zero_grad()  # 模型参数梯度清零
                output = self.model(data)
                loss = self.criterion(output, target)
                loss.backward()
                self.train_loss.append(loss.item())
                # 调整参数
                self.optimizer.step()
            else:
                # 获得每一个批次的acc
                predict_acc = self.val(data, target)
                tkinter.Label(self.top,
                              text=f'now_val_acc: {predict_acc:.4f}', font=('FangSong', 20)).place(x=250, y=350)
            progressbarOne['value'] += 1
            self.top.update()

        # 调整学习率
        self.scheduler.step()

    def val(self, data, target):

        self.model.eval()

        # 初始化参数
        val_one_loss = 0
        # 一个批次的正确率
        correct = 0
        # 一个批次的数量
        total = 0

        with torch.no_grad():
            output = self.model(data)
            # print(output.shape)
        self.val_loss.append(self.criterion(output, target).item())
        val_one_loss += self.criterion(output, target).item()

        pred = torch.argmax(output, 1)
        correct += (pred == target).sum().float()
        total += len(target)
        predict_acc = correct / total

        # 返回当前批次的最好acc
        return predict_acc
