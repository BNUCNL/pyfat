# !/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import nibabel as nib
import numpy.linalg as npl
from nibabel.affines import apply_affine
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import linkage, fcluster

from pyfat.io.load import load_tck
from pyfat.io.save import save_tck
from pyfat.core.dataobject import Fasciculus
from pyfat.algorithm.node_clustering import NodeClustering

import nibabel.streamlines.array_sequence as nibas

import matplotlib.pyplot as plt

# load data
data_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
             'response_dhollander/100408/Structure/T1w_acpc_dc_restore_brain.nii.gz'
img = nib.load(data_path)
img_data = img.get_data()
# tck_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
#        'response_dhollander/100408/result/result20vs45/cc_20fib_step20_new_sample5000.tck'
tck_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/100408/result/result20vs45/cc_20fib_lr1.5_01_new_correct.tck'

imgtck = load_tck(tck_path)
fasciculus = Fasciculus(tck_path)
streamstck = fasciculus.get_data()
# print streamstck

# extract node according to x-value
Ls_temp = fasciculus.xmin_nodes()
print len(Ls_temp)
# show node or density
# show_2d_node(img, Ls_temp)
# show_slice_density(img, Ls_temp)

# knn_graph = kneighbors_graph(Ls_temp, 10, include_self=False)
Ls_temp_labels, Ls_temp_centers = NodeClustering(Ls_temp).k_means()
sdist = pdist(Ls_temp_centers)
knn_graph = linkage(sdist, method='single', metric='euclidean')
print knn_graph

label_img = fcluster(knn_graph, t=2, criterion='distance')
print label_img

# choose fiber according to node clusters
# indexhie
fig, ax = plt.subplots()
slice = img.get_data()[img.shape[0] / 2, :, :]
ax.imshow(slice.T, cmap='gray', origin='lower')
color = plt.cm.spectral(np.linspace(0, 1, len(set(label_img))))

node_clusters = []
fib_clusters = []

for i in set(label_img):
    l = np.argwhere(label_img == i)
    stream = Ls_temp_labels == l
    stream_sum = stream.sum(axis=0)
    stream_temp = stream_sum > 0
    fib_path_index = imgtck.streamlines[stream_temp]
    fib_clusters.append(fib_path_index)
    mid_node_affine = apply_affine(npl.inv(img.affine), Ls_temp[stream_temp])
    node_clusters.append(mid_node_affine)

    ax.plot(mid_node_affine[:, 1], mid_node_affine[:, 2],
            'o', color=color[i-1])
    # save_tck(fib_path_index, imgtck.header, imgtck.tractogram.data_per_streamline,
    #          imgtck.tractogram.data_per_point, imgtck.tractogram.affine_to_rasmm,
    #          out_path % i)

# plt.show()

# extract cc
fig, ax = plt.subplots()
slice = img.get_data()[img.shape[0] / 2, :, :]
ax.imshow(slice.T, cmap='gray', origin='lower')

index = [k[:, 2].max() for k in node_clusters]
index_need = np.array(index).argmax()
ax.plot(node_clusters[index_need][:, 1], node_clusters[index_need][:, 2],
        'o', color='r')

# save_tck(fib_clusters[index_need], imgtck.header, imgtck.tractogram.data_per_streamline,
#          imgtck.tractogram.data_per_point, imgtck.tractogram.affine_to_rasmm,
#          out_path % 'cc_step20')

# plt.show()

fig, ax = plt.subplots()
slice = img.get_data()[img.shape[0] / 2, :, :]
ax.imshow(slice.T, cmap='gray', origin='lower')

clusters_z_mean = [k[:, 2].mean() for k in node_clusters]
clusters_y_mean = [k[:, 1].mean() for k in node_clusters]
index_z = np.array(clusters_z_mean) < 105
index_y = np.array(clusters_y_mean) < 165

remain_clusters = []
remain_fib_clusters = []
for i in range(len(node_clusters)):
    if not index_z[i] or not index_y[i]:
        remain_clusters.append(node_clusters[i])
        remain_fib_clusters.append(fib_clusters[i])

color = plt.cm.spectral(np.linspace(0, 1, len(remain_clusters)))
for index_need in range(len(remain_clusters)):
    ax.plot(remain_clusters[index_need][:, 1], remain_clusters[index_need][:, 2],
            'o', color=color[index_need])

# plt.show()

clusters_z_max = [k[:, 2].max() for k in remain_clusters]

node = np.array(zip(range(len(clusters_z_max)), clusters_z_max))
node_sort = node[np.lexsort(node.T)]
node_total = []
other_node = []
for d in node_sort[2:-1]:
    for n in remain_clusters[int(d[0])]:
        other_node.append(list(n))

print other_node
node_total.append(remain_clusters[int(node_sort[0][0])])
node_total.append(remain_clusters[int(node_sort[1][0])])
if len(other_node) == 0:
    pass
else:
    node_total.append(np.array(other_node))
node_total.append(remain_clusters[int(node_sort[-1][0])])
print node_total[2]

fig, ax = plt.subplots()
slice = img.get_data()[img.shape[0] / 2, :, :]
ax.imshow(slice.T, cmap='gray', origin='lower')
color = plt.cm.spectral(np.linspace(0, 1, len(node_total)))
for index in range(len(node_total)):
    ax.plot(node_total[index][:, 1], node_total[index][:, 2],
            'o', color=color[index])

# plt.show()

fib_total = []
other = nibas.ArraySequence()
for d in node_sort[2:-1]:
    for f in remain_fib_clusters[int(d[0])]:
        other.append(f)

fib_total.append(remain_fib_clusters[int(node_sort[0][0])])
fib_total.append(remain_fib_clusters[int(node_sort[1][0])])
if len(other) == 0:
    pass
else:
    fib_total.append(other)
fib_total.append(remain_fib_clusters[int(node_sort[-1][0])])

out_path = '/home/brain/workingdir/data/dwi/hcp/' \
           'preprocessed/response_dhollander/100408/result/' \
           'result20vs45/cc_20fib_lr1.5_01_new_hierarchical_single_%s.tck'
spe_name_four = ['oc', 'ac', 'other', 'cc']
spe_name_three = ['oc', 'ac', 'cc']
for fi in range(len(fib_total)):
    if len(fib_total) == 4:
        save_tck(fib_total[fi], imgtck.header, imgtck.tractogram.data_per_streamline,
                 imgtck.tractogram.data_per_point, imgtck.tractogram.affine_to_rasmm,
                 out_path % spe_name_four[fi])
    if len(fib_total) == 3:
        save_tck(fib_total[fi], imgtck.header, imgtck.tractogram.data_per_streamline,
                 imgtck.tractogram.data_per_point, imgtck.tractogram.affine_to_rasmm,
                 out_path % spe_name_three[fi])

plt.show()
