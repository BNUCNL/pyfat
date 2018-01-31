# !/usr/bin/python
# -*- coding: utf-8 -*-

import nibabel as nib
from pyfat.io.save import save_nifti
from pyfat.algorithm.vol_maths import voll_volr_merge, vold_volv_merge, vold_volv_mpm, vol_mask_vol, make_mpm

# lh_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
#            'response_dhollander/ProbAtlas_v4/subj_vol_all/mpm_lh.nii.gz'
# rh_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
#            'response_dhollander/ProbAtlas_v4/subj_vol_all/mpm_rh.nii.gz'
# out_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
#            'response_dhollander/100408/Structure/native_mpm_lrh_thr10.nii.gz'

# img = nib.load(lh_path)
# data = voll_volr_merge(lh_path, rh_path)
# save_nifti(data, img.affine, out_path)


# volume = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/100408/Structure/T1w_short.nii.gz'
# ccseg_v = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/100408/Structure/ccseg_v_merge.nii.gz'
# ccseg_v_out = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/100408/Structure/ccseg_v_merge_mpm.nii.gz'
# ccseg_d_out = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/100408/Structure/ccseg_d_merge_mpm.nii.gz'
# ccseg_d = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/100408/Structure/ccseg_d_merge.nii.gz'
# # data_d_v = vold_volv_merge(ccseg_d, ccseg_v)
# img = nib.load(volume)
#
# data_d_v_mpm = vold_volv_mpm(ccseg_d, ccseg_v)
# save_nifti(data_d_v_mpm[0], img.affine, ccseg_d_out)
# save_nifti(data_d_v_mpm[1], img.affine, ccseg_v_out)

vol = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
      'response_dhollander/996782/Structure/T1w_acpc_dc_restore_1.25.nii.gz'
mask = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
       'response_dhollander/996782/Diffusion/data/nodif_brain_mask.nii.gz'
out_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/996782/Structure/T1w_acpc_dc_restore_brain1.25.nii.gz'

img = nib.load(vol)
data = vol_mask_vol(vol, mask)
save_nifti(data, img.affine, out_path, 'float32')

# vol = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/101107/lab_map/pm_rh.nii.gz'
# out_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/101107/lab_map/mpm_rh.nii.gz'
#
# img = nib.load(vol)
# data = make_mpm(img.get_data(), 0)
# save_nifti(data, img.affine, out_path, 'float32')

# source_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
#               'response_dhollander/101107/lab_map/native1.25_wang_maxprob_vol_rh_mask.nii.gz'
# img = nib.load(source_path)
# data = img.get_data()
# data[data > 6] = 0
# out_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
#            'response_dhollander/101107/lab_map/native1.25_wang_maxprob_vol_rh_mask_vis.nii.gz'
# save_nifti(data, img.affine, out_path, 'float32')
