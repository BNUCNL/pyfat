# !/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import nibabel as nib
import numpy.linalg as npl
from nibabel.affines import apply_affine

from pyfat.io.load import load_tck
from pyfat.io.save import save_tck
from CC_extract_tck import extract_cc, extract_multi_node, extract_cc_step
from node_extract import xmin_extract
from ncut import ncut, discretisation, get_labels
from node_show import show_2d_node, show_dist_matrix, show_slice_density
from metric import coordinate_dist

import nibabel.streamlines.array_sequence as nibAS

import matplotlib.pyplot as plt

# load data
data_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
             'response_dhollander/100206/Structure/T1w_acpc_dc_restore_brain.nii.gz'
img = nib.load(data_path)
img_data = img.get_data()
print img.shape
print img_data
# tck_path = '/home/brain/workingdir/data/dwi/hcp/' \
#            'preprocessed/response_dhollander/100206/result/CC_fib_new.tck'
tck_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
       'response_dhollander/100206/Diffusion/100k_sift_1M45006_dynamic250.tck'

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
# show node or density
show_2d_node(img, Ls_temp)
show_slice_density(img, Ls_temp)

# calculate similarity matrix
sdist = coordinate_dist(Ls_temp)
print sdist

# set the correlation matrix
thre0 = sdist > 4.6
sdist[thre0] = 0
thre1 = sdist > 0
# sdist[thre1] = sdist[thre1] / sdist[thre1].max()
# sdist[thre1] = 1 - sdist[thre1]
sdist[thre1] = 1
print sdist

# show the sdist matrix
# show_dist_matrix(sdist)

# ncut according to coordinate
eigen_val, eigen_vec = ncut(sdist, 4)
eigenvec_discrete = discretisation(eigen_vec)
print eigenvec_discrete

# get labels
label_img = get_labels(eigenvec_discrete)

print label_img

# choose fiber according to node clusters
d = zip(label_img, Ls_temp)
L_temp_0 = nibAS.ArraySequence()
L_temp_1 = nibAS.ArraySequence()
L_temp_2 = nibAS.ArraySequence()
L_temp_3 = nibAS.ArraySequence()
L_temp0 = []
L_temp1 = []
L_temp2 = []
L_temp3 = []

for k in range(len(d)):
    if d[k][0] == 0:
        L_temp_0.append(imgtck.streamlines[k])
        L_temp0.append(d[k][1])
    if d[k][0] == 1:
        L_temp_1.append(imgtck.streamlines[k])
        L_temp1.append(d[k][1])
    if d[k][0] == 2:
        L_temp_2.append(imgtck.streamlines[k])
        L_temp2.append(d[k][1])
    if d[k][0] == 3:
        L_temp_3.append(imgtck.streamlines[k])
        L_temp3.append(d[k][1])

# show node clusters
fig, ax = plt.subplots()
slice = img.get_data()[img.shape[0] / 2, :, :]
ax.imshow(slice.T, cmap='gray', origin='lower')
L_temp0 = apply_affine(npl.inv(img.affine), L_temp0)
L_temp1 = apply_affine(npl.inv(img.affine), L_temp1)
L_temp2 = apply_affine(npl.inv(img.affine), L_temp2)
L_temp3 = apply_affine(npl.inv(img.affine), L_temp3)
ax.plot(np.array(L_temp0)[:, 1], np.array(L_temp0)[:, 2], 'o', color='r')
ax.plot(np.array(L_temp1)[:, 1], np.array(L_temp1)[:, 2], 'o', color='b')
ax.plot(np.array(L_temp2)[:, 1], np.array(L_temp2)[:, 2], 'o', color='g')
ax.plot(np.array(L_temp3)[:, 1], np.array(L_temp3)[:, 2], 'o', color='c')
plt.show()

# save the fiber cluster
out_path = '/home/brain/workingdir/data/dwi/hcp/' \
           'preprocessed/response_dhollander/100206/result/CC_fib_ncut_new_set0-1_0.tck'
out_path1 = '/home/brain/workingdir/data/dwi/hcp/' \
            'preprocessed/response_dhollander/100206/result/CC_fib_ncut_new_set0-1_1.tck'
out_path2 = '/home/brain/workingdir/data/dwi/hcp/' \
            'preprocessed/response_dhollander/100206/result/CC_fib_ncut_new_set0-1_2.tck'
out_path3 = '/home/brain/workingdir/data/dwi/hcp/' \
            'preprocessed/response_dhollander/100206/result/CC_fib_ncut_new_set0-1_3.tck'

save_tck(L_temp_0, imgtck.header, imgtck.tractogram.data_per_streamline,
         imgtck.tractogram.data_per_point, imgtck.tractogram.affine_to_rasmm, out_path)
save_tck(L_temp_1, imgtck.header, imgtck.tractogram.data_per_streamline,
         imgtck.tractogram.data_per_point, imgtck.tractogram.affine_to_rasmm, out_path1)
save_tck(L_temp_2, imgtck.header, imgtck.tractogram.data_per_streamline,
         imgtck.tractogram.data_per_point, imgtck.tractogram.affine_to_rasmm, out_path2)
save_tck(L_temp_3, imgtck.header, imgtck.tractogram.data_per_streamline,
         imgtck.tractogram.data_per_point, imgtck.tractogram.affine_to_rasmm, out_path3)
