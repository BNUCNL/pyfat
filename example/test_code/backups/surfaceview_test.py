# !/usr/bin/python
# -*- coding: utf-8 -*-

import nibabel as nib
import numpy as np
from scipy.spatial.distance import cdist
from pyfat.core.dataobject import Fasciculus
from pyfat.algorithm.roi_vol_surf import roi_surf2vol
from pyfat.io.save import save_nifti
from surfer import Brain
from mayavi import mlab


roi_surf_path_l = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
                  'response_dhollander/101107/101107/label/lh.aparc.annot'
# roi_surf_path_r = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
#                   'response_dhollander/101107/101107/label/rh.aparc.annot'
geo_path_l = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
             'response_dhollander/101107/Native/101107.L.white.native.surf.gii'
# geo_path_r = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
#              'response_dhollander/101107/Native/101107.R.white.native.surf.gii'
vol_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/101107/Structure/T1w_acpc_dc_restore_brain1.25.nii.gz'

vertices, colortable, label = nib.freesurfer.read_annot(roi_surf_path_l)
gii_data = nib.load(geo_path_l).darrays
coords, faces = gii_data[0].data, gii_data[1].data

l_label_value = np.array(len(coords) * [0])
l_label_value[vertices == 11] = 11
l_label_value[vertices == 13] = 13
l_label_value[vertices == 5] = 5
l_label_value[vertices == 21] = 21

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

tck_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/101107/Diffusion/1M_20_01_20dynamic250_SD_Stream_single.tck'

fasciculus = Fasciculus(tck_path)
streamlines = fasciculus.get_data()
print len(streamlines)
streamlines = fasciculus.sort_streamlines()
s0 = [s[0] for s in streamlines]
stream_terminus_lh = np.array(s0)
dist_lh = cdist(coords[l_label_value > 0], stream_terminus_lh)
lh_stream_index = np.array(len(streamlines) * [False])
for i in range(len(dist_lh[:])):
    temp_index = np.array(dist_lh[i] <= 3)
    lh_stream_index += temp_index

lh_rois_streamlines = streamlines[lh_stream_index]
fasciculus.set_data(lh_rois_streamlines)
out_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/101107/Diffusion/1M_20_01_20dynamic250_SD_Stream_lh_occipital3.tck'
fasciculus.save2tck(out_path)
