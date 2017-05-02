#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 02 2017

The goal of this script is to vizualised the reponse of the filter of the
different convolution of the network

@author: nicolas
"""

import scipy
import numpy as np
import tensorflow as tf
import Style_Transfer as st
from Arg_Parser import get_parser_args 
import seaborn as sns
import matplotlib.pyplot as plt
import os
import pandas as pd
import math
from matplotlib.backends.backend_pdf import PdfPages


# Name of the 19 first layers of the VGG19
VGG19_LAYERS = (
    'conv1_1', 'relu1_1', 'conv1_2', 'relu1_2', 'pool1',

    'conv2_1', 'relu2_1', 'conv2_2', 'relu2_2', 'pool2',

    'conv3_1', 'relu3_1', 'conv3_2', 'relu3_2', 'conv3_3',
    'relu3_3', 'conv3_4', 'relu3_4', 'pool3',

    'conv4_1', 'relu4_1', 'conv4_2', 'relu4_2', 'conv4_3',
    'relu4_3', 'conv4_4', 'relu4_4', 'pool4',

    'conv5_1', 'relu5_1', 'conv5_2', 'relu5_2', 'conv5_3',
    'relu5_3', 'conv5_4', 'relu5_4'
)

def is_square(apositiveint):
    x = apositiveint // 2
    seen = set([x])
    while x * x != apositiveint:
        x = (x + (apositiveint // x)) // 2
        if x in seen: return False
        seen.add(x)
    return True

def plot_and_save(Matrix,path,name=''):
     Matrix = Matrix[0] # Remove first dim
     h,w,channels = Matrix.shape
     df_Matrix = pd.DataFrame(np.reshape(Matrix,(h*w,channels)))
     len_columns = len(df_Matrix.columns)
     if(len_columns<6):
         fig, axes = plt.subplots(1,len_columns)
     else:
         if(len_columns%4==0):
             fig, axes = plt.subplots(len_columns//4, 4)
         elif(len_columns%3==0):
             fig, axes = plt.subplots(len_columns//3, 3)
         elif(len_columns%5==0):
             fig, axes = plt.subplots(len_columns//5, 5)
         elif(len_columns%2==0):
             fig, axes = plt.subplots(len_columns//2, 2)
         else:
             j=6
             while(not(len_columns%j==0)):
                 j += 1
             fig, axes = plt.subplots(len_columns//j, j)
     
     i = 0
     axes = axes.flatten()
     for axis in zip(axes):
         df_Matrix.hist(column = i, bins = 64, ax=axis)
         i += 1
     pltname = path+name+'.png'
     # TODO avoid to Plot some ligne on the screen
     fig.savefig(pltname, dpi = 1000)

def plot_and_save_pdf(Matrix,path,name=''):
    pltname = path+name+'_hist.pdf'
    pltname_rep = path+name+'_img.pdf'
    pp = PdfPages(pltname)

    Matrix = Matrix[0] # Remove first dim
    h,w,channels = Matrix.shape
    df_Matrix = pd.DataFrame(np.reshape(Matrix,(h*w,channels)))
    len_columns = len(df_Matrix.columns)
    for i in range(len_columns):
        df_Matrix.hist(column = i, bins = 128)
        plt.savefig(pp, format='pdf')
        plt.close()
    pp.close()

    plt.clf()
    # Result of the convolution 
    pp_img = PdfPages(pltname_rep)
    for i in range(len_columns):
        plt.imshow(Matrix[:,:,i], cmap='gray')
        plt.savefig(pp_img, format='pdf')
        plt.close()
    pp_img.close()


def plot_Rep(args):
    
    directory_path = 'Results/Filter_Rep/'+args.style_img_name+'/' 
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    
    sns.set()
    image_style_path = args.img_folder + args.style_img_name + args.img_ext
    image_style = st.preprocess(scipy.misc.imread(image_style_path).astype('float32')) 
    _,image_h_art, image_w_art, _ = image_style.shape 
    plot_and_save_pdf(image_style,directory_path,'ProcessIm')
    print("Plot initial image")
    
    vgg_layers = st.get_vgg_layers()
    net = st.net_preloaded(vgg_layers, image_style) # net for the style image
    sess = tf.Session()
    sess.run(net['input'].assign(image_style))
    for layer in VGG19_LAYERS:
        a = net[layer].eval(session=sess)
        print(layer,a.shape)
        plot_and_save_pdf(a,directory_path,layer)


def main():
    parser = get_parser_args()
    style_img_name = "StarryNight"
    #style_img_name = "Louvre_Big"
    parser.set_defaults(style_img_name=style_img_name)
    args = parser.parse_args()
    plot_Rep(args)

if __name__ == '__main__':
    main()   