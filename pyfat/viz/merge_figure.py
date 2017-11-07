# !/usr/bin/python
# -*- coding: utf-8 -*-

import glob
import matplotlib.pyplot as plt


def path_list(prefix):
    # prefix = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander' \
    #          '/100408/result/result20vs45/cc_clustering_png1/100408lr15'
    # prefix = input('Input the prefix of images:')
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

    return files


def montage_plotting(pic_path, column_num, row_num, s=None, text_list=None, text_loc=(0, 50), fontsize=12,
                      fontcolor='w'):
    """
    Show pictures in a figure
    Author: Huang taicheng
    Parameters:
    -----------
    pic_path: path of pictures, as a list
    column_num: picture numbers shown in each column
    row_num: picture numbers shown in each row
    text_list: whether to show text in each picture, by default is None
    text_loc: text location
    fontsize: text font size
    fontcolor: text font color
    Example:
    ---------
    >>> plotmontage(pic_path, 8, 6, text_list)
    """
    try:
        from skimage import io as sio
    except ImportError as e:
        raise Exception('Please install skimage first')

    assert (len(pic_path) < column_num * row_num) | (len(
        pic_path) == column_num * row_num), "Number of pictures is larger than what subplot could accomdate, please increase column_num/row_num values"
    if text_list is not None:
        assert len(pic_path) == len(text_list), "pic_path shall have the same length as text_list"

    plt.figure(figsize=(2 * column_num, 2 * row_num))
    for i, ppath in enumerate(pic_path):
        img = sio.imread(ppath)
        ax = plt.subplot(row_num, column_num, i + 1)
        ax.set_axis_off()
        plt.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99, wspace=0.1, hspace=0.1)
        if text_list is not None:
            plt.text(text_loc[0], text_loc[1], text_list[i], fontsize=fontsize, color=fontcolor)
        plt.imshow(img)
        if s is not None:
            plt.savefig("/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander"
                        "/100408/result/result20vs45/cc_clustering_png1/merge/100408lr15_merge_%s.png" % s)
    plt.show()
