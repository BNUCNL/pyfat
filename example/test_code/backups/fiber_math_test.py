# !/usr/bin/python
# -*- coding: utf-8 -*-

import os
import nibabel as nib
from pyfat.core.dataobject import Fasciculus
from pyfat.algorithm.fiber_maths import create_registration_paths, bundle_registration, muti_bundle_registration
from pyfat.viz.fiber_simple_viz_advanced import fiber_simple_3d_show_advanced

prepath = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/'
pospath = 'Diffusion/SD/1M_20_01_20dynamic250_SD_Stream_occipital5.tck'
# pospath = '1M_20_01_20dynamic250_SD_Stream_lhemi_occipital5.tck'
# pospath = '1M_20_01_20dynamic250_SD_Stream_rhemi_occipital5.tck'

paths_file = create_registration_paths(prepath, pospath)
print paths_file
# fas = muti_bundle_registration(paths_file, 20)
# out_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/100610/' \
#            'Diffusion/1M_20_01_20dynamic250_SD_Stream_occipital5_all_subjects.tck'
# fas.save2tck(out_path)
# img = nib.load('/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/'
#                '100610/Structure/T1w_acpc_dc_restore_brain1.25.nii.gz')
#
# fiber_simple_3d_show_advanced(img, fas.get_data())

fas = Fasciculus(paths_file[0])
stream = fas.get_data()
out_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/subjects_all/Diffusion/1M_20_01_20dynamic250_SD_Stream_occipital5_%s_aligned.tck'
for path in paths_file:
    subject_id = path.split('/')[9]
    print subject_id
    aligned = bundle_registration(stream, Fasciculus(path).get_data(), 20)
    fas.save2tck(out_path % subject_id)


