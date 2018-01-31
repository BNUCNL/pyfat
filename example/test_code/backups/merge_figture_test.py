# !/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
from PIL import Image
import glob, os
import matplotlib.pyplot as plt


if __name__ == '__main__':
    prefix = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander' \
             '/100408/result/result20vs45/cc_clustering_png1/100408lr15'
    #input('Input the prefix of images:')
    files = glob.glob(prefix + '_*')
    num = len(files)

    filename_lens = [len(x) for x in files]  # length of the files
    min_len = min(filename_lens)  # minimal length of filenames
    max_len = max(filename_lens)  # maximal length of filenames
    if min_len == max_len:  # the last number of each filename has the same length
        files = sorted(files)  # sort the files in ascending order
    else:  # maybe the filenames are:x_0.png ... x_10.png ... x_100.png
        index = [0 for x in range(num)]
        for i in range(num):
            filename = files[i]
            start = filename.rfind('_') + 1
            end = filename.rfind('.')
            file_no = int(filename[start:end])
            index[i] = file_no
        index = sorted(index)
        files = [prefix + '_' + str(x) + '.png' for x in index]

    # fig = plt.figure(figsize=(2*8, 2*6))
    # for i in range(len(files)):
    #     img = Image.open(files[i])
    #     ax = plt.subplot(8, 6, i+1)
    #     ax.set_axis_off()
    #     plt.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99, wspace=0.1, hspace=0.1)
    #     plt.imshow(img)
    # plt.show()

    # print(files[0])
    # baseimg = Image.open(files[0])
    # sz = baseimg.size
    # basemat = np.atleast_2d(baseimg)
    # for i in range(1, num):
    #     file = files[i]
    #     im = Image.open(file)
    #     im = im.resize(sz, Image.ANTIALIAS)
    #     mat = np.atleast_2d(im)
    #     print(file)
    #     if i % 5 == 0 and i != 0:
    #         basemat = np.append(basemat, mat, axis=0)
    #     else:
    #         basemat = np.append(basemat, mat, axis=1)
    # final_img = Image.fromarray(basemat)
    # final_img.save('merged.png')

    from pyfat.viz.merge_figure import montage_plotting
    montage_plotting(files[:48], 8, 6, 1, text_list=range(48))
    montage_plotting(files[48:96], 8, 6, 2, text_list=range(48))
    montage_plotting(files[96:144], 8, 6, 3, text_list=range(48))
    montage_plotting(files[144:192], 8, 6, 4, text_list=range(48))
    montage_plotting(files[192:], 8, 6, 5, text_list=range(len(files[192:])))
