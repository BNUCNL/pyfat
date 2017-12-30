# !/usr/bin/python
# -*- coding: utf-8 -*-


import nibabel.streamlines.tck as nibtck
from nibabel import trackvis


def load_tck(file):
    """
    load the streamlines data (.tck)
    Parameters
    ----------
    file: data path

    Return
    ------
    streamlines
    """
    imgtck = nibtck.TckFile.load(file)
    return imgtck


def load_trk(file):
    """
    load the streamlines data (.trk)
    Parameters
    ----------
    file: data path

    Return
    ------
    streamlines
    """
    streams, hdr = trackvis.read(file, points_space="rasmm")
    # streamlines = [s[0] for s in streams]
    return streams, hdr
