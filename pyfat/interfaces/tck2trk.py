# !/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
import nipype.interfaces.mrtrix as mrt


def tck2trk(tckfile, volumefile, trkfile):
    """
    Convert .tck file to .trk file
    Parameters
    ----------
    tckfile: streamlines data .tck
    volumefile: volume data .nii.gz (T1w volume)
    trkfile: streamlines data .trk

    Return
    ------
    trkfile
    """
    tck2trk = mrt.MRTrix2TrackVis()
    tck2trk.inputs.in_file = tckfile
    tck2trk.inputs.image_file = volumefile
    tck2trk.inputs.out_filename = trkfile
    tck2trk.run()
