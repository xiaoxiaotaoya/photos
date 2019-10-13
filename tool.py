# coding: utf-8
from PIL import Image
import os
import sys
import json
from datetime import datetime
from ImageProcess import Graphics
import shutil

dir, min_dir = "photos/", "min_photos/"
list_dir=[]

def directory_exists(directory):
    """判断目录是否存在"""
    if os.path.exists(directory):
        return True
    else:
        return False

def make_directory():
    if not os.path.exists(min_dir):
        os.mkdir(min_dir)
    else:
        shutil.rmtree(min_dir)
        os.mkdir(min_dir)
    files = os.listdir(dir)  # 得到文件夹下的所有文件名称
    for file in files:
            if os.path.isdir(dir + file):  # 判断是否是文件夹
                list_dir.append(file)
    print(list_dir)  # 打印结果
    for i in range(len(list_dir)):
        if not os.path.exists(min_dir + list_dir[i]):
            os.makedirs(min_dir + list_dir[i])
        print("创建{}文件夹".format(list_dir[i]))


def list_img_file(directory):
    """列出目录下所有文件，并筛选出图片文件列表返回"""
    old_list = os.listdir(directory)
    # print old_list
    new_list = []
    for filename in old_list:
        name, fileformat = filename.split(".")
        if fileformat.lower() == "jpg" or fileformat.lower() == "png" or fileformat.lower() == "gif":
            new_list.append(filename)
    # print new_list
    return new_list


def cut_photo():
    """裁剪算法

    ----------
    调用Graphics类中的裁剪算法，将dir目录下的文件进行裁剪（裁剪成正方形）
    """
    for i in range(len(list_dir)):
        file_list = list_img_file(dir + list_dir[i])
        for infile in file_list:
            img = Image.open(dir + list_dir[i] + "/" + infile)
            Graphics(infile=dir + list_dir[i] + "/" + infile, outfile=min_dir + list_dir[i] + "/" + infile).cut_by_ratio()
        else:
            pass
    print("裁剪完成")  # 打印结果

if __name__ == "__main__":
    make_directory()
    cut_photo()

