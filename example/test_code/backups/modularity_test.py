# !/usr/bin/python
# -*- coding: utf-8 -*-

import os
import numpy as np
import random
import nibabel as nib
import numpy.linalg as npl
from compiler.ast import flatten, flatten_nodes
from nibabel.affines import apply_affine
from sklearn.neighbors import kneighbors_graph

from pyfat.io.load import load_tck
from pyfat.io.save import save_tck
from pyfat.algorithm.node_show import show_dist_matrix
from pyfat.algorithm.fiber_extract import extract_endpoint_dissimilar, extract_multi_node, extract_lr_step, extract_xyz_gradient
from pyfat.algorithm.node_extract import xmin_extract
from pyfat.algorithm.ncut import ncut, discretisation, get_labels
from pyfat.algorithm.node_show import show_2d_node, show_dist_matrix, show_slice_density
from pyfat.algorithm.node_clustering import k_means, hierarchical_clust
from pyfat.algorithm.metric import coordinate_dist

from pyfat.example.bctpy.bct.algorithms.modularity import modularity_finetune_und, modularity_louvain_und


import nibabel.streamlines.array_sequence as nibAS

import matplotlib.pyplot as plt

# load data
data_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
             'response_dhollander/100408/Structure/T1w_acpc_dc_restore_brain.nii.gz'
img = nib.load(data_path)
img_data = img.get_data()
# tck_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
#            'response_dhollander/100408/result/45006old/CC_fib_ncut_set0-1_1.tck'
# tck_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
#        'response_dhollander/100408/result/result20vs45/cc_20fib_step20_new_sample5000.tck'
tck_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/100408/result/result20vs45/cc_20fib_step20_new_correct.tck'

imgtck = load_tck(tck_path)
# streamstck = imgtck.streamlines
# print streamstck

# extract cc fib
# imgtck_fib = extract_cc(imgtck)
# remove multi-node fib
# imgtck_fib = extract_multi_node(imgtck_fib)[0]
# step > 20
# imgtck_fib = extract_cc_step(imgtck_fib)[0]

# extract node according to x-value
Ls_temp = xmin_extract(imgtck)
# print len(Ls_temp)
# show node or density
# show_2d_node(img, Ls_temp)
# show_slice_density(img, Ls_temp)

# k-means
Ls_temp_labels, Ls_temp_centers = k_means(Ls_temp)

# show_2d_node(img, Ls_temp_centers)

# calculate similarity matrix
sdist = coordinate_dist(Ls_temp_centers)
# show_dist_matrix(img, sdist)
# print sdist

# set the similarity matrix
beta = 5
eps = 1e-6
sdist = np.exp(-beta * sdist / sdist.std()) + eps

#show the sdist matrix
# print sdist
# show_dist_matrix(sdist)

modularity = modularity_louvain_und(sdist)
modularity_finetune = modularity_finetune_und(sdist, ci=modularity[0])

label_img = modularity_finetune[0]

# choose fiber according to node clusters
# index
fig, ax = plt.subplots()
slice = img.get_data()[img.shape[0] / 2, :, :]
ax.imshow(slice.T, cmap='gray', origin='lower')
color = plt.cm.spectral(np.linspace(0, 1, len(set(label_img))))

# save the fiber cluster
out_path = '/home/brain/workingdir/data/dwi/hcp/' \
           'preprocessed/response_dhollander/100408/result/' \
           'result20vs45/cc_20fib_step20_new_correct_modularity_set0-1_%s.tck'

for i in set(label_img):
    l = np.argwhere(label_img == i)
    stream = Ls_temp_labels == l
    stream_sum = stream.sum(axis=0)
    stream_temp = stream_sum > 0
    fib_path_index = imgtck.streamlines[stream_temp]
    mid_node_affine = apply_affine(npl.inv(img.affine), Ls_temp[stream_temp])

    ax.plot(np.array(mid_node_affine)[:, 1], np.array(mid_node_affine)[:, 2],
            'o', color=color[i-1])
    save_tck(fib_path_index, imgtck.header, imgtck.tractogram.data_per_streamline,
             imgtck.tractogram.data_per_point, imgtck.tractogram.affine_to_rasmm,
             out_path % i)

plt.show()
