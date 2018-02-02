# !/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
import numpy as np
import nibabel as nib

from dipy.tracking import streamline, utils
import nibabel.streamlines.array_sequence as nibas
import nibabel.streamlines.tck as nibtck
import numpy.linalg as npl
from nibabel.affines import apply_affine


class Tract(object):

    def __init__(self, name=None, Id=None, space='native', xform=None):
        self.name = name
        self.id = Id
        self.space = space
        self.xform = xform

    def __setattr__(self, key, value):
        object.__setattr__(self, key, value)

    def __getattr__(self, item):
        if item not in self.__dict__:
            return None

    def load_streamline(self, source):
        self.streamline_img = nibtck.TckFile.load(source)
        self.streamline = self.streamline_img.streamlines

    def load_scalar(self, scalar_source, scalar_name):
        if self.streamline_img is None:
            raise ValueError("Streamline data does not exist.")
        else:
            if self.scalar is None:
                self.scalar = {}
            scalar = nib.load(scalar_source)
            self.scalar[scalar_name] = scalar

    def get_streamline(self):

        return self.streamline

    def get_streamline_header(self):

        return self.streamline_img.header

    def set_streamline(self, data):
        if isinstance(data, nibas.ArraySequence):
            self.streamline = data

        else:
            raise ValueError("Data must be an object of nibtck.ArraySequence.")

    def set_scalar(self, data, data_name):
        if data_name in self.scalar.keys():
            if isinstance(data, type):
                self.scalar[data_name] = data

    def get_scalar(self, scalar_name=None):
        if scalar_name is None:
            return self.scalar
        else:
            if scalar_name in self.scalar.keys():
                return self.scalar[scalar_name]

    def scalar2streamline(self, scalar_name):
        streamline_scalar = {}
        for scalar in scalar_name:
            if scalar in self.scalar.keys():
                scalar_img = self.scalar[scalar]
                scalar_data = scalar_img.get_data()
                scalar_l = []
                for s in self.streamline:
                    s_points = apply_affine(npl.inv(scalar_img.affine), s)
                    scalar_l.append(np.array([scalar_data[int(p[0]), int(p[1]), int(p[2])] for p in s_points]).mean())
                scalar_l = np.array(scalar_l).mean()
            streamline_scalar[scalar_name] = scalar_l

        return streamline_scalar

    def select_by_vol_roi(self, target_mask, affine, streamlines=None, include=True):
        """
        Include or exclude the streamlines according to a ROI
        """
        if streamlines is None:
            streamlines = self.streamline
        roi_selection = utils.target(streamlines=streamlines, target_mask=target_mask,
                                     affine=affine, include=include)
        roi_streamlines = list(roi_selection)

        return roi_streamlines

    def select_by_vol_rois(self, rois, include, streamlines=None, mode=None, affine=None, tol=None):
        """
        Include or exclude the streamlines according to some ROIs
        """
        if streamlines is None:
            streamlines = self.streamline
        rois_selection = streamline.select_by_rois(streamline=streamlines, rois=rois,
                                                   include=include, mode=mode, affine=affine, tol=tol)
        rois_streamlines = list(rois_selection)

        return rois_streamlines
