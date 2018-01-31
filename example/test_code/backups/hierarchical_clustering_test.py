# !/usr/bin/python
# -*- coding: utf-8 -*-

from pyfat.io.load import load_tck
from pyfat.io.save import save_tck
from pyfat.algorithm.node_extract import xmin_extract
from pyfat.algorithm.hierarchical_clustering import hierarchical_clust
import nibabel.streamlines.array_sequence as nibAS
from sklearn.neighbors import kneighbors_graph


input_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
                'response_dhollander/100206/result/CC_fib.tck'
img_cc = load_tck(input_path)
Ls_temp = xmin_extract(img_cc)
# connectivity = kneighbors_graph(Ls_temp, n_neighbors=10, mode='connectivity', include_self=True)
# connectivity = kneighbors_graph(Ls_temp, n_neighbors=10, include_self=False)
labels = hierarchical_clust(Ls_temp, 4, linkage='complete')
print len(labels)
d = zip(labels, Ls_temp)

L_temp_0 = nibAS.ArraySequence()
L_temp_1 = nibAS.ArraySequence()
L_temp_2 = nibAS.ArraySequence()
L_temp_3 = nibAS.ArraySequence()

for k in range(len(d)):
    if d[k][0] == 0:
        L_temp_0.append(img_cc.streamlines[k])
    if d[k][0] == 1:
        L_temp_1.append(img_cc.streamlines[k])
    if d[k][0] == 2:
        L_temp_2.append(img_cc.streamlines[k])
    if d[k][0] == 3:
        L_temp_3.append(img_cc.streamlines[k])

out_put = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/100206/result/CC_fib_only3_0.tck'
out_put1 = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/100206/result/CC_fib_only3_1.tck'
out_put2 = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/100206/result/CC_fib_only3_2.tck'
out_put3 = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/100206/result/CC_fib_only3_3.tck'
save_tck(L_temp_0, img_cc.header, img_cc.tractogram.data_per_streamline, img_cc.tractogram.data_per_point,
            img_cc.tractogram.affine_to_rasmm, out_put)
save_tck(L_temp_1, img_cc.header, img_cc.tractogram.data_per_streamline, img_cc.tractogram.data_per_point,
            img_cc.tractogram.affine_to_rasmm, out_put1)
save_tck(L_temp_2, img_cc.header, img_cc.tractogram.data_per_streamline, img_cc.tractogram.data_per_point,
            img_cc.tractogram.affine_to_rasmm, out_put2)
save_tck(L_temp_3, img_cc.header, img_cc.tractogram.data_per_streamline, img_cc.tractogram.data_per_point,
            img_cc.tractogram.affine_to_rasmm, out_put3)
