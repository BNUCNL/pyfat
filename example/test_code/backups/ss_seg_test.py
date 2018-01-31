# !/usr/bin/python
# -*- coding: utf-8 -*-
import nibabel as nib
from pyfat.algorithm.cc_seg import cc_seg_region, cc_seg_regions, cc_seg_same_regions

if __name__ == '__main__':
    from pyfat.io.save import save_nifti
    data_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
                'response_dhollander/100408/Structure/T1w_short.nii.gz'
    # s = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/100408/result/ROIs_fibs/hcp_dorsal_vis'
    out_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/100408/Structure/hcp_VanEssen_Atlas/ccseg_VMV3_rh.nii.gz'
    img = nib.load(data_path)
    # data = cc_seg_regions(data_path, s)
    # save_nifti(data, img.affine, out_path)

    # pre_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/100408/result/ROIs_fibs/dorsal_vis'
    # out_paths = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/100408/Structure/ccsegs_dorsal.nii.gz'
    # datas = cc_seg_region(data_path, pre_path)
    # save_nifti(datas, img.affine, out_paths)

    roi_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
               'response_dhollander/100408/result/ROIs_fibs/hcp_VanEssen_Atlas/VMV3/rh/'
    data = cc_seg_same_regions(data_path, roi_path)
    save_nifti(data, img.affine, out_path)
