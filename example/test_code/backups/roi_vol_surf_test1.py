# !/usr/bin/python
# -*- coding: utf-8 -*-

import nibabel as nib
from pyfat.algorithm.roi_vol_surf import roi_surf2vol
from pyfat.io.save import save_nifti


roi_surf_path_l = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
                  'response_dhollander/101107/101107/label/lh.aparc.annot'
roi_surf_path_r = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
                  'response_dhollander/101107/101107/label/rh.aparc.annot'
geo_path_l = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
             'response_dhollander/101107/Native/101107.L.white.native.surf.gii'
geo_path_r = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
             'response_dhollander/101107/Native/101107.R.white.native.surf.gii'
vol_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/101107/Structure/T1w_acpc_dc_restore_brain1.25.nii.gz'

img = nib.load(vol_path)

data = roi_surf2vol(roi_surf_path_r, geo_path_r, vol_path)
out_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/101107/Structure/rh_labels.nii.gz'
save_nifti(data, img.affine, out_path)
