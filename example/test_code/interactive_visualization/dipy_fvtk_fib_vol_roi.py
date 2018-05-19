#!/usr/bin/env python
# -*- coding: utf-8 -*-

import vtk
import numpy as np
import nibabel as nib
from scipy.spatial.distance import cdist

from dipy.viz import actor, window, ui
from dipy.viz.interactor import CustomInteractorStyle
from dipy.tracking.streamline import set_number_of_points


class MouseInteractorStylePP(CustomInteractorStyle):
    def __init__(self, renderer, actors):
        CustomInteractorStyle.__init__(self)

        # Remember data we need for the interaction
        self.peaker = vtk.vtkPointPicker()
        self.renderer = renderer
        self.chosenActor = None
        self.actors = actors

    def OnRightButtonUp(self, obj, eventType):
        # When the right button is released, we stop the interaction
        self.chosenActor = None

        # Call parent interaction
        CustomInteractorStyle.on_right_button_up(self, obj, eventType)

    def OnRightButtonDown(self, obj, eventType):
        # The rightbutton can be used to pick up the actor.

        # Get the display mouse event position
        screen_pos = self.GetInteractor().GetEventPosition()

        # Use a picker to see which actor is under the mouse
        self.picker.Pick(screen_pos[0], screen_pos[1], 0, self.renderer)
        actor = self.picker.GetActor()

        # Is this a actor that we should interact with?
        if actor in self.actors:
            # Yes! Remember it.
            self.chosenActor = actor
            self.world_pos = self.picker.GetPickPosition()

        # Call parent interaction
        CustomInteractorStyle.on_right_button_down(self, obj, eventType)

    def OnMouseMove(self, obj, eventType):
        # Translate a choosen actor
        if self.chosenActor is not None:
            # Redo the same calculation as during OnRightButtonDown
            screen_pos = self.GetInteractor().GetEventPosition()
            self.picker.Pick(screen_pos[0], screen_pos[1], 0, self.renderer)
            actor_new = self.picker.GetActor()
            # print actor_new
            world_pos_new = self.picker.GetPickPosition()

            # Calculate the xy movement
            dx = world_pos_new[0] - self.world_pos[0]
            dy = world_pos_new[1] - self.world_pos[1]
            dz = world_pos_new[2] - self.world_pos[2]

            # Remember the new reference coordinate
            self.world_pos = world_pos_new

            # Shift the choosen actor in the xy plane
            x, y, z = self.chosenActor.GetPosition()
            self.chosenActor.SetPosition(x + dx, y + dy, z + dz)

            # Request a redraw
            self.GetInteractor().GetRenderWindow().Render()
            # self.renWin.Render()
        else:
            CustomInteractorStyle.on_mouse_move(self, obj, eventType)

    def SetInteractor(self, interactor):
        CustomInteractorStyle.SetInteractor(self, interactor)
        # The following three events are involved in the actors interaction.
        self.RemoveObservers('RightButtonPressEvent')
        self.RemoveObservers('RightButtonReleaseEvent')
        self.RemoveObservers('MouseMoveEvent')
        self.AddObserver('RightButtonPressEvent', self.OnRightButtonDown)
        self.AddObserver('RightButtonReleaseEvent', self.OnRightButtonUp)
        self.AddObserver('MouseMoveEvent', self.OnMouseMove)

fib_file = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/100206/Diffusion/SD/1M_20_01_20dynamic250_SD_Stream_occipital5.tck'
# fib_file = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
#            'response_dhollander/100206/Diffusion/SD/1M_20_01_20dynamic250_SD_Stream_single.tck'
vol_file = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/100206/Structure/T1w_acpc_dc_restore_brain1.25.nii.gz'
roi_file = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/100206/ROI/100206_CGC_roi1_L.nii.gz'
roi_file1 = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
            'response_dhollander/100206/ROI/100206_CGC_roi2_L.nii.gz'

fib = nib.streamlines.tck.TckFile.load(fib_file)
streamlines = fib.streamlines

# create a rendering renderer
ren = window.Renderer()
stream_actor = actor.line(streamlines)

roi = nib.load(roi_file)
roi_data = roi.get_data()
roi1 = nib.load(roi_file1)
roi1_data = roi1.get_data()
ROI_actor = actor.contour_from_roi(roi_data, affine=roi.affine, color=(1., 1., 0.), opacity=0.5)
ROI_actor1 = actor.contour_from_roi(roi1_data, affine=roi1.affine, color=(1., 1., 0.), opacity=0.5)


vol = nib.load(vol_file)
data = vol.get_data()
shape = vol.shape
affine = vol.affine

image_actor_z = actor.slicer(data, affine)
slicer_opacity = 0.6
image_actor_z.opacity(slicer_opacity)
image_actor_x = image_actor_z.copy()
image_actor_x.opacity(slicer_opacity)
x_midpoint = int(np.round(shape[0] / 2))
image_actor_x.display_extent(x_midpoint,
                             x_midpoint, 0,
                             shape[1] - 1,
                             0,
                             shape[2] - 1)

image_actor_y = image_actor_z.copy()
image_actor_y.opacity(slicer_opacity)
y_midpoint = int(np.round(shape[1] / 2))
image_actor_y.display_extent(0,
                             shape[0] - 1,
                             y_midpoint,
                             y_midpoint,
                             0,
                             shape[2] - 1)

# assign actor to the renderer
ren.add(stream_actor)
ren.add(ROI_actor)
ren.add(ROI_actor1)
ren.add(image_actor_z)
ren.add(image_actor_x)
ren.add(image_actor_y)
show_m = window.ShowManager(ren, size=(1200, 900), interactor_style=MouseInteractorStylePP(ren, [ROI_actor, ROI_actor1]))
show_m.initialize()

line_slider_z = ui.LineSlider2D(min_value=0,
                                max_value=shape[2] - 1,
                                initial_value=shape[2] / 2,
                                text_template="{value:.0f}",
                                length=140)

line_slider_x = ui.LineSlider2D(min_value=0,
                                max_value=shape[0] - 1,
                                initial_value=shape[0] / 2,
                                text_template="{value:.0f}",
                                length=140)

line_slider_y = ui.LineSlider2D(min_value=0,
                                max_value=shape[1] - 1,
                                initial_value=shape[1] / 2,
                                text_template="{value:.0f}",
                                length=140)

opacity_slider = ui.LineSlider2D(min_value=0.0,
                                 max_value=1.0,
                                 initial_value=slicer_opacity,
                                 length=140)


def change_slice_z(i_ren, obj, slider):
    z = int(np.round(slider.value))
    image_actor_z.display_extent(0, shape[0] - 1, 0, shape[1] - 1, z, z)


def change_slice_x(i_ren, obj, slider):
    x = int(np.round(slider.value))
    image_actor_x.display_extent(x, x, 0, shape[1] - 1, 0, shape[2] - 1)


def change_slice_y(i_ren, obj, slider):
    y = int(np.round(slider.value))
    image_actor_y.display_extent(0, shape[0] - 1, y, y, 0, shape[2] - 1)


def change_opacity(i_ren, obj, slider):
    slicer_opacity = slider.value
    image_actor_z.opacity(slicer_opacity)
    image_actor_x.opacity(slicer_opacity)
    image_actor_y.opacity(slicer_opacity)


line_slider_z.add_callback(line_slider_z.slider_disk,
                           "MouseMoveEvent",
                           change_slice_z)
line_slider_x.add_callback(line_slider_x.slider_disk,
                           "MouseMoveEvent",
                           change_slice_x)
line_slider_y.add_callback(line_slider_y.slider_disk,
                           "MouseMoveEvent",
                           change_slice_y)
opacity_slider.add_callback(opacity_slider.slider_disk,
                            "MouseMoveEvent",
                            change_opacity)

"""
We'll also create text labels to identify the sliders.
"""


def build_label(text):
    label = ui.TextBlock2D()
    label.message = text
    label.font_size = 18
    label.font_family = 'Arial'
    label.justification = 'left'
    label.bold = False
    label.italic = False
    label.shadow = False
    label.actor.GetTextProperty().SetBackgroundColor(0, 0, 0)
    label.actor.GetTextProperty().SetBackgroundOpacity(0.0)
    label.color = (1, 1, 1)

    return label


line_slider_label_z = build_label(text="Z Slice")
line_slider_label_x = build_label(text="X Slice")
line_slider_label_y = build_label(text="Y Slice")
opacity_slider_label = build_label(text="Opacity")

"""
Now we will create a ``panel`` to contain the sliders and labels.
"""

panel = ui.Panel2D(center=(1030, 120),
                   size=(300, 200),
                   color=(1, 1, 1),
                   opacity=0.1,
                   align="right")

panel.add_element(line_slider_label_x, 'relative', (0.1, 0.75))
panel.add_element(line_slider_x, 'relative', (0.65, 0.8))
panel.add_element(line_slider_label_y, 'relative', (0.1, 0.55))
panel.add_element(line_slider_y, 'relative', (0.65, 0.6))
panel.add_element(line_slider_label_z, 'relative', (0.1, 0.35))
panel.add_element(line_slider_z, 'relative', (0.65, 0.4))
panel.add_element(opacity_slider_label, 'relative', (0.1, 0.15))
panel.add_element(opacity_slider, 'relative', (0.65, 0.2))

show_m.ren.add(panel)
global size
size = ren.GetSize()


def win_callback(obj, event):
    global size
    if size != obj.GetSize():
        size_old = size
        size = obj.GetSize()
        size_change = [size[0] - size_old[0], 0]
        panel.re_align(size_change)


################################
# Call back function
def _computeFib(stream, spherewidget):
    stream = np.array([f for f in set_number_of_points(stream, 20)])
    center = np.array([spherewidget.GetCenter()])
    dist = np.array([cdist(stream[i], center).min() for i in xrange(len(stream))])
    new_stream = stream[dist <= spherewidget.GetRadius()]

    return new_stream


def computeFibCallback(obj, event):
    global streamlines, stream_actor
    new_f = _computeFib(streamlines, obj)
    try:
        ren.RemoveActor(stream_actor)
        stream_actor = actor.line(new_f)
        ren.add(stream_actor)
    except:
        pass

# enable user interface interactor
iren = show_m.iren
renWin = show_m.window
renWin.AddRenderer(ren)

# A Sphere widget
sphereWidget = vtk.vtkSphereWidget()
sphereWidget.SetCenter(3.98, -30.94, 9.16)
sphereWidget.SetRadius(5)
sphereWidget.SetInteractor(iren)
sphereWidget.SetRepresentationToSurface()
# sphereWidget.SetKeyPressActivationValue('k')  # By default, the key press activation value is 'i'.
# sphereWidget.On()

# Connect the event to a function
sphereWidget.AddObserver("InteractionEvent", computeFibCallback)
######################################

show_m.initialize()
ren.zoom(1.5)
ren.reset_clipping_range()
show_m.add_window_callback(win_callback)
show_m.render()
show_m.start()
