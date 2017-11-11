# !/usr/bin/python
# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:l

from scipy.spatial.distance import pdist, squareform
from dipy.tracking.streamline import set_number_of_points
from dipy.align.streamlinear import StreamlineLinearRegistration


def coordinate_dist(coordinate, metric='euclidean'):
    """
    coordinate distance
    :param coordinate: ndarray
        An m by n array of m original observations in an
        n-dimensional space.
    :param metric: string or function
        The distance metric to use. The distance function can
        be 'braycurtis', 'canberra', 'chebyshev', 'cityblock',
        'correlation', 'cosine', 'dice', 'euclidean', 'hamming',
        'jaccard', 'kulsinski', 'mahalanobis', 'matching',
        'minkowski', 'rogerstanimoto', 'russellrao', 'seuclidean',
        'sokalmichener', 'sokalsneath', 'sqeuclidean', 'yule'.
    :return: matrix of distance
    """
    dist_temp = pdist(coordinate, metric)
    sdist = squareform(dist_temp)
    return sdist


def bundle_registration(cb_subj1, cb_subj2, pts=12):
    """
    Register two bundle from two subjects
    directly in the space of streamlines
    """
    cb_subj1 = set_number_of_points(cb_subj1, pts)
    cb_subj2 = set_number_of_points(cb_subj2, pts)

    srr = StreamlineLinearRegistration()
    srm = srr.optimize(static=cb_subj1, moving=cb_subj2)
    cb_subj2_aligned = srm.transform(cb_subj2)

    return cb_subj2_aligned
