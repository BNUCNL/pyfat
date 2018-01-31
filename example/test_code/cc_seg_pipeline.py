# !/usr/bin/python
# -*- coding: utf-8 -*-

import gc
import nibabel as nib
import numpy as np
from scipy.spatial.distance import cdist
from pyfat.core.dataobject import Fasciculus
from pyfat.algorithm.fiber_extract import FibSelection


def cc_seg_pipeline(tck_path, mask, geo_path, thr=5., volume_path=None, step=0):
    # load data
    fasciculus = Fasciculus(tck_path)

    # extract streamlines from left to right hemisphere
    fibselection = FibSelection(fasciculus)
    L_temp_need0 = fibselection.endpoint_dissimilarity()
    fasciculus.set_data(L_temp_need0)
    L_temp_need1 = fibselection.single_point_mid_sag()
    fasciculus.set_data(L_temp_need1)
    del L_temp_need0, L_temp_need1
    gc.collect()

    # separation of lr_seed fib
    fib = fasciculus.hemi_fib_separation()

    # choose the mask: Occipital
    mask_fib = []
    for i in range(len(fib)):
        vertices, colortable, label = nib.freesurfer.read_annot(mask[i])
        gii_data = nib.load(geo_path[i]).darrays
        coords, faces = gii_data[0].data, gii_data[1].data

        label_value = np.array(len(coords) * [0])
        label_value[vertices == 11] = 11  # lateraloccipital
        label_value[vertices == 13] = 13  # lingual
        label_value[vertices == 5] = 5  # cuneus
        label_value[vertices == 21] = 21  # pericalcarine

        # extract fib using mask
        streamlines = fib[i]
        streamlines = fasciculus.sort_streamlines(streamlines)

        if i == 0:
            s0 = [s[0] for s in streamlines]
        else:
            s0 = [s[-1] for s in streamlines]

        stream_terminus = np.array(s0)
        dist = cdist(coords[label_value > 0], stream_terminus)
        stream_index = np.array(len(streamlines) * [False])
        for j in range(len(dist[:])):
            temp_index = np.array(dist[j] <= thr)
            stream_index += temp_index

        rois_streamlines = streamlines[stream_index]
        mask_fib.append(rois_streamlines)

    # lr fib merge
    fib_merge = fasciculus.fib_merge(mask_fib[0], mask_fib[1])
    del mask_fib
    gc.collect()
    fib_hemi = fasciculus.separation_fib_to_hemi(fib_merge)
    del fib_merge
    gc.collect()

    return fib_hemi

if __name__ == '__main__':
    tck_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
               'response_dhollander/100307/Diffusion/SD/1M_20_01_20dynamic250_SD_Stream.tck'
    fasciculus = Fasciculus(tck_path)
    # load left hemisphere mask and geometry data
    roi_surf_path_l = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
                      'response_dhollander/100307/100307/label/lh.aparc.annot'
    geo_path_l = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
                 'response_dhollander/100307/Native/100307.L.white.native.surf.gii'

    # load right hemisphere mask and geometry data
    roi_surf_path_r = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
                      'response_dhollander/100307/100307/label/rh.aparc.annot'
    geo_path_r = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
                 'response_dhollander/100307/Native/100307.R.white.native.surf.gii'
    mask = [roi_surf_path_l, roi_surf_path_r]
    geo_path = [geo_path_l, geo_path_r]
    fib_hemi = cc_seg_pipeline(tck_path, mask, geo_path)

    out_hemi_lh_fib = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
                      'response_dhollander/100307/Diffusion/1M_20_01_20dynamic250_SD_Stream_lhemi_occipital5_test.tck'
    out_hemi_rh_fib = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
                      'response_dhollander/100307/Diffusion/1M_20_01_20dynamic250_SD_Stream_rhemi_occipital5_test.tck'
    fasciculus.set_data(fib_hemi[0])
    fasciculus.save2tck(out_hemi_lh_fib)
    fasciculus.set_data(fib_hemi[1])
    fasciculus.save2tck(out_hemi_rh_fib)
