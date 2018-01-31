# !/usr/bin/python
# -*- coding: utf-8 -*-

import nibabel as nib
from pyfat.algorithm.fiber_maths import create_registration_paths, muti_bundle_registration
from pyfat.viz.fiber_simple_viz_advanced import fiber_simple_3d_show_advanced

prepath = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/'
pospath = 'Diffusion/SD/1M_20_01_20dynamic250_SD_Stream_occipital5.tck'
# pospath = '1M_20_01_20dynamic250_SD_Stream_lhemi_occipital5.tck'
# pospath = '1M_20_01_20dynamic250_SD_Stream_rhemi_occipital5.tck'

paths_file = create_registration_paths(prepath, pospath)
print paths_file
fas = muti_bundle_registration(paths_file, 20)
out_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/100610/' \
           'Diffusion/1M_20_01_20dynamic250_SD_Stream_occipital5_all_subjects.tck'
fas.save2tck(out_path)
img = nib.load('/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/'
               '100610/Structure/T1w_acpc_dc_restore_brain1.25.nii.gz')

fiber_simple_3d_show_advanced(img, fas.get_data())
