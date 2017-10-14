# -*- coding: utf-8 -*-
'''
    将文件夹里面所有文件夹的图片，进行合并放在一个文件夹里面。
    如A下面有A1,A2... 文件夹，然后An文件夹中有很多由数字命名的图片，如123.jpg/png
    现在可让他们和并在B文件夹，然后重新命名。（也是 数字命名）。

'''

import os
import shutil
import sys
from random import shuffle

pre_root_path = os.path.join(os.environ['HOME'],
                             'Code/PycharmProjects/AnimeSketchColorization/colorization/datasets/anime/')

src_path_raw = os.path.join(pre_root_path, 'select_raw')
des_path_combine_raw = os.path.join(pre_root_path, 'combine_raw')


# 合并
def combine_pics(src_path=src_path_raw, des_path=des_path_combine_raw):
    all_des_abs_path = []
    # 获得所有An文件夹
    src_floders = os.listdir(src_path)
    for each_floder in src_floders:
        # 获取A1文件夹下面所有图片
        files = os.listdir(os.path.join(src_path_raw, each_floder))
        for file in files:
            abs_file = os.path.join(src_path_raw, each_floder, file)
            all_des_abs_path.append(abs_file)
    shuffle(all_des_abs_path)
    for (i, each) in enumerate(all_des_abs_path):
        jpg_png = each.split('.')[-1]
        des_file = os.path.join(des_path, str(i) + '.' + jpg_png)
        shutil.copy(each, des_file)
