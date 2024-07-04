import os

def get_num_classes(train_path):
    path = os.listdir(train_path)
    return len(path)
