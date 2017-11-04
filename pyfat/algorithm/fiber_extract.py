# !/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
import numpy as np
import nibabel.streamlines.array_sequence as nibas

from pyfat.core.dataobject import Fasciculus


class FibSelection(object):
    """Based on the fasciculus choose fiber"""
    def __init__(self, fasciculus):
        """
        Based on the fasciculus choose fiber

        Parameters
        ----------
        fasciculus : an object of class Fasciculus
            An object of class Fasciculus

        Return
        ------
        FibSelection

        """
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

        return fasciculus_data

    def single_point_mid_sag(self):
        """
        A single time through the sagittal plane in the middle.
        The function is implemented after function endpoint_dissimilarity
        """
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

        return fasciculus_data

    def lr_step(self, n=20):
        """
        Extract lr n steps fiber
        The function is implemented after function single_point_mid_sag
        """
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

        return fasciculus_data

    def lr_rat(self, ratio=1.5):
        """
        Extract lr ratio fiber
        The function is implemented after function single_point_mid_sag
        """
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

        return fasciculus_data

    def xmax_gradient(self, n=None):
        """
        Extract fiber according to x max gradient
        The function is implemented after function single_point_mid_sag
        """
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

        return fasciculus_data

    def ymax_gradient(self, n=None):
        """
        Extract fiber according to y max gradient
        The function is implemented after function single_point_mid_sag
        """
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

        return fasciculus_data

    def zmax_gradient(self, n=None):
        """
        Extract fiber according to z max gradient
        The function is implemented after function single_point_mid_sag
        """
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

        return fasciculus_data

    def fib_cc(self):
        """
        Extract corpus callosum fiber
        The function is implemented after function step/lr/gradient
        """
        fasciculus_data = self._fasciculus.get_data()
        labels = self._fasciculus.get_labes()
        xmin = self._fasciculus.xmin_nodes()
        node_clusters = []
        fib_clusters = []
        for label in set(labels):
            index_i = np.argwhere(labels == label)
            node_clusters.append(xmin[index_i])
            fib_clusters.append(fasciculus_data[index_i])

        index = [n_c[:, 2].max() for n_c in node_clusters]
        index_need = np.array(index).argmax()
        cc_nodes = node_clusters[index_need]
        cc_fibs = fib_clusters[index_need]

        return cc_nodes, cc_fibs

    def fib_ac_oc(self):
        """
        Extract anterior commissure and optic chiasma fiber
        The function is implemented after function step/lr/gradient
        """
        fasciculus_data = self._fasciculus.get_data()
        labels = self._fasciculus.get_labes()
        xmin = self._fasciculus.xmin_nodes()

        node_clusters = []
        fib_clusters = []
        for label in set(labels):
            index_i = np.argwhere(labels == label)
            node_clusters.append(xmin[index_i])
            fib_clusters.append(fasciculus_data[index_i])

        clusters_z_mean = [n_c[:, 2].mean() for n_c in node_clusters]
        clusters_y_mean = [n_c[:, 1].mean() for n_c in node_clusters]
        index_z = np.array(clusters_z_mean) < 1.50
        index_y = np.array(clusters_y_mean) < -10.50

        remain_clusters = []
        remain_fib_clusters = []
        for i in range(len(node_clusters)):
            if not index_z[i] or not index_y[i]:
                remain_clusters.append(node_clusters[i])
                remain_fib_clusters.append(fib_clusters[i])

        clusters_z_max = [k[:, 2].max() for k in remain_clusters]
        node = np.array(zip(range(len(clusters_z_max)), clusters_z_max))
        node_sort = node[np.lexsort(node.T)]

        node_total = []
        other_node = []
        for d in node_sort[2:-1]:
            for n in remain_clusters[int(d[0])]:
                other_node.append(list(n))

        node_total.append(remain_clusters[int(node_sort[0][0])])
        node_total.append(remain_clusters[int(node_sort[1][0])])
        if len(other_node) == 0:
            pass
        else:
            node_total.append(np.array(other_node))
        node_total.append(remain_clusters[int(node_sort[-1][0])])

        fib_total = []
        other = nibas.ArraySequence()
        for d in node_sort[2:-1]:
            for f in remain_fib_clusters[int(d[0])]:
                other.append(f)

        fib_total.append(remain_fib_clusters[int(node_sort[0][0])])
        fib_total.append(remain_fib_clusters[int(node_sort[1][0])])
        if len(other) == 0:
            pass
        else:
            fib_total.append(other)
        fib_total.append(remain_fib_clusters[int(node_sort[-1][0])])

        # return [oc ac other cc] or [oc ac cc]
        return node_total, fib_total

    def labels2fasc(self, label):
        """Extract fasc according to labels"""
        fasciculus_data = self._fasciculus.get_data()
        labels = self._fasciculus.get_labes()
        fib_clusters = []
        for label in set(labels):
            index_i = np.argwhere(labels == label)
            fib_clusters.append(fasciculus_data[index_i])
        # labels_data = zip(set(labels), fib_clusters)
        label_data = fib_clusters[label]
        return label_data
