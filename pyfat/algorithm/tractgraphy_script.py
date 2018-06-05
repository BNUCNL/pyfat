#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
5ttgen fsl T1w_acpc_dc_restore_brain1.25.nii.gz 5TT.mif -premasked
mrconvert data.nii.gz DWI.mif -fslgrad bvecs bvals -datatype float32 -stride 0,0,0,1
dwiextract DWI.mif - -bzero | mrmath - mean mean0.mif -axis 3
dwi2response dhollander DWI.mif RF_WM.txt RF_GM.txt RF_CSF.txt -voxels RF_voxels.mif
dwi2fod msmt_csd DWI.mif RF_WM.txt WM_FODs.mif RF_GM.txt GM.mif RF_CSF.txt CSF.mif -mask nodif_brain_mask.nii.gz
tckgen WM_FODs.mif 1M_20_01_20dynamic250_SD_Stream.tck -algorithm SD_Stream -act 5TT.mif -crop_at_gmwmi -seed_dynamic WM_FODs.mif -angle 20 -minlength 20 -maxlength 250 -select 1M -cutoff 0.1
"""

import os
import subprocess as sp


# fsl_path = os.environ.get('FSLDIR')
# first_atlas_path = os.path.join(fsl_path, 'data', 'first', 'models_336_bin')
# print os.path.exists(first_atlas_path)

prepath = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects/'

pospath_data = 'Diffusion/data/data.nii.gz'
pospath_T1w = 'T1w/T1w_acpc_dc_restore_brain1.25.nii.gz'
pospath_bvecs = 'Diffusion/data/bvecs'
pospath_bvals = 'Diffusion/data/bvals'
pospath_mask = 'Diffusion/data/nodif_brain_mask.nii.gz'
subjects = os.listdir(prepath)
for sb_id in subjects:
    print sb_id
    data_path = os.path.join(prepath, str(sb_id), pospath_data)
    T1w_path = os.path.join(prepath, str(sb_id), pospath_T1w)
    bvecs_path = os.path.join(prepath, str(sb_id), pospath_bvecs)
    bvals_path = os.path.join(prepath, str(sb_id), pospath_bvals)
    mask_path = os.path.join(prepath, str(sb_id), pospath_mask)

    data_dir = os.path.split(data_path)[0]

    act_flag = os.path.join(data_dir, '5TT.mif')
    if not os.path.exists(act_flag):
        cmd = "5ttgen fsl %s %s -premasked"
        sp.call(cmd % (T1w_path, act_flag), shell=True)

    dwi_flag = os.path.join(data_dir, 'DWI.mif')
    if not os.path.exists(dwi_flag):
        cmd = "mrconvert %s %s -fslgrad %s %s -datatype float32 -stride 0,0,0,1"
        sp.call(cmd % (data_path, dwi_flag, bvecs_path, bvals_path), shell=True)

    mean_b0 = os.path.join(data_dir, 'mean0.mif')
    if not os.path.exists(mean_b0):
        cmd = 'dwiextract %s - -bzero | mrmath - mean %s -axis 3'
        sp.call(cmd % (dwi_flag, mean_b0), shell=True)

    response_flag = os.path.join(data_dir, 'RF_WM.txt')
    if not os.path.exists(response_flag):
        global p_rf_gm, p_rf_csf
        p_rf_gm = os.path.join(data_dir, 'RF_GM.txt')
        p_rf_csf = os.path.join(data_dir, 'RF_CSF.txt')
        p_rf_voxels = os.path.join(data_dir, 'RF_voxels.mif')
        cmd = 'dwi2response dhollander %s %s %s %s -voxels %s'
        sp.call(cmd % (dwi_flag, response_flag, p_rf_gm, p_rf_csf, p_rf_voxels), shell=True)

    fod_flag = os.path.join(data_dir, 'WM_FODs.mif')
    if not os.path.exists(fod_flag):
        p_fod_gm = os.path.join(data_dir, 'GM.mif')
        p_fod_csf = os.path.join(data_dir, 'CSF.mif')
        cmd = 'dwi2fod msmt_csd %s %s %s %s %s %s %s -mask %s'
        sp.call(cmd % (dwi_flag, response_flag, fod_flag, p_rf_gm, p_fod_gm, p_rf_csf, p_fod_csf, mask_path), shell=True)

    tck_flag = os.path.join(prepath, str(sb_id), 'Diffusion/SD/1M_20_01_20dynamic250_SD_Stream.tck')
    if not os.path.exists(tck_flag):
        sd_dir = os.path.split(tck_flag)[0]
        os.makedirs(sd_dir)
        cmd = 'tckgen %s %s -algorithm SD_Stream -act %s -crop_at_gmwmi -seed_dynamic %s -angle 20 -minlength 20 -maxlength 250 -select 1M -cutoff 0.1'
        sp.call(cmd % (fod_flag, tck_flag, act_flag, fod_flag), shell=True)
