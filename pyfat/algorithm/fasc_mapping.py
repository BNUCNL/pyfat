# !/usr/bin/python
# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:l


"""
The module consits of functions which map fasciculus information to brain volume or cortical surface, including,
endpoint mapping,density mapping, midsag plane mapping. 
"""

import nibabel as nib
import numpy as np
from scipy.spatial.distance import cdist
import dipy.tracking.utils as ditu

# fiber density of volume
def fib_density_map(volume, fiber, output_path):
    """
    fiber to volume density map
    Parameters
    ----------
    volume : nifti img
        nifti img
    fiber : ArraySequence streamlines
        streamlines
    output : output path
            output path nii.gz

    Return
    ------
    output file nii.gz
    """
    shape = volume.shape
    affine = volume.affine
    streamlines = fiber
    voxel_size = nib.affine.voxel_size(affine)
    image_volume = ditu.density_map(streamlines, vol_dims=shape, voxel_size=voxel_size, affine=affine)

    dm_img = nib.Nifti1Image(image_volume.astype("int16"), affine)
    dm_img.to_filename(output_path)

def terminus2surface(streamlines, geo_path):
    """Points project surface"""
    coords, faces = nib.freesurfer.read_geometry(geo_path)
    s0 = [s[0] for s in streamlines]
    s_t = [s[-1] for s in streamlines]
    s = s0 + s_t

    stream_terminus = np.array(s)
    dist = cdist(stream_terminus, coords)
    nearest_vert = np.array([dist[i].argmin() for i in range(len(dist[:]))])

    stream_terminus_lh = stream_terminus[stream_terminus[:, 0] < 0]
    dist_lh = cdist(stream_terminus_lh, coords)
    nearest_vert_lh = np.array([dist_lh[i].argmin() for i in range(len(dist_lh[:]))])

    stream_terminus_rh = stream_terminus[stream_terminus[:, 0] < 0]
    dist_rh = cdist(stream_terminus_rh, coords)
    nearest_vert_rh = np.array([dist_rh[i].argmin() for i in range(len(dist_rh[:]))])
    # print len(nearest_vert_lh), len(nearest_vert_rh)

    return nearest_vert, nearest_vert_lh, nearest_vert_rh
