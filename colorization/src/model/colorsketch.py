# -*- coding:utf-8 -*-
'''
    通过训练好的模型，传入手绘图片，返回上色图片。
'''
import os

os.environ["KERAS_BACKEND"] = "tensorflow"

import keras.backend as K

image_dim_ordering = "tf"
K.set_image_dim_ordering(image_dim_ordering)
from model import models
from keras.optimizers import Adam, SGD

import numpy as np
import h5py

import matplotlib.pylab as plt
from PIL import Image
import numpy as np
from utils import data_utils

img_dim = (256, 256, 3)

bn_mode = 2

# 对于generator_unet_upsampling是无关变量
nb_patch = None
use_mbd = None  # True
batch_size = None  # 4


def get_generator_unet_upsampling(weight_path):
    # model_name = "generator_unet_upsampling"
    generator = "upsampling"
    generator_model = models.load("generator_unet_%s" % generator,
                                  img_dim=img_dim,
                                  nb_patch=nb_patch,
                                  bn_mode=bn_mode,
                                  use_mbd=use_mbd,
                                  batch_size=batch_size)
    opt_generator = Adam(lr=1E-3, beta_1=0.9, beta_2=0.999, epsilon=1e-08)
    generator_model.compile(loss='mae', optimizer=opt_generator)
    generator_model.load_weights(weight_path)
    return generator_model


def get_sketch_arr(sketch_path):
    image = Image.open(sketch_path)  # image is a PIL image
    imgrgb = image.convert('RGB')
    array = np.array(imgrgb)  # array is a numpy array
    array = array.reshape(img_dim)  # (256,256,3)
    return array


def get_image(colorful_img):
    colorful_img = colorful_img.reshape((img_dim[-1],) + img_dim[:2])  # (3,256,256)
    r = Image.fromarray(colorful_img[0]).convert('L')
    g = Image.fromarray(colorful_img[1]).convert('L')
    b = Image.fromarray(colorful_img[2]).convert('L')
    image = Image.merge("RGB", (r, g, b))
    return image


# sketch_path='/home/luo/Code/PycharmProjects/AnimeSketchColorization/colorization/datasets/anime_test/568.jpg'
# weight_path='/home/luo/Code/PycharmProjects/AnimeSketchColorization/colorization/models/CNN/gen_weights_epoch120.h5'
# des_path='/home/luo/Code/PycharmProjects/AnimeSketchColorization/colorization/datasets/anime_test/gen_567.jpg'
def color_sketch(sketch_path, des_path, weight_path, ):
    # try:
    generator_model = get_generator_unet_upsampling(weight_path)
    sketch_img = data_utils.normalization(get_sketch_arr(sketch_path))  # (1,256,263,3)
    gen_image = generator_model.predict(sketch_img.reshape((1,) + sketch_img.shape))
    gen_image_tmp = data_utils.inverse_normalization(gen_image)
    gen_image_tmp = gen_image_tmp.reshape(gen_image_tmp.shape[1:])
    gen_image_tmp *= 254
    colorful_img = get_image(gen_image_tmp)
    colorful_img.save(des_path)
    # colorful_img.show()
    return colorful_img
    # except Exception as e:
    #     print(e)
    #     return None

# weight_path='~/Code/experiment/luomingnan/code/luonango/extras/keras/DeepLearningImplementations/pix2pix/models/CNN/gen_weights_epoch120.h5'
#
#
# sketch_path='/home/luo/Code/PycharmProjects/AnimeSketchColorization/colorization/datasets/anime_test/568.jpg'
# weight_path='/home/luo/Code/PycharmProjects/AnimeSketchColorization/colorization/models/CNN/gen_weights_epoch120.h5'
# des_path='/home/luo/Code/PycharmProjects/AnimeSketchColorization/colorization/datasets/anime_test/gen_567.jpg'
#
#
# aa=color_sketch(sketch_path=sketch_path,weight_path=weight_path,des_path=des_path)
#
# sketch_path='/home/luo/Code/PycharmProjects/AnimeSketchColorization/colorization/datasets/anime_test/20.jpg'
#
# sketch_img = data_utils.normalization(get_sketch_arr(sketch_path))  # (1,256,263,3)
# gen_image = generator_model.predict(sketch_img.reshape((1,)+sketch_img.shape))
# gen_image_tmp = data_utils.inverse_normalization(gen_image)
# gen_image_tmp=gen_image_tmp.reshape(gen_image_tmp.shape[1:])
# gen_image_tmp*=254
# colorful_img = get_image(gen_image_tmp)
# colorful_img.show()
