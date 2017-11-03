# !/usr/bin/python
# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:l


"""
The module consits of functions which map fasciculus information to brain volume or cortical surface, including,
endpoint mapping,density mapping, midsag plane mapping. 
"""

import nibabel as nib
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

