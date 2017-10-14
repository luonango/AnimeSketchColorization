#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Author:Nango

'''
import os
from PIL import Image

# almost CNN-ImageNet Model use (224,224) ImageNet比赛大多cnn模型采用(224，224)图片
pic_resize = (256, 256)

"""
调整全部图片
    调整src文件夹下所有图片，输出保存到des文件夹中
    Out_Info：
        输出程序执行信息
    RESIZE 调整图片尺寸：
        可选，默认调整到(224,224)格式。
        如果图片长宽不等，则裁剪crop图片，再将图片缩放到re_size
    Only_Mode 保留单一图片色彩模型：
        可选，默认只保存RGB图片
        若想保存RGB和YCbCr,则传入color_mode=["RGB","YCbCr"]
    
    return:
        0:  执行成功
        -1: Error,src不存在 

"""


def pics_adjust(src="./src/", des="./des/", Out_Info=False, RESIZE=True, re_size=pic_resize, Only_Mode=True,
                color_mode=["RGB"]):
    try:
        files = os.listdir(src)
    except:  # FileNotFoundError:
        if Out_Info:    print("pics_adjust: FileNotFoundError ", src)
        return -1  # 文件夹不存在
    if not os.path.exists(des):
        os.makedirs(des)
    for each in files:
        if not ("jpg" in each):
            continue
        try:
            img = Image.open(os.path.join(src, str(each)))
        except:
            continue
        # 解决Only_Mode问题
        if Only_Mode:
            if img.mode not in color_mode:
                continue
        # 解决图片resize问题
        try:
            if RESIZE:
                # img=get_square_pic(img)
                img = img.resize(re_size, Image.ANTIALIAS)
            img.save(os.path.join(des, str(each)), quality=100)
        except:
            continue
    if Out_Info:    print("pics_adjust successed.")
    return 0


"""
将图片裁剪成正方形图片。居中裁剪
"""


def get_square_pic(img=None):
    if img == None:   return img
    (l, s) = (img.height, img.width)
    if img.width > img.height:
        (l, s) = (img.width, img.height)
        z = (l - s) / 2
        img = img.crop((z, 0, z + s, s))
    elif img.width < img.height:
        z = (l - s) / 2
        img = img.crop((0, z, s, z + s))
    else:
        pass
    return img


'''
    传入一个文件夹，将里面图片按序号编排，存到另外一个文件夹中。
'''

import os
import shutil


def change_files_order(src="/home/luo/mongodb/data/tmp_pictures/", des="/home/luo/mongodb/data/pictures/",
                       des_max_num=-1):
    if (des_max_num == -1):
        imgs_des = os.listdir(des)
        for each in imgs_des:
            _num = int(each.split('.')[0])
            if _num > des_max_num:
                des_max_num = _num
    start_index = des_max_num + 1
    print(start_index)
    imgs_src = os.listdir(src)
    for each in imgs_src:
        shutil.copy(src + each, des + str(start_index) + ".jpg")
        start_index += 1
    print(start_index)


def test1():
    root_src = "/home/luo/Code/PycharmProjects/AnimeSketchColorization/colorization/datasets/anime/combine_raw"
    root_des = "/home/luo/Code/PycharmProjects/AnimeSketchColorization/colorization/datasets/anime/combine_resize_nosquare"
    if not os.path.exists(root_des):
        os.makedirs(root_des)
    pics_adjust(src=root_src, des=root_des, Out_Info=False, RESIZE=True, re_size=pic_resize, Only_Mode=True,
                color_mode=["RGB"])


# if __name__ == '__main__':
def test(class_name="combine_raw"):
    root_src = "/home/luo/Code/PycharmProjects/AnimeSketchColorization/colorization/datasets/anime/"
    files = os.listdir(os.path.join(root_src, class_name))
    for each in files:
        if str(each).startswith("results_"):
            src = str(each) + "/"
            des = "des_" + src
            if not os.path.exists(des):
                os.makedirs(des)
            print("read to pic_adjust")
            pics_adjust(src=src, des=des, Out_Info=False, RESIZE=True, re_size=pic_resize, Only_Mode=True,
                        color_mode=["RGB"])


def main_test():
    class_name = input("/home/luo/ml/data/images/baidu_clothes/")
    class_name = str(class_name)
    if (len(class_name) > 2):
        print("start...", class_name)
        test(class_name=class_name)


# 图片手绘
from PIL import Image
import numpy as np
import os

root_src = "/home/luo/Code/PycharmProjects/AnimeSketchColorization/colorization/datasets/anime/combine_resize_nosquare"
root_des = "/home/luo/Code/PycharmProjects/AnimeSketchColorization/colorization/datasets/anime/sketch_7_5"


def get_AnimeSketch(src=root_src, des=root_des):
    files = os.listdir(src)
    if not os.path.exists(root_des):
        os.makedirs(root_des)
    for filename in files:
        a = np.asarray(Image.open(os.path.join(src, filename)).convert('L')).astype('float')
        depth = 7.5  # (0-100)
        grad = np.gradient(a)  # 取图像灰度的梯度值
        grad_x, grad_y = grad  # 分别取横纵图像梯度值
        grad_x = grad_x * depth / 100.
        grad_y = grad_y * depth / 100.
        A = np.sqrt(grad_x ** 2 + grad_y ** 2 + 1.)
        uni_x = grad_x / A
        uni_y = grad_y / A
        uni_z = 1. / A
        vec_el = np.pi / 2.2  # 光源的俯视角度，弧度值
        vec_az = np.pi / 4.  # 光源的方位角度，弧度值
        dx = np.cos(vec_el) * np.cos(vec_az)  # 光源对x 轴的影响
        dy = np.cos(vec_el) * np.sin(vec_az)  # 光源对y 轴的影响
        dz = np.sin(vec_el)  # 光源对z 轴的影响
        b = 255 * (dx * uni_x + dy * uni_y + dz * uni_z)  # 光源归一化
        b = b.clip(0, 255)
        im = Image.fromarray(b.astype('uint8'))  # 重构图像
        im.save(os.path.join(des, filename))


# 图片拼接
import PIL.Image as Image
import os, sys

mw = 256  # 图片大小+图片间隔
ms = 2
msize = mw * ms

root_src1 = "/home/luo/Code/PycharmProjects/AnimeSketchColorization/colorization/datasets/anime/combine_resize_nosquare"
root_src2 = "/home/luo/Code/PycharmProjects/AnimeSketchColorization/colorization/datasets/anime/sketch_7_5"
root_des = "/home/luo/Code/PycharmProjects/AnimeSketchColorization/colorization/datasets/anime/combine_sketch_7_5"


def combine_pic_sketch(src1=root_src1, src2=root_src2, des=root_des):
    if not os.path.exists(des):
        os.makedirs(des)
    files = os.listdir(src1)
    for fname in files:
        fromImage1 = Image.open(os.path.join(src1, fname))
        fromImage2 = Image.open(os.path.join(src2, fname))
        toImage = Image.new('RGB', (msize, mw))
        toImage.paste(fromImage1, (0, 0))
        toImage.paste(fromImage2, (256, 0))
        # for y in range(1,2):  ## 先试一下 拼一个5*5 的图片
        #     for x in range(1, 3):
        #         # 之前保存的图片是顺序命名的，x_1.jpg, x_2.jpg ...
        #         fromImage = Image.open(fname)
        #         #fromImage =fromImage.resize((mw, mw), Image.ANTIALIAS)   # 先拼的图片不多，不用缩小
        #         toImage.paste(fromImage, ((x-1) * mw, (y-1) * mw))
        toImage.save(os.path.join(root_des, fname))


# 将文件夹中变为顺数数字

import os
import shutil


def change_name(src, des):
    files = os.listdir(src)
    for i, file in enumerate(files):
        src_file = os.path.join(src, file)
        houzui = file.split('.')[-1]
        des_file = os.path.join(des, str(i) + '.' + houzui)
        shutil.copy(src_file, des_file)


src = "/home/luo/Code/PycharmProjects/AnimeSketchColorization/colorization/datasets/anime_sketch/train_tmp/"
des = "/home/luo/Code/PycharmProjects/AnimeSketchColorization/colorization/datasets/anime_sketch/train/"

# change_name(src,des)
