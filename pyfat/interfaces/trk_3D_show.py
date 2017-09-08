# !/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
import numpy as np
import nibabel as nib
from nibabel import trackvis
from dipy.viz import actor, window, widget


# load brain_mask data
img = nib.load('/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/100206/Diffusion/T1w_acpc_dc_restore_brain.nii.gz')
# img = nib.load('/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/hcp_lh_projabs-2_FFA.nii.gz')
data = img.get_data()
shape = data.shape
affine = img.affine

fname = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/100206/Diffusion/l250_hcp_FFA_projabs-0-abs-2-1.trk'
streams, hdr = trackvis.read(fname, points_space="rasmm")
streamlines = [s[0] for s in streams]

world_coords = True
if not world_coords:
    from dipy.tracking.streamline import transform_streamlines
    streamlines = transform_streamlines(streamlines, np.linalg.inv(affine))

# Renderer
ren = window.Renderer()
stream_actor = actor.line(streamlines)

if not world_coords:
    image_actor = actor.slicer(data, affine=np.eye(4))
else:
    image_actor = actor.slicer(data, affine)

# opacity
slicer_opacity = 0.6
image_actor.opacity(slicer_opacity)

# add some slice
image_actor2 = image_actor.copy()
image_actor2.opacity(slicer_opacity)
image_actor2.display(None, image_actor2.shape[1]/2, None)
image_actor3 = image_actor.copy()
image_actor3.opacity(slicer_opacity)
image_actor3.display(image_actor3.shape[0]/2, None, None)

# connect the actors with the Render
ren.add(stream_actor)
ren.add(image_actor)
ren.add(image_actor2)
ren.add(image_actor3)

# initial showmanager
show_m = window.ShowManager(ren, size=(1200, 900))
show_m.initialize()

# change the position of the image_actor using a slider
def change_slice(obj, event):
    z = int(np.round(obj.get_value()))
    image_actor.display_extent(0, shape[0]-1, 0, shape[1]-1, z, z)

slicer = widget.slider(show_m.iren, show_m.ren, callback=change_slice, min_value=0, max_value=shape[2]-1, value=shape[2]/2, label="Move slice",
                       right_normalized_pos=(.98, 0.6), size=(120, 0), label_format="%0.1f", color=(1., 1., 1.), selected_color=(0.86, 0.33, 1.))

# change the position of the image_actor using a slider
def change_slice2(obj, event):
    y = int(np.round(obj.get_value()))
    image_actor2.display_extent(0, shape[0]-1, y, y, 0, shape[2]-1)

slicer2 = widget.slider(show_m.iren, show_m.ren, callback=change_slice2, min_value=0, max_value=shape[1]-1, value=shape[1]/2, label="Coronal slice",
                       right_normalized_pos=(.98, 0.3), size=(120, 0), label_format="%0.1f", color=(1., 1., 1.), selected_color=(0.86, 0.33, 1.))

# change the position of the image_actor using a slider
def change_slice3(obj, event):
    x = int(np.round(obj.get_value()))
    image_actor3.display_extent(x, x, 0, shape[1]-1, 0, shape[2]-1)

slicer3 = widget.slider(show_m.iren, show_m.ren, callback=change_slice3, min_value=0, max_value=shape[0]-1, value=shape[0]/2, label="Sagittal slice",
                       right_normalized_pos=(.98, 0.9), size=(120, 0), label_format="%0.1f", color=(1., 1., 1.), selected_color=(0.86, 0.33, 1.))

# change window size, the slider will change
global size
size = ren.GetSize()

def win_callback(obj, event):
    global size
    if size != obj.GetSize():
        slicer.place(ren)
        slicer2.place(ren)
        slicer3.place(ren)
        size = obj.GetSize()
show_m.initialize()

# interact with the available 3D and 2D objects
show_m.add_window_callback(win_callback)
show_m.render()
show_m.start()

ren.zoom(1.5)
ren.reset_clipping_range()

window.record(ren, out_path='l250_hcp_FFA_projabs-0-abs-2-1.png', size=(1200, 900), reset_camera=False)
del show_m
