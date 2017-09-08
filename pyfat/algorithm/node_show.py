# !/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import numpy.linalg as npl
import matplotlib.pyplot as plt
from nibabel.affines import apply_affine


def show_2d_node(img, Ls_temp):
    fig, ax = plt.subplots()
    slice = img.get_data()[img.shape[0]/2, :, :]
    Ls_temp = apply_affine(npl.inv(img.affine), Ls_temp)
    ax.imshow(slice.T, cmap='gray', origin='lower')
    ax.plot(np.array(Ls_temp)[:, 1], np.array(Ls_temp)[:, 2], 'o')
    ax.set_title('y_z distribution')
    plt.show()

def show_dist_matrix(sdist):
    name = range(sdist.shape[0])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.imshow(slice.T, cmap='gray', origin='lower')
    cax = ax.matshow(sdist, vmin=-1, vmax=1)
    fig.colorbar(cax)
    ticks = np.arange(0, sdist.shape[0], 1)
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)
    ax.set_xticklabels(name)
    ax.set_yticklabels(name)
    plt.show()

def show_slice_density(img, Ls_temp):
    fig, ax = plt.subplots()
    Ls_temp = np.array(Ls_temp)
    Ls_temp.T[0] = 0
    Ls_temp = apply_affine(npl.inv(img.affine), Ls_temp)
    slice = img.get_data()[img.shape[0]/2, :, :]
    counts = np.zeros(slice.shape, 'int')
    for Ls in Ls_temp:
        j = Ls[1]
        k = Ls[2]
        counts[j, k] += 1

    count = counts == 0
    counts[count] = slice[count]
    count1 = counts > 0
    # ax.imshow(slice.T, cmap='gray', origin='lower')
    ax.imshow(slice.T, cmap='gray', origin='lower')
    cax = ax.imshow(counts.T, cmap='gray', origin='lower') # camp=plt.cm.hot
    plt.colorbar(cax)
    plt.show()


if __name__ == '__main__':
    import nibabel as nib
    from pyfat.io.load import load_tck
    from CC_extract_tck import extract_cc, extract_multi_node, extract_cc_step
    from node_extract import xmin_extract

    # load data
    data_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
                'response_dhollander/100206/Structure/T1w_acpc_dc_restore_brain.nii.gz'
    img = nib.load(data_path)
    img_data = img.get_data()
    print img.shape
    print img_data
    tck_path = '/home/brain/workingdir/data/dwi/hcp/' \
               'preprocessed/response_dhollander/100206/result/CC_fib_new.tck'

    imgtck = load_tck(tck_path)
    streamstck = imgtck.streamlines
    print len(streamstck)

    # extract cc fib
    imgtck_fib = extract_cc(imgtck)
    # remove multi-node fib
    imgtck_fib = extract_multi_node(imgtck_fib)[0]
    # step > 20
    imgtck_fib = extract_cc_step(imgtck_fib)[0]

    # extract node according to x-value
    Ls_temp = xmin_extract(imgtck_fib)
    print len(Ls_temp)
    # show node density
    show_slice_density(img, Ls_temp)
