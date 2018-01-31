# !/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import time
import nibabel as nib
import numpy.linalg as npl
from scipy.sparse.csr import csr_matrix
from compiler.ast import flatten, flatten_nodes
from nibabel.affines import apply_affine
from sklearn.neighbors import kneighbors_graph, BallTree
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import linkage

from pyfat.io.load import load_tck
from pyfat.io.save import save_tck
from pyfat.algorithm.fiber_extract import extract_endpoint_dissimilar, extract_multi_node, extract_lr_step, extract_xyz_gradient
from pyfat.algorithm.node_extract import xmin_extract
from pyfat.algorithm.ncut import ncut, discretisation, get_labels
from pyfat.algorithm.node_show import show_2d_node, show_dist_matrix, show_slice_density
from pyfat.algorithm.node_clustering import k_means, hierarchical_clust
from pyfat.algorithm.metric import coordinate_dist

import nibabel.streamlines.array_sequence as nibAS

import matplotlib.pyplot as plt

# load data
data_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
             'response_dhollander/100408/Structure/T1w_acpc_dc_restore_brain.nii.gz'
img = nib.load(data_path)
img_data = img.get_data()
# tck_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
#            'response_dhollander/100408/result/45006old/CC_fib_ncut_set0-1_1.tck'
tck_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
       'response_dhollander/100408/result/result20vs45/cc_20fib_step20_new_sample5000.tck'
# tck_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
#            'response_dhollander/100408/result/result20vs45/cc_20fib_step20_new_correct.tck'

imgtck = load_tck(tck_path)
streamstck = imgtck.streamlines
print streamstck

# extract cc fib
# imgtck_fib = extract_cc(imgtck)
# remove multi-node fib
# imgtck_fib = extract_multi_node(imgtck_fib)[0]
# step > 20
# imgtck_fib = extract_cc_step(imgtck_fib)[0]

# extract node according to x-value
Ls_temp = xmin_extract(imgtck)
Ls_temp = apply_affine(npl.inv(img.affine), Ls_temp)
print len(Ls_temp)
print Ls_temp.shape
# show node or density
# show_2d_node(img, Ls_temp)
# show_slice_density(img, Ls_temp)

# knn_graph = kneighbors_graph(Ls_temp, 10, include_self=False)
Ls_temp_labels, Ls_temp_centers = k_means(Ls_temp, n_clusters=100)
sdist = coordinate_dist(Ls_temp_centers)
sdist[sdist > 2.0] = 0
sdist[sdist > 0.0] = 1
knn_graph = csr_matrix(sdist)
# tree = BallTree(Ls_temp)
# knn_graph, dist = tree.query_radius(Ls_temp[0], r=3)
# knn_graph = linkage(sdist, method='single', metric='euclidean')
print knn_graph.shape
print knn_graph

for connectivity in (None, knn_graph):
    for n_clusters in (10, 5):
        plt.figure(figsize=(10, 4))
        slice = img.get_data()[img.shape[0] / 2, :, :]
        plt.imshow(slice.T, cmap='gray', origin='lower')
        for index, linkage in enumerate(('average', 'complete', 'ward')):
            plt.subplot(1, 3, index + 1)
            model = AgglomerativeClustering(linkage=linkage,
                                            connectivity=connectivity,
                                            n_clusters=n_clusters)
            t0 = time.time()
            model.fit(Ls_temp)
            elapsed_time = time.time() - t0
            plt.scatter(Ls_temp[:, 1], Ls_temp[:, 2], c=model.labels_,
                        cmap=plt.cm.spectral)
            plt.title('linkage=%s (time %.2fs)' % (linkage, elapsed_time),
                      fontdict=dict(verticalalignment='top'))
            plt.axis('equal')
            plt.axis('off')

            plt.subplots_adjust(bottom=0, top=.89, wspace=0,
                                left=0, right=1)
            plt.suptitle('n_cluster=%i, connectivity=%r' %
                         (n_clusters, connectivity is not None), size=17)


plt.show()
