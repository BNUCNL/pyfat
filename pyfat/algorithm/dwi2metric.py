#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import subprocess as sp

prepath = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects/'

pospath_data = 'Diffusion/data/data.nii.gz'
pospath_bvecs = 'Diffusion/data/bvecs'
pospath_bvals = 'Diffusion/data/bvals'
pospath_mask = 'Diffusion/data/nodif_brain_mask.nii.gz'

subjects = os.listdir(prepath)
for sb_id in subjects:
    print sb_id

    data_path = os.path.join(prepath, str(sb_id), pospath_data)
    bvecs_path = os.path.join(prepath, str(sb_id), pospath_bvecs)
    bvals_path = os.path.join(prepath, str(sb_id), pospath_bvals)
    mask_path = os.path.join(prepath, str(sb_id), pospath_mask)

    metrics_dir = os.path.join(prepath, str(sb_id), 'Diffusion/metrics/')
    if not os.path.exists(metrics_dir):
        os.makedirs(metrics_dir)
    adc_path = os.path.join(metrics_dir, 'adc.mif')
    fa_path = os.path.join(metrics_dir, 'fa.mif')
    ad_path = os.path.join(metrics_dir, 'ad.mif')
    rd_path = os.path.join(metrics_dir, 'rd.mif')
    cl_path = os.path.join(metrics_dir, 'cl.mif')
    cp_path = os.path.join(metrics_dir, 'cp.mif')
    cs_path = os.path.join(metrics_dir, 'cs.mif')
    value_path = os.path.join(metrics_dir, 'value.mif')
    vector_path = os.path.join(metrics_dir, 'vector.mif')
    out_metrics = (data_path, bvecs_path, bvals_path, adc_path, fa_path, ad_path, rd_path, cl_path, cp_path, cs_path, value_path, vector_path, mask_path)

    if not os.path.exists(adc_path):
        cmd = "dwi2tensor %s -fslgrad %s %s - | tensor2metric - -adc %s -fa %s -ad %s -rd %s -cl %s -cp %s -cs %s -value %s -vector %s -mask %s"
        sp.call(cmd % out_metrics, shell=True)
