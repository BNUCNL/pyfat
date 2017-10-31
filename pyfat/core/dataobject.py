# !/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
from dipy.tracking.utils import length
import nibabel.streamlines.tck as nibtck

class Fasciculus(object):
    """Base attributes of the fasciculus"""
    def __init__(self, source, header=None, lengths_min=None, lengths_max=None):
        """
        Create a dataset  from an TckFile which has following attributes:

        Parameters
        ----------
        source: Tck file path or ArraySequence
            Tck dataset, specified either as a filename (single file) or
            a ArraySequence. When source is a ArraySequence, parameter header is required.
        header: Tck header structure
            Tck header structure.

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
        else:
            self._img = nibtck.TckFile.load(source)
            self._header = self._img.header
            self._data = self._img.streamlines

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
            self._lengths_min = min_value
            if self.get_lengths_min() <= min_value <= self.get_lengths_max():
                index = self._lengths >= min_value
                self._data = self._data[index]
            else:
                ValueError("min_value is not in the range of length_min to length_max.")
        except ValueError:
            print "min_value must be a number."

    def set_lengths_max(self, max_value):
        try:
            if self.get_lengths_min() <= max_value <= self.get_lengths_max():
                index = self._lengths <= max_value
                self._data = self._data[index]
            else:
                ValueError("max_value is not in the range of length_min to length_max.")
        except ValueError:
            print "min_value must be a number."
