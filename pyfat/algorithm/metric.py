# !/usr/bin/python
# -*- coding: utf-8 -*-


from scipy.spatial.distance import pdist, squareform
from dipy.tracking.utils import length
import numpy as np
import nibabel.streamlines.tck as nibtck
import nibabel.streamlines.array_sequence as nibas


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


class Metric(object):
    def __init__(self, streamlines):
        self.streamlines = streamlines
        self.lengths = self.length()
        self.counts = self.count()
        self.lengths_min = self.length_min()

    def length(self):
        lengths = np.array(list(length(self.streamlines)))
        return lengths

    def count(self):
        counts = len(self.streamlines)
        return counts

    def length_min(self):
        return self.lengths.min()

    def length_max(self):
        return self.lengths.max()

    def set_length_min(self, min_value):
        index = self.lengths >= min_value
        set_length_min_fib = self.streamlines[index]
        return Metric(set_length_min_fib)

    def set_length_max(self, max_value):
        index = self.lengths <= max_value
        set_length_max_fib = self.streamlines[index]
        return Metric(set_length_max_fib)

    def fib_merge(self, stream):
        ars = nibas.ArraySequence()
        for i in self.streamlines:
            ars.append(i)
        for j in stream:
            ars.append(j)
        return Metric(ars)
