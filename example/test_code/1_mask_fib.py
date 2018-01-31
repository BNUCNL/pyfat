# !/usr/bin/python
# -*- coding: utf-8 -*-

import nibabel as nib
import numpy as np
from scipy.spatial.distance import cdist
from pyfat.core.dataobject import Fasciculus
from surfer import Brain
from mayavi import mlab

# load left hemisphere mask and geometry data
# roi_surf_path_l = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
#                   'response_dhollander/996782/996782/label/lh.aparc.annot'
# geo_path_l = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
#              'response_dhollander/996782/Native/996782.L.white.native.surf.gii'
#
# load right hemisphere mask and geometry data
roi_surf_path_r = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
                  'response_dhollander/996782/996782/label/rh.aparc.annot'
geo_path_r = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
             'response_dhollander/996782/Native/996782.R.white.native.surf.gii'

# choose the mask: Occipital
vertices, colortable, label = nib.freesurfer.read_annot(roi_surf_path_r)
gii_data = nib.load(geo_path_r).darrays
coords, faces = gii_data[0].data, gii_data[1].data

l_label_value = np.array(len(coords) * [0])
l_label_value[vertices == 11] = 11  # lateraloccipital
l_label_value[vertices == 13] = 13  # lingual
l_label_value[vertices == 5] = 5  # cuneus
l_label_value[vertices == 21] = 21  # pericalcarine


# # show mask on surface
# subject_id = "101107"
# subjects_dir = "/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/101107"
# hemi = 'lh'
# surf = 'white'
# alpha = 1
# brain = Brain(subjects_dir=subjects_dir, subject_id=subject_id, hemi=hemi, surf=surf, alpha=alpha)
# brain.add_overlay(l_label_value, min=l_label_value[l_label_value > 0].min(),
#                   max=l_label_value.max(), sign='pos', hemi='lh', name='lh')
#
# mlab.show()


# extract fib using mask
tck_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/996782/Diffusion/SD/1M_20_01_20dynamic250_SD_Stream_rh.tck'

fasciculus = Fasciculus(tck_path)
streamlines = fasciculus.get_data()
print len(streamlines)
streamlines = fasciculus.sort_streamlines()

# if lh
# s0 = [s[0] for s in streamlines]

# if rh
s0 = [s[-1] for s in streamlines]

stream_terminus_lh = np.array(s0)
dist_lh = cdist(coords[l_label_value > 0], stream_terminus_lh)
lh_stream_index = np.array(len(streamlines) * [False])
for i in range(len(dist_lh[:])):
    temp_index = np.array(dist_lh[i] <= 5)
    lh_stream_index += temp_index

lh_rois_streamlines = streamlines[lh_stream_index]
fasciculus.set_data(lh_rois_streamlines)

# save extracted fib
out_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/996782/Diffusion/SD/1M_20_01_20dynamic250_SD_Stream_rh_occipital5.tck'
fasciculus.save2tck(out_path)
