# !/usr/bin/python
# -*- coding: utf-8 -*-


import numpy as np
from warnings import warn
import line_profiler

# Conditional import machinery for vtk
from dipy.utils.optpkg import optional_package

# Allow import, but disable doctests if we don't have vtk
vtk, have_vtk, setup_module = optional_package('vtk')
cm, have_matplotlib, _ = optional_package('matplotlib.cm')

if have_matplotlib:
    get_cmap = cm.get_cmap
else:
    from dipy.data import get_cmap
    

def colormap_lookup_table(scale_range=(0, 1), hue_range=(0.8, 0),
                          saturation_range=(1, 1), value_range=(0.8, 0.8)):
    """ Lookup table for the colormap

    Parameters
    ----------
    scale_range : tuple
        It can be anything e.g. (0, 1) or (0, 255). Usually it is the mininum
        and maximum value of your data. Default is (0, 1).
    hue_range : tuple of floats
        HSV values (min 0 and max 1). Default is (0.8, 0).
    saturation_range : tuple of floats
        HSV values (min 0 and max 1). Default is (1, 1).
    value_range : tuple of floats
        HSV value (min 0 and max 1). Default is (0.8, 0.8).

    Returns
    -------
    lookup_table : vtkLookupTable

    """
    lookup_table = vtk.vtkLookupTable()
    lookup_table.SetRange(scale_range)
    lookup_table.SetTableRange(scale_range)

    lookup_table.SetHueRange(hue_range)
    lookup_table.SetSaturationRange(saturation_range)
    lookup_table.SetValueRange(value_range)

    lookup_table.Build()
    return lookup_table


def cc(na, nd):
    return (na * np.cos(nd * np.pi / 180.0))


def ss(na, nd):
    return na * np.sin(nd * np.pi / 180.0)


def boys2rgb(v):
    """ boys 2 rgb cool colormap

    Maps a given field of undirected lines (line field) to rgb
    colors using Boy's Surface immersion of the real projective
    plane.
    Boy's Surface is one of the three possible surfaces
    obtained by gluing a Mobius strip to the edge of a disk.
    The other two are the crosscap and Roman surface,
    Steiner surfaces that are homeomorphic to the real
    projective plane (Pinkall 1986). The Boy's surface
    is the only 3D immersion of the projective plane without
    singularities.
    Visit http://www.cs.brown.edu/~cad/rp2coloring for further details.
    Cagatay Demiralp, 9/7/2008.

    Code was initially in matlab and was rewritten in Python for dipy by
    the Dipy Team. Thank you Cagatay for putting this online.

    Parameters
    ------------
    v : array, shape (N, 3) of unit vectors (e.g., principal eigenvectors of
       tensor data) representing one of the two directions of the
       undirected lines in a line field.

    Returns
    ---------
    c : array, shape (N, 3) matrix of rgb colors corresponding to the vectors
           given in V.

    """

    if v.ndim == 1:
        x = v[0]
        y = v[1]
        z = v[2]

    if v.ndim == 2:
        x = v[:, 0]
        y = v[:, 1]
        z = v[:, 2]

    x2 = x ** 2
    y2 = y ** 2
    z2 = z ** 2

    x3 = x * x2
    y3 = y * y2
    z3 = z * z2

    z4 = z * z2

    xy = x * y
    xz = x * z
    yz = y * z

    hh1 = .5 * (3 * z2 - 1) / 1.58
    hh2 = 3 * xz / 2.745
    hh3 = 3 * yz / 2.745
    hh4 = 1.5 * (x2 - y2) / 2.745
    hh5 = 6 * xy / 5.5
    hh6 = (1 / 1.176) * .125 * (35 * z4 - 30 * z2 + 3)
    hh7 = 2.5 * x * (7 * z3 - 3 * z) / 3.737
    hh8 = 2.5 * y * (7 * z3 - 3 * z) / 3.737
    hh9 = ((x2 - y2) * 7.5 * (7 * z2 - 1)) / 15.85
    hh10 = ((2 * xy) * (7.5 * (7 * z2 - 1))) / 15.85
    hh11 = 105 * (4 * x3 * z - 3 * xz * (1 - z2)) / 59.32
    hh12 = 105 * (-4 * y3 * z + 3 * yz * (1 - z2)) / 59.32

    s0 = -23.0
    s1 = 227.9
    s2 = 251.0
    s3 = 125.0

    ss23 = ss(2.71, s0)
    cc23 = cc(2.71, s0)
    ss45 = ss(2.12, s1)
    cc45 = cc(2.12, s1)
    ss67 = ss(.972, s2)
    cc67 = cc(.972, s2)
    ss89 = ss(.868, s3)
    cc89 = cc(.868, s3)

    X = 0.0

    X = X + hh2 * cc23
    X = X + hh3 * ss23

    X = X + hh5 * cc45
    X = X + hh4 * ss45

    X = X + hh7 * cc67
    X = X + hh8 * ss67

    X = X + hh10 * cc89
    X = X + hh9 * ss89

    Y = 0.0

    Y = Y + hh2 * -ss23
    Y = Y + hh3 * cc23

    Y = Y + hh5 * -ss45
    Y = Y + hh4 * cc45

    Y = Y + hh7 * -ss67
    Y = Y + hh8 * cc67

    Y = Y + hh10 * -ss89
    Y = Y + hh9 * cc89

    Z = 0.0

    Z = Z + hh1 * -2.8
    Z = Z + hh6 * -0.5
    Z = Z + hh11 * 0.3
    Z = Z + hh12 * -2.5

    # scale and normalize to fit
    # in the rgb space

    w_x = 4.1925
    trl_x = -2.0425
    w_y = 4.0217
    trl_y = -1.8541
    w_z = 4.0694
    trl_z = -2.1899

    if v.ndim == 2:

        N = len(x)
        C = np.zeros((N, 3))

        C[:, 0] = 0.9 * np.abs(((X - trl_x) / w_x)) + 0.05
        C[:, 1] = 0.9 * np.abs(((Y - trl_y) / w_y)) + 0.05
        C[:, 2] = 0.9 * np.abs(((Z - trl_z) / w_z)) + 0.05

    if v.ndim == 1:

        C = np.zeros((3,))
        C[0] = 0.9 * np.abs(((X - trl_x) / w_x)) + 0.05
        C[1] = 0.9 * np.abs(((Y - trl_y) / w_y)) + 0.05
        C[2] = 0.9 * np.abs(((Z - trl_z) / w_z)) + 0.05

    return C


def orient2rgb(v):
    """ standard orientation 2 rgb colormap

    v : array, shape (N, 3) of vectors not necessarily normalized

    Returns
    -------

    c : array, shape (N, 3) matrix of rgb colors corresponding to the vectors
           given in V.

    """

    if v.ndim == 1:
        orient = v
        orient = np.abs(orient / np.linalg.norm(orient))

    if v.ndim == 2:
        orientn = np.sqrt(v[:, 0] ** 2 + v[:, 1] ** 2 + v[:, 2] ** 2)
        orientn.shape = orientn.shape + (1,)
        orient = np.abs(v / orientn)

    return orient


def line_colors(streamlines, cmap='rgb_standard'):
    """ Create colors for streamlines to be used in fvtk.line

    Parameters
    ----------
    streamlines : sequence of ndarrays
    cmap : ('rgb_standard', 'boys_standard')

    Returns
    -------
    colors : ndarray
    """

    if cmap == 'rgb_standard':
        col_list = [orient2rgb(streamline[-1] - streamline[0])
                    for streamline in streamlines]

    if cmap == 'boys_standard':
        col_list = [boys2rgb(streamline[-1] - streamline[0])
                    for streamline in streamlines]

    return np.vstack(col_list)


lowercase_cm_name = {'blues': 'Blues', 'accent': 'Accent'}


def create_colormap(v, name='plasma', auto=True):
    """Create colors from a specific colormap and return it
    as an array of shape (N,3) where every row gives the corresponding
    r,g,b value. The colormaps we use are similar with those of matplotlib.

    Parameters
    ----------
    v : (N,) array
        vector of values to be mapped in RGB colors according to colormap
    name : str.
        Name of the colormap. Currently implemented: 'jet', 'blues',
        'accent', 'bone' and matplotlib colormaps if you have matplotlib
        installed. For example, we suggest using 'plasma', 'viridis' or
        'inferno'. 'jet' is popular but can be often misleading and we will
        deprecate it the future.
    auto : bool,
        if auto is True then v is interpolated to [0, 10] from v.min()
        to v.max()

    Notes
    -----
    Dipy supports a few colormaps for those who do not use Matplotlib, for
    more colormaps consider downloading Matplotlib (see matplotlib.org).
    """

    if name == 'jet':
        msg = 'Jet is a popular colormap but can often be misleading'
        msg += 'Use instead plasma, viridis, hot or inferno.'
        warn(msg, DeprecationWarning)

    if v.ndim > 1:
        msg = 'This function works only with 1d arrays. Use ravel()'
        raise ValueError(msg)

    if auto:
        v = np.interp(v, [v.min(), v.max()], [0, 1])
    else:
        v = np.clip(v, 0, 1)

    # For backwards compatibility with lowercase names
    newname = lowercase_cm_name.get(name) or name

    colormap = get_cmap(newname)
    if colormap is None:
        e_s = "Colormap {} is not yet implemented ".format(name)
        raise ValueError(e_s)

    rgba = colormap(v)
    rgb = rgba[:, :3].copy()
    return rgb


def create_random_colormap(v, rand_range=(0, 255), dim=3, alpha=255):
    """
    Create random colormap.
    """
    rgb = np.zeros([v, dim])
    if dim == 3:
        for i in range(v):
            for j in range(dim):
                rgb[i, j] = np.random.randint(rand_range[0], rand_range[1])
    elif dim == 4:
        for i in range(v):
            for j in range(dim-1):
                rgb[i, j] = np.random.randint(rand_range[0], rand_range[1])
            rgb[i, 3] = alpha

    return rgb
