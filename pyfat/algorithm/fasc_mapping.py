# !/usr/bin/python
# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:l


"""
The module consits of functions which map fasciculus information to brain volume or cortical surface, including,
endpoint mapping,density mapping, midsag plane mapping. 
"""

import nibabel as nib
from scipy.spatial.distance import cdist
import dipy.tracking.utils as ditu
import nibabel.streamlines.array_sequence as nibas

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

def terminus2surface(streamlines, geo_path, scalar_path=None):
    """Points project surface"""
    coords, faces = nib.freesurfer.read_geometry(geo_path)
    scalar_data = nib.freesurfer.read_morph_data(scalar_path)
    s0 = [s[0] for s in streamlines]
    s_t = [s[-1] for s in streamlines]
    s = s0 + s_t
    stream_terminus = nibas.ArraySequence(s)
    y = cdist(stream_terminus, coords)
    nearest_coords = nibas.ArraySequence([coords[y[i].argmin()] for i in range(len(y[:]))])

    return stream_terminus, nearest_coords
