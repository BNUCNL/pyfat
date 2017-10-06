# !/usr/bin/python
# -*- coding: utf-8 -*-


import numpy as np
from dipy.viz import fvtk

from dipy.segment.metric import Feature, Metric, VectorOfEndpointsFeature
from dipy.tracking.streamline import length


class ArcLengthFeature(Feature):
    """ Computes the arc length of a streamline. """
    def __init__(self):
        # The arc length stays the same even if the streamline is reversed.
        super(ArcLengthFeature, self).__init__(is_order_invariant=True)

    def infer_shape(self, streamline):
        """ Infers the shape of features extracted from `streamline`. """
        # Arc length is a scalar
        return 1

    def extract(self, streamline):
        """ Extracts features from `streamline`. """
        # return np.sum(np.sqrt(np.sum((streamline[1:] - streamline[:-1]) ** 2)))
        # or use a Dipy's function that computes the arc length of a streamline.
        return length(streamline)


class CosineMetric(Metric):
    """ Computes the cosine distance between two streamlines. """
    def __init__(self):
        # For simplicity, features will be the vector between endpoints of a streamline.
        super(CosineMetric, self).__init__(feature=VectorOfEndpointsFeature())

    def are_compatible(self, shape1, shape2):
        """ Checks if two features are vectors of same dimension.

        Basically this method exists so we don't have to do this check
        inside the `dist` method (speedup).
        """
        return shape1 == shape2 and shape1[0] == 1

    def dist(self, v1, v2):
        """ Computes a the cosine distance between two vectors. """
        norm = lambda x: np.sqrt(np.sum(x**2))
        cos_theta = np.dot(v1, v2.T) / (norm(v1)*norm(v2))

        # Make sure it's in [-1, 1], i.e. within domain of arccosine
        cos_theta = np.minimum(cos_theta, 1.)
        cos_theta = np.maximum(cos_theta, -1.)
        return np.arccos(cos_theta) / np.pi  # Normalized cosine distance

def show(imgtck, clusters, out_path):
    colormap = fvtk.create_colormap(np.ravel(clusters.centroids), name='jet')
    colormap_full = np.ones((len(imgtck.streamlines), 3))
    for cluster, color in zip(clusters, colormap):
        colormap_full[cluster.indices] = color

    ren = fvtk.ren()
    ren.SetBackground(1, 1, 1)
    fvtk.add(ren, fvtk.streamtube(imgtck.streamlines, colormap_full))
    fvtk.record(ren, n_frames=1, out_path=out_path, size=(600, 600))
    fvtk.show(ren)
