#!/usr/bin/python
# -*- coding: utf-8 -*-

import nipype.interfaces.mrtrix3 as mrt


def tck2vtk(in_file, reference, out_file):
    """
        Convert .tck file to .vtk file
        Parameters
        ----------
        in_file: streamlines data .tck
        reference: volume data .nii.gz (b0-image)
        out_file: streamlines data .vtk

        Return
        ------
        trkfile
    """
    vtk = mrt.TCK2VTK()
    vtk.inputs.in_file = in_file
    vtk.inputs.reference = reference
    vtk.inputs.out_file = out_file
    vtk.run()
