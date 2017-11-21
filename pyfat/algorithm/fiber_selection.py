# !/usr/bin/python
# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:l

from dipy.tracking import streamline, utils


def select_by_roi(streamlines, target_mask, affine, include=True):
    """
    Include or exclude the streamlines according to a ROI
    """
    roi_selection = utils.target(streamlines=streamlines, target_mask=target_mask,
                                 affine=affine, include=include)
    roi_streamlines = list(roi_selection)

    return roi_streamlines


def select_by_rois(streamlines, rois, include, mode=None, affine=None, tol=None):
    """
    Include or exclude the streamlines according to some ROIs
    example
    >>>selection = select_by_rois(streamlines, [mask1, mask2], [True, False], mode="both_end", tol=1.0)
    >>>selection = list(selection)
    """
    rois_selection = streamline.select_by_rois(streamline=streamline, rois=rois,
                                               include=include, mode=mode, affine=affine, tol=tol)
    rois_streamlines = list(rois_selection)

    return rois_streamlines
