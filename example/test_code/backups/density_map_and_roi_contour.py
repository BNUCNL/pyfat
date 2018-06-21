# !/usr/bin/python
# -*- coding: utf-8 -*-

import glob
from pyfat.io.load import load_tck
from pyfat.algorithm.roi_vol_surf import label2surf_roi
from pyfat.algorithm.fasc_mapping import terminus2surface_map
from pyfat.viz.surfaceview import surface_streamlines_map, surface_roi_contour

lh_white = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/100408/Native/100408.L.white.native.surf.gii'
rh_white = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/100408/Native/100408.R.white.native.surf.gii'
geo_path = [lh_white, rh_white]

l_labels = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/100408/my_labels/native/native_lh_FFA.label'
r_labels = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/100408/my_labels/native_rh_FFA.label'
lr_labels_path = [l_labels, r_labels]
lr_label = label2surf_roi(lr_labels_path, geo_path)

subject_id = "100408"
subjects_dir = "/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/100408"
hemi = 'both'
surf = 'inflated'
alpha = 1

prefix = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
         'response_dhollander/100408/result/463_clusters/clusters'
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
    files = [prefix + '_' + str(x) + '.tck' for x in index]

for f in files[23:]:
    streamlines = load_tck(f).streamlines
    vertex = terminus2surface_map(streamlines, geo_path)
    surface_roi_contour(subjects_dir, subject_id, hemi, surf, alpha, vertex, lr_label)
    # surface_streamlines_map(subjects_dir, subject_id, hemi, surf, alpha, vertex)
