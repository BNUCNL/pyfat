# !/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import nibabel.streamlines.tractogram as nibtcg
from dipy.tracking.utils import length
import nibabel.streamlines.tck as nibtck

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
        if isinstance(source, nibtck.ArraySequence):
            self._data = source
            if not isinstance(header, dict):
                raise ValueError("Parameter header must be specified!")
            elif header['nb_streamlines'] == len(source):
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
        self._labels_data = dict(zip(self._labels, self._data))

        if lengths_min is None:
            self._lengths_min = self.get_lengths_min()
        else:
            self._lengths_min = lengths_min
        if lengths_max is None:
            self._lengths_max = self.get_lengths_max()
        else:
            self._lengths_max = lengths_max

    def get_space(self):
        for x in self._header.items():
            if isinstance(x[1], np.ndarray):
                key = x[0]
            else:
                key = None
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

    def set_lengths_min(self, min_value):
        try:
            min_value = float(min_value)
            if self.get_lengths_min() <= min_value <= self.get_lengths_max():
                self._lengths_min = min_value
                index = self._lengths >= min_value
                self._data = self._data[index]
            else:
                ValueError("min_value is not in the range of length_min to length_max.")
        except ValueError:
            print "min_value must be a number."

    def set_lengths_max(self, max_value):
        try:
            max_value = float(max_value)
            if self.get_lengths_min() <= max_value <= self.get_lengths_max():
                self._lengths_max = max_value
                index = self._lengths <= max_value
                self._data = self._data[index]
            else:
                ValueError("max_value is not in the range of length_min to length_max.")
        except ValueError:
            print "min_value must be a number."

    def save2tck(self, file_path):
        """Save to a tck file"""
        tractogram = nibtcg.Tractogram(streamlines=self._data, data_per_streamline=self._data_per_streamline,
                                       data_per_point=self._data_per_point, affine_to_rasmm=self._affine_to_rasmm)
        datdat = nibtck.TckFile(tractogram=tractogram, header=self._header)
        datdat.save(file_path)
