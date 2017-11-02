# !/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
import numpy as np

from pyfat.core.dataobject import Fasciculus


class FibSelection(object):
    """Based on the fasciculus choose fiber"""
    def __init__(self, fasciculus):
        if isinstance(fasciculus, Fasciculus):
            self._fasciculus = fasciculus
        else:
            raise ValueError("The fasciculus must be an object of class Fasciculus.")

    def endpoint_dissimilarity(self):
        """Extract endpoint dissimilar fiber"""
        fasciculus_data = self._fasciculus.get_data()
        index = len(fasciculus_data) * [False]
        for i in range(len(fasciculus_data)):
            if fasciculus_data[i][0][0] * fasciculus_data[i][-1][0] < 0:
                index[i] = True
        fasciculus_data = fasciculus_data[index]
        self._fasciculus.set_data(fasciculus_data)
        return self._fasciculus

    def single_point_mid_sag(self):
        """A single time through the sagittal plane in the middle."""
        fasciculus_data = self._fasciculus.get_data()
        index = len(fasciculus_data) * [False]
        for i in range(len(fasciculus_data)):
            l = fasciculus_data[i][:, 0]
            l_ahead = list(l[:])
            a = l_ahead.pop(0)
            l_ahead.append(a)
            x_stemp = np.array([l, l_ahead])
            x_stemp_index = x_stemp.prod(axis=0)
            if len(np.argwhere(x_stemp_index < 0)) == 2 \
                    or len(np.argwhere(x_stemp_index == 0)) == 2:
                index[i] = True
        fasciculus_data = fasciculus_data[index]
        self._fasciculus.set_data(fasciculus_data)
        return self._fasciculus

    def lr_step(self, n=20):
        """Extract lr n steps fiber"""
        fasciculus_data = self._fasciculus.get_data()
        index = len(fasciculus_data) * [False]
        for i in range(len(fasciculus_data)):
            l = fasciculus_data[i][:, 0]
            l_ahead = list(l[:])
            a = l_ahead.pop(0)
            l_ahead.append(a)
            x_stemp = np.array([l, l_ahead])
            x_stemp_index = x_stemp.prod(axis=0)
            index0 = np.argwhere(x_stemp_index <= 0)
            index_term = np.argmin((abs(fasciculus_data[i][index0[0][0]][0]),
                                    abs(fasciculus_data[i][index0[0][0] + 1][0])))
            index_t = index0[0][0] + index_term
            if index_t - n in range(len(l)) \
                    and index_t + n in range(len(l)):
                index[i] = True
        fasciculus_data = fasciculus_data[index]
        self._fasciculus.set_data(fasciculus_data)
        return self._fasciculus

    def lr_rat(self, ratio=1.5):
        """Extract lr ratio fiber"""
        fasciculus_data = self._fasciculus.get_data()
        index = len(fasciculus_data) * [False]
        for i in range(len(fasciculus_data)):
            rat = len(fasciculus_data[i][:, 0][fasciculus_data[i][:, 0] <= 0]) / \
                  len(fasciculus_data[i][:, 0][fasciculus_data[i][:, 0] >= 0])
            if rat < 1:
                rat = 1 / rat
            if rat < ratio:
                index[i] = True
        fasciculus_data = fasciculus_data[index]
        self._fasciculus.set_data(fasciculus_data)
        return self._fasciculus

    def xmax_gradient(self, n=None):
        """Extract fiber according to x max gradient"""
        fasciculus_data = self._fasciculus.get_data()
        index = len(fasciculus_data) * [False]
        if n:
            for i in range(len(fasciculus_data)):
                l = fasciculus_data[i][:, 0]
                l_ahead = list(l[:])
                a = l_ahead.pop(0)
                l_ahead.append(a)
                x_stemp = np.array([l, l_ahead])
                x_stemp_index = x_stemp.prod(axis=0)
                index0 = np.argwhere(x_stemp_index <= 0)
                index_term = np.argmin((abs(fasciculus_data[i][index0[0][0]][0]),
                                        abs(fasciculus_data[i][index0[0][0] + 1][0])))
                index_t = index0[0][0] + index_term
                if (index_t - n) in range(len(l)) \
                        and (index_t + n) in range(len(l)):
                    grad = np.gradient(fasciculus_data[i])
                    x_grad = grad[0][:, 0].sum()
                    y_grad = grad[0][:, 1].sum()
                    z_grad = grad[0][:, 2].sum()

                    index_temp = np.array([x_grad, y_grad, z_grad]).argmax()
                    if index_temp == 0:
                        index[i] = True
        else:
            for i in range(len(fasciculus_data)):
                grad = np.gradient(fasciculus_data[i])
                x_grad = grad[0][:, 0].sum()
                y_grad = grad[0][:, 1].sum()
                z_grad = grad[0][:, 2].sum()

                index_temp = np.array([x_grad, y_grad, z_grad]).argmax()
                if index_temp == 0:
                    index[i] = True
        fasciculus_data = fasciculus_data[index]
        self._fasciculus.set_data(fasciculus_data)
        return self._fasciculus

    def ymax_gradient(self, n=None):
        """Extract fiber according to y max gradient"""
        fasciculus_data = self._fasciculus.get_data()
        index = len(fasciculus_data) * [False]
        if n:
            for i in range(len(fasciculus_data)):
                l = fasciculus_data[i][:, 0]
                l_ahead = list(l[:])
                a = l_ahead.pop(0)
                l_ahead.append(a)
                x_stemp = np.array([l, l_ahead])
                x_stemp_index = x_stemp.prod(axis=0)
                index0 = np.argwhere(x_stemp_index <= 0)
                index_term = np.argmin((abs(fasciculus_data[i][index0[0][0]][0]),
                                        abs(fasciculus_data[i][index0[0][0] + 1][0])))
                index_t = index0[0][0] + index_term
                if (index_t - n) in range(len(l)) \
                        and (index_t + n) in range(len(l)):
                    grad = np.gradient(fasciculus_data[i])
                    x_grad = grad[0][:, 0].sum()
                    y_grad = grad[0][:, 1].sum()
                    z_grad = grad[0][:, 2].sum()

                    index_temp = np.array([x_grad, y_grad, z_grad]).argmax()
                    if index_temp == 1:
                        index[i] = True
        else:
            for i in range(len(fasciculus_data)):
                grad = np.gradient(fasciculus_data[i])
                x_grad = grad[0][:, 0].sum()
                y_grad = grad[0][:, 1].sum()
                z_grad = grad[0][:, 2].sum()

                index_temp = np.array([x_grad, y_grad, z_grad]).argmax()
                if index_temp == 1:
                    index[i] = True
        fasciculus_data = fasciculus_data[index]
        self._fasciculus.set_data(fasciculus_data)
        return self._fasciculus

    def zmax_gradient(self, n=None):
        """Extract fiber according to z max gradient"""
        fasciculus_data = self._fasciculus.get_data()
        index = len(fasciculus_data) * [False]
        if n:
            for i in range(len(fasciculus_data)):
                l = fasciculus_data[i][:, 0]
                l_ahead = list(l[:])
                a = l_ahead.pop(0)
                l_ahead.append(a)
                x_stemp = np.array([l, l_ahead])
                x_stemp_index = x_stemp.prod(axis=0)
                index0 = np.argwhere(x_stemp_index <= 0)
                index_term = np.argmin((abs(fasciculus_data[i][index0[0][0]][0]),
                                        abs(fasciculus_data[i][index0[0][0] + 1][0])))
                index_t = index0[0][0] + index_term
                if (index_t - n) in range(len(l)) \
                        and (index_t + n) in range(len(l)):
                    grad = np.gradient(fasciculus_data[i])
                    x_grad = grad[0][:, 0].sum()
                    y_grad = grad[0][:, 1].sum()
                    z_grad = grad[0][:, 2].sum()

                    index_temp = np.array([x_grad, y_grad, z_grad]).argmax()
                    if index_temp == 2:
                        index[i] = True
        else:
            for i in range(len(fasciculus_data)):
                grad = np.gradient(fasciculus_data[i])
                x_grad = grad[0][:, 0].sum()
                y_grad = grad[0][:, 1].sum()
                z_grad = grad[0][:, 2].sum()

                index_temp = np.array([x_grad, y_grad, z_grad]).argmax()
                if index_temp == 2:
                    index[i] = True
        fasciculus_data = fasciculus_data[index]
        self._fasciculus.set_data(fasciculus_data)
        return self._fasciculus
