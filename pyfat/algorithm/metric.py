# !/usr/bin/python
# -*- coding: utf-8 -*-


from scipy.spatial.distance import pdist, squareform
from dipy.tracking.utils import length
import nibabel.streamlines.tck as nibtck
import nibabel.streamlines.array_sequence as nibAS


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
    def __init__(self, imgtck):
        self.imgtck = imgtck
        self.lengths = None
        self.count = None

    def length(self):
        self.lengths = length(self.imgtck)
        return self.lengths

    def count(self):
        if isinstance(self.imgtck, nibtck.TckFile):
            self.count = len(self.imgtck.streamlines)
        if isinstance(self.imgtck, nibAS.ArraySequence):
            self.count = len(self.imgtck)
        return self.count
