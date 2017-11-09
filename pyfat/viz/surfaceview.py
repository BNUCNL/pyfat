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


def surface_roi(subjects_dir, subject_id, hemi, surf, coords):
    """
    Bring up the visualization.
    """
    brain = Brain(subjects_dir=subjects_dir, subject_id=subject_id, hemi=hemi, surf=surf)

    if hemi == 'both':
        hemi_both = ['lh', 'rh']
        for hemi_index in range(len(['lh', 'rh'])):
            brain.add_foci(coords[hemi_index+1], coords_as_verts=True, map_surface="inflated",
                           scale_factor=0.4, color="gold", hemi=hemi_both[hemi_index])
    elif hemi == 'lh':
        brain.add_foci(coords[1], coords_as_verts=True, map_surface="inflated", scale_factor=0.4, color="gold")
    else:
        brain.add_foci(coords[2], coords_as_verts=True, map_surface="inflated", scale_factor=0.4, color="gold")

    mlab.show()
