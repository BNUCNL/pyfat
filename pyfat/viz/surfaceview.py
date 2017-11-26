# !/usr/bin/python
# -*- coding: utf-8 -*-

"""
====================
Plot Activation Foci
====================

Plot spheroids at positions on the surface manifold
according to coordinates or vertex ids.

"""
from surfer import Brain
from mayavi import mlab


def surface_roi(subjects_dir, subject_id, hemi, surf, alpha, coords):
    """
    Bring up the visualization.
    """
    brain = Brain(subjects_dir=subjects_dir, subject_id=subject_id, hemi=hemi, surf=surf, alpha=alpha)

    if hemi == 'both':
        hemi_both = ['lh', 'rh']
        for hemi_index in range(len(['lh', 'rh'])):
            brain.add_foci(coords[hemi_index+1], coords_as_verts=True, map_surface="inflated",
                           scale_factor=0.4, color="gold", hemi=hemi_both[hemi_index])
    elif hemi == 'lh':
        brain.add_foci(coords[1], coords_as_verts=True, map_surface="inflated",
                       scale_factor=0.4, color="gold", hemi='lh')
    else:
        brain.add_foci(coords[2], coords_as_verts=True, map_surface="inflated",
                       scale_factor=0.4, color="gold", hemi='rh')

    mlab.show()


def surface_streamlines_roi(subjects_dir, subject_id, hemi, surf, alpha, coords, streamlines=None):
    """
    Bring up the visualization.
    """
    brain = Brain(subjects_dir=subjects_dir, subject_id=subject_id, hemi=hemi, surf=surf, alpha=alpha)

    if hemi == 'both':
        hemi_both = ['lh', 'rh']
        for hemi_index in range(len(['lh', 'rh'])):
            brain.add_foci(coords[hemi_index], coords_as_verts=True, map_surface="inflated",
                           scale_factor=0.4, color="gold", hemi=hemi_both[hemi_index])
        if streamlines is not None:
            for st in streamlines:
                brain.add_foci(st[st[:, 0] < 0], hemi='lh', scale_factor=0.4, color='red')
                brain.add_foci(st[st[:, 0] > 0], hemi='rh', scale_factor=0.4, color='red')

    elif hemi == 'lh':
        brain.add_foci(coords[0], coords_as_verts=True, map_surface="inflated",
                       scale_factor=0.4, color="gold", hemi='lh')
    else:
        brain.add_foci(coords[1], coords_as_verts=True, map_surface="inflated",
                       scale_factor=0.4, color="gold", hemi='rh')

    mlab.show()


def surface_streamlines_map(subjects_dir, subject_id, hemi, surf, alpha, coords):
    """
    Bring up the visualization.
    """
    brain = Brain(subjects_dir=subjects_dir, subject_id=subject_id, hemi=hemi, surf=surf, alpha=alpha)

    if hemi == 'both':
        hemi_both = ['lh', 'rh']
        for hemi_index in range(len(['lh', 'rh'])):
            brain.add_overlay(coords[hemi_index], min=coords[hemi_index][coords[hemi_index] > 0].min(),
                              max=coords[hemi_index].max(), sign='pos', hemi=hemi_both[hemi_index])

    elif hemi == 'lh':
        brain.add_overlay(coords[0], min=coords[0][coords[0] > 0].min(),
                          max=coords[0].max(), sign='pos', hemi='lh', name='lh')

    else:
        brain.add_overlay(coords[1], min=coords[1][coords[1] > 0].min(),
                          max=coords[1].max(), sign='pos', hemi='rh', name='rh')

    mlab.show()


def surface_roi_contour(subjects_dir, subject_id, hemi, surf, alpha, coords, region):
    """
    Bring up the visualization.
    Add the contour of region.
    """
    brain = Brain(subjects_dir=subjects_dir, subject_id=subject_id, hemi=hemi, surf=surf, alpha=alpha)

    if hemi == 'both':
        brain.add_contour_overlay(region[0], min=region[0].min(), max=region[0].max(), n_contours=2, line_width=1.5,
                                  colormap="YlOrRd_r", hemi='lh', remove_existing=True, colorbar=False)
        brain.add_overlay(coords[0], min=coords[0][coords[0] > 0].min(),
                          max=coords[0].max(), sign='pos', hemi='lh', name='lh')
        brain.add_contour_overlay(region[1], min=region[1].min(), max=region[1].max(), n_contours=2, line_width=1.5,
                                  colormap="YlOrRd_r", hemi='rh', remove_existing=False, colorbar=False)
        brain.add_overlay(coords[1], min=coords[1][coords[1] > 0].min(),
                          max=coords[1].max(), sign='pos', hemi='rh', name='rh')
    elif hemi == 'lh':
        brain.add_contour_overlay(region[0], min=region[0].min(),
                                  max=region[0].max(), n_contours=2, line_width=1.5,
                                  colormap="YlOrRd_r", hemi='lh', remove_existing=True, colorbar=False)
        brain.add_overlay(coords[0], min=coords[0][coords[0] > 0].min(),
                          max=coords[0].max(), sign='pos', hemi='lh', name='lh')
    else:
        brain.add_contour_overlay(region[1], min=region[1].min(),
                                  max=region[1].max(), n_contours=2, line_width=1.5,
                                  colormap="YlOrRd_r", hemi='rh', remove_existing=True, colorbar=False)
        brain.add_overlay(coords[1], min=coords[1][coords[1] > 0].min(),
                          max=coords[1].max(), sign='pos', hemi='rh', name='rh')

    mlab.show()
