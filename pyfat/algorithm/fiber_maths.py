# !/usr/bin/python
# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:l

from scipy.spatial.distance import pdist, squareform


def coordinate_dist(coordinate, metric='euclidean'):
    '''
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
    '''
    dist_temp = pdist(coordinate, metric)
    sdist = squareform(dist_temp)
    return sdist