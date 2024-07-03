import tkinter as tk
from tkinter import ttk  # 导入ttk模块以使用滚动条

def on_upper_button_click(index):
    """上模块按钮点击示例处理函数"""
    print(f"上模块按钮{index}被点击")

def on_lower_button_click(text):
    """下模块按钮点击示例处理函数"""
    print(f"下模块按钮'{text}'被点击")

def create_upper_module(parent):
    """创建上模块，包含多行，每行有文本显示框和两个按钮"""
    upper_frame = tk.Frame(parent, bd=2, relief="solid", padx=5, pady=5)
    for i in range(3):  # 示例中创建3行
        row_frame = tk.Frame(upper_frame, pady=5)
        tk.Label(row_frame, text=f"文本显示框{i+1}", width=20, anchor="w").pack(side=tk.LEFT, padx=5)  # 文本显示框
        tk.Button(row_frame, text="按钮A", command=lambda idx=i: on_upper_button_click(idx)).pack(side=tk.RIGHT, padx=5)  # 按钮A
        tk.Button(row_frame, text="按钮B", command=lambda idx=i: on_upper_button_click(idx)).pack(side=tk.RIGHT, padx=5)  # 按钮B
        row_frame.pack(fill=tk.X)  # 让按钮水平充满行
    return upper_frame

def create_lower_module(parent):
    """创建下模块，包含可滚动的文字按钮列表"""
    lower_frame = tk.Frame(parent, bd=2, relief="solid", padx=5, pady=5)
    canvas = tk.Canvas(lower_frame)
    scrollbar = ttk.Scrollbar(lower_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    for i in range(10):  # 示例中创建10个按钮
        tk.Button(scrollable_frame, text=f"按钮{i+1}", command=lambda txt=f"Button {i+1}": on_lower_button_click(txt)).pack(fill=tk.X)

    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    return lower_frame

def main():
    root = tk.Tk()
    root.title("双模块界面示例")

    upper_module = create_upper_module(root)
    lower_module = create_lower_module(root)

    upper_module.pack(fill=tk.BOTH, expand=True)
    lower_module.pack(fill=tk.BOTH, expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()