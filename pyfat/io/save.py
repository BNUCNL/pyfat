# !/usr/bin/python
# -*- coding: utf-8 -*-


import nibabel as nib
from nibabel import streamlines
import nibabel.streamlines.tck as nibtck

def save_tck(streamline=None, header=None, data_per_streamline=None,
         data_per_point=None, affine_to_rasmm=None, out_path=None):
    '''
    save streamlines data
    :param streamlines: iterable of ndarrays or :class:`ArraySequence`, optional
            Sequence of $T$ streamlines. Each streamline is an ndarray of
            shape ($N_t$, 3) where $N_t$ is the number of points of
            streamline $t$.
    :param header:streamlines data header
    :param data_per_streamline: dict of iterable of ndarrays, optional
            Dictionary where the items are (str, iterable).
            Each key represents an information $i$ to be kept alongside every
            streamline, and its associated value is an iterable of ndarrays of
            shape ($P_i$,) where $P_i$ is the number of scalar values to store
            for that particular information $i$.
    :param data_per_point: dict of iterable of ndarrays, optional
            Dictionary where the items are (str, iterable).
            Each key represents an information $i$ to be kept alongside every
            point of every streamline, and its associated value is an iterable
            of ndarrays of shape ($N_t$, $M_i$) where $N_t$ is the number of
            points for a particular streamline $t$ and $M_i$ is the number
            scalar values to store for that particular information $i$.
    :param affine_to_rasmm: ndarray of shape (4, 4) or None, optional
            Transformation matrix that brings the streamlines contained in
            this tractogram to *RAS+* and *mm* space where coordinate (0,0,0)
            refers to the center of the voxel. By default, the streamlines
            are in an unknown space, i.e. affine_to_rasmm is None.
    :param out_path:save filename
    :return: streamlines data
    '''
    tractogram = streamlines.tractogram.Tractogram(streamlines=streamline, data_per_streamline=data_per_streamline,
                                               data_per_point=data_per_point, affine_to_rasmm=affine_to_rasmm)
    datdat = nibtck.TckFile(tractogram=tractogram, header=header)
    datdat.save(out_path)

def save_nifti(volume, affine, output):
    '''

    :param volume: input volume data
    :param affine: affine of volume
    :param output: save filename
    :return:
    '''
    dm_img = nib.Nifti1Image(volume.astype("int16"), affine)
    dm_img.to_filename(output)
