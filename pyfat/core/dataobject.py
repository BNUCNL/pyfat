# !/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
import numpy as np
import nibabel.streamlines.tractogram as nibtcg
import nibabel.streamlines.array_sequence as nibas
from dipy.tracking.utils import length
import nibabel.streamlines.tck as nibtck
import dipy.tracking.metrics as dtm


class Fasciculus(object):
    """Base attributes of the fasciculus"""
    def __init__(self, source, header=None, lengths_min=None, lengths_max=None,
                 data_per_streamline=None, data_per_point=None, affine_to_rasmm=None):
        """
        Create a dataset  from a TckFile which has following attributes:

        Parameters
        ----------
        source : Tck file path or ArraySequence
            Tck dataset, specified either as a filename (single file) or
            a ArraySequence. When source is a ArraySequence, parameter header is required.
        header : Tck header structure
            Tck header structure.
        lengths_min : Fasciculus min length
            Fasciculus min length
        lengths_max : Faciculus max length
            Faciculus max length
        data_per_streamline : dict of iterable of ndarrays, optional
            Dictionary where the items are (str, iterable).
            Each key represents an information $i$ to be kept alongside every
            streamline, and its associated value is an iterable of ndarrays of
            shape ($P_i$,) where $P_i$ is the number of scalar values to store
            for that particular information $i$.
        data_per_point : dict of iterable of ndarrays, optional
            Dictionary where the items are (str, iterable).
            Each key represents an information $i$ to be kept alongside every
            point of every streamline, and its associated value is an iterable
            of ndarrays of shape ($N_t$, $M_i$) where $N_t$ is the number of
            points for a particular streamline $t$ and $M_i$ is the number
            scalar values to store for that particular information $i$.
        affine_to_rasmm : ndarray of shape (4, 4) or None, optional
            Transformation matrix that brings the streamlines contained in
            this tractogram to *RAS+* and *mm* space where coordinate (0,0,0)
            refers to the center of the voxel. By default, the streamlines
            are in an unknown space, i.e. affine_to_rasmm is None.

        Return
        ------
        Fasciculus

        """
        if isinstance(source, nibas.ArraySequence):
            self._data = source
            if not isinstance(header, dict):
                raise ValueError("Parameter header must be specified!")
            elif source.data.shape[1] == 3:
                self._header = header
                self._img = None
            else:
                raise ValueError("Data dimension does not match.")
            if isinstance(data_per_streamline, nibtcg.PerArrayDict):
                self._data_per_streamline = data_per_streamline
            else:
                raise ValueError("data_per_streamline must be an object of "
                                 "class nibabel.streamlines.tractogram.PerArrayDict.")
            if isinstance(data_per_point, nibtcg.PerArraySequenceDict):
                self._data_per_point = data_per_point
            else:
                raise ValueError("data_per_point must be an object of "
                                 "class nibabel.streamlines.tractogram.PerArraySequenceDict.")
            if affine_to_rasmm:
                self._affine_to_rasmm = affine_to_rasmm
            else:
                self._affine_to_rasmm = self._header['voxel_to_rasmm']
        else:
            self._img = nibtck.TckFile.load(source)
            self._header = self._img.header
            self._data = self._img.streamlines
            self._data_per_streamline = self._img.tractogram.data_per_streamline
            self._data_per_point = self._img.tractogram.data_per_point
            self._affine_to_rasmm = self._header['voxel_to_rasmm']

        # tractography algorithm
        self._algorithm = self._header['method']
        # step size
        self._step_size = self._header['step_size']
        # space
        self._space = self.get_space()
        # length
        self._lengths = self.get_lengths()
        # counts
        self._counts = self.get_counts()
        # labes
        self._labels = len(self._data)*[None]
        # dict(self._label, self._data)
        self._labels_data = zip(self._labels, self._data)
        # lr ratio
        self._ratio = self.get_lr_ratio()

        if lengths_min is None:
            self._lengths_min = self.get_lengths_min()
        else:
            self._lengths_min = lengths_min
        if lengths_max is None:
            self._lengths_max = self.get_lengths_max()
        else:
            self._lengths_max = lengths_max

    def get_header(self):
        return self._header

    def update_header(self):
        pass

    def get_data(self):
        return self._data

    def set_data(self, data):
        if isinstance(data, nibas.ArraySequence):
            self._data = data
        else:
            raise ValueError("Data must be an object nibtck.ArraySequence.")

    def get_space(self):
        key = []
        for x in self._header.items():
            if isinstance(x[1], np.ndarray):
                key = x[0]
        if key:
            return key[9:12]
        else:
            raise ValueError("Transform space is unknown.")

    def get_algorithm(self):
        return self._header['method']

    def get_step_size(self):
        return self._header['step_size']

    def get_lengths_min(self):
        return self._lengths.min()

    def get_lengths_max(self):
        return self._lengths.max()

    def get_lengths(self):
        lengths = np.array(list(length(self._data)))
        return lengths

    def get_counts(self):
        counts = len(self._data)
        return counts

    def get_labes(self):
        return self._labels

    def get_labels_data(self):
        return self._labels_data

    def set_lengths_min(self, min_value):
        min_value = float(min_value)
        if self.get_lengths_min() <= min_value <= self.get_lengths_max():
            self._lengths_min = min_value
            index = self._lengths >= min_value
            self._data = self._data[index]
            self._lengths = self.get_lengths()
        else:
            raise ValueError("min_value must be in the range of %s to %s." % (self._lengths_min, self._lengths_max))

    def set_lengths_max(self, max_value):
        max_value = float(max_value)
        if self.get_lengths_min() <= max_value <= self.get_lengths_max():
            self._lengths_max = max_value
            index = self._lengths <= max_value
            self._data = self._data[index]
            self._lengths = self.get_lengths()
        else:
            raise ValueError("max_value must be in the range of %s to %s." % (self._lengths_min, self._lengths_max))

    def get_x_gradient(self):
        x_gradient = []
        for i in range(len(self._data)):
            x = self._data[i][:, 0]
            x_ahead = list(x[:])
            a = x_ahead.pop(0)
            x_ahead.append(a)
            x_stemp = np.array([x, x_ahead])
            x_gradient_list = x_stemp[1, :] - x_stemp[0, :]
            x_gradient_sum = x_gradient_list[:-2].sum()
            x_gradient.append(np.abs(x_gradient_sum))
        return x_gradient

    def get_y_gradient(self):
        y_gradient = []
        for i in range(len(self._data)):
            y = self._data[i][:, 1]
            y_ahead = list(y[:])
            a = y_ahead.pop(0)
            y_ahead.append(a)
            y_stemp = np.array([y, y_ahead])
            y_gradient_list = y_stemp[1, :] - y_stemp[0, :]
            y_gradient_sum = y_gradient_list[:-2].sum()
            y_gradient.append(np.abs(y_gradient_sum))
        return y_gradient

    def get_z_gradient(self):
        z_gradient = []
        for i in range(len(self._data)):
            z = self._data[i][:, 2]
            z_ahead = list(z[:])
            a = z_ahead.pop(0)
            z_ahead.append(a)
            z_stemp = np.array([z, z_ahead])
            z_gradient_list = z_stemp[1, :] - z_stemp[0, :]
            z_gradient_sum = z_gradient_list[:-2].sum()
            z_gradient.append(np.abs(z_gradient_sum))
        return z_gradient

    def get_mean_curvature(self):
        mean_curvature = [dtm.mean_curvature(stream) for stream in self._data]
        return mean_curvature

    def get_mean_orientation(self):
        mean_orientation = [dtm.mean_orientation(stream) for stream in self._data]
        return mean_orientation

    def get_lr_ratio(self):
        r = []
        for i in range(len(self._data)):
            rat = len(self._data[i][:, 0][self._data[i][:, 0] <= 0]) / \
                  len(self._data[i][:, 0][self._data[i][:, 0] >= 0])
            if rat < 1:
                rat = 1 / rat
            r.append(rat)
        return r

    def set_labels(self, labels):
        if len(labels) == len(self._labels):
            self._labels = labels
        else:
            raise ValueError("Data dimension does not match.")

    def set_labels_data(self, labels):
        if len(labels) == len(self._data):
            self._labels = labels
            self._labels_data = zip(self._labels, self._data)
        else:
            raise ValueError("Data dimension does not match.")

    def xmin_nodes(self):
        """Extract xmin nodes"""
        xmin_nodes = nibas.ArraySequence()
        for i in range(len(self._data)):
            l = self._data[i][:, 0]
            l_ahead = list(l[:])
            a = l_ahead.pop(0)
            l_ahead.append(a)
            x_stemp = np.array([l, l_ahead])
            x_stemp_index = x_stemp.prod(axis=0)
            index0 = np.argwhere(x_stemp_index <= 0)
            index_term = np.argmin((abs(self._data[i][index0[0][0]][0]),
                                    abs(self._data[i][index0[0][0] + 1][0])))
            index = index0[0][0] + index_term
            xmin_nodes.append(self._data[i][index])
        return xmin_nodes

    def save2tck(self, file_path):
        """Save to a tck file"""
        tractogram = nibtcg.Tractogram(streamlines=self._data, data_per_streamline=self._data_per_streamline,
                                       data_per_point=self._data_per_point, affine_to_rasmm=self._affine_to_rasmm)
        datdat = nibtck.TckFile(tractogram=tractogram, header=self._header)
        datdat.save(file_path)
