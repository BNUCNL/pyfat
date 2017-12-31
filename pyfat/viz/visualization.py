# !/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import numpy.linalg as npl
import matplotlib.pyplot as plt
from nibabel.affines import apply_affine

# import h5py
from dipy.viz import fvtk
from time import sleep


def show(lengths, x=180, y=10000,
         title='Length histogram', xlabel='Length', ylabel='Count'):
    """Display length or lr ratio"""
    plt.figure('Fiber statistics')
    plt.subplot(111)
    plt.title(title)
    plt.hist(lengths, bins=100, color='burlywood')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.text(x, y, 'fiber_count=%d' % len(lengths), fontsize=10)

    plt.show()


def show_2d_node(img, Ls_temp):
    """Points mapping to slice"""
    fig, ax = plt.subplots()
    slice = img.get_data()[img.shape[0]/2, :, :]
    Ls_temp = apply_affine(npl.inv(img.affine), Ls_temp)
    ax.imshow(slice.T, cmap='gray', origin='lower')
    ax.plot(np.array(Ls_temp)[:, 1], np.array(Ls_temp)[:, 2], 'o')
    ax.set_title('y_z distribution')
    plt.show()


def show_dist_matrix(sdist):
    """Display distance matrix"""
    name = range(sdist.shape[0])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(sdist, vmin=sdist.min(), vmax=sdist.max())
    fig.colorbar(cax)
    ticks = np.arange(0, sdist.shape[0], 1)
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)
    ax.set_xticklabels(name)
    ax.set_yticklabels(name)
    plt.show()


def show_slice_density(img, Ls_temp):
    """Show middle slice density"""
    fig, ax = plt.subplots()
    Ls_temp = np.array(Ls_temp)
    Ls_temp.T[0] = 0
    Ls_temp = apply_affine(npl.inv(img.affine), Ls_temp)
    slice = img.get_data()[img.shape[0]/2, :, :]
    counts = np.zeros(slice.shape)
    for Ls in Ls_temp:
        j = Ls[1]
        k = Ls[2]
        counts[int(j), int(k)] += 1
        print j, k

    counts[counts == 0.0] = np.nan
    ax.imshow(slice.T, cmap='gray', origin='lower')
    cax = ax.imshow(counts.T, cmap=plt.cm.hot, origin='lower')
    plt.colorbar(cax)
    plt.show()


def qcomposition(array_list):
    """Composite several qrgba arrays into one."""
    if not len(array_list):
        raise ValueError('Input array list cannot be empty.')

    dimension = array_list[0].ndim
    if dimension not in (2, 3):
        raise ValueError('RGBA array must be 2D or 3D.')

    result = np.array(array_list[0][..., :3], dtype=np.int64)
    if dimension == 3:
        h, w, channel = array_list[0].shape
        for index in range(1, len(array_list)):
            item = np.array(array_list[index], dtype=np.int64)
            alpha_array = np.tile(item[..., -1].reshape((-1, 1)), (1, 1, 3))
            alpha_array = alpha_array.reshape((h, w, 3))
            result = item[..., :3] * alpha_array + result * (255 - alpha_array)
            result /= 255
    elif dimension == 2:
        for i in range(1, len(array_list)):
            item = array_list[i].astype(np.int64)
            alpha_channel = item[:, -1]
            alpha_channels = np.tile(alpha_channel, (3, 1)).T
            result = item[:, :3] * alpha_channels + result * (255 - alpha_channels)
            result /= 255
    result = result.astype(np.uint8)

    return result


def show_both_bundles(bundles, colors=None, show_b=False, fname=None):
    """
    Show both bundles
    bundles: return of --pyfat/algorithm/fiber_math/bundle_registration
    example:
    show_both_bundles([cb_subj1, cb_subj2_aligned],
                     colors=[fvtk.colors.orange, fvtk.colors.red],
                     fname='after_registration.png')
    """
    ren = fvtk.ren()
    ren.SetBackground(1., 1, 1)
    for (i, bundle) in enumerate(bundles):
        color = colors[i]
        lines = fvtk.streamtube(bundle, color, linewidth=0.3)
        lines.RotateX(-90)
        lines.RotateZ(90)
        fvtk.add(ren, lines)
    if show_b:
        fvtk.show(ren)
    if fname is not None:
        sleep(1)
        fvtk.record(ren, n_frames=1, out_path=fname, size=(900, 900))


def show_bundles(streamlines, clusters, show_b=True):
    # Color each streamline according to the cluster they belong to.
    colormap = fvtk.create_colormap(np.arange(len(clusters)))
    colormap_full = np.ones((len(streamlines), 3))
    for cluster, color in zip(clusters, colormap):
        colormap_full[cluster.indices] = color

    ren = fvtk.ren()
    ren.SetBackground(1, 1, 1)
    fvtk.add(ren, fvtk.streamtube(streamlines, colormap_full))
    fvtk.record(ren, n_frames=1, out_path='fornix_clusters_cosine.png', size=(600, 600))

    if show_b:
        fvtk.show(ren)
