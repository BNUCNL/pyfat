#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import vtk
import numpy as np
import nibabel as nib
from scipy.spatial.distance import cdist

from dipy.viz import actor, window, ui
from dipy.data import read_viz_icons, fetch_viz_icons
from dipy.tracking.fbcmeasures import FBCMeasures
from dipy.tracking.streamline import set_number_of_points
from dipy.denoise.enhancement_kernel import EnhancementKernel

from pyfat.viz.custom_interactor import MouseInteractorStylePP
from pyfat.algorithm.fiber_selection import select_by_vol_roi
from pyfat.io.save import save_tck


# fib_file = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
#            'response_dhollander/subjects/100206/Diffusion/SD/1M_20_01_20dynamic250_SD_Stream_occipital5.tck'
# fib_file = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
#            'response_dhollander/subjects/100206/Diffusion/SD/100206_FP.tck'
vol_file = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/subjects/100408/T1w/T1w_acpc_dc_restore_brain1.25.nii.gz'
roi_file = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/subjects/100408/ROI/100408_L_Occipital.nii.gz'
roi_file1 = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
            'response_dhollander/subjects/100408/ROI/100408_R_Occipital.nii.gz'
# roi_vis = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
#           'response_dhollander/subjects/100408/Structure/Native_cytoMPM_thr25_vis.nii.gz'
fib_file = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/subjects/100408/result/result20vs45/cc_20fib_lr1.5_new_SD_Stream_hierarchical_single_cc.tck'

fib = nib.streamlines.tck.TckFile.load(fib_file)
streamlines = fib.streamlines
print len(streamlines)

# # Compute lookup table
# D33 = 1.0
# D44 = 0.02
# t = 1
# k = EnhancementKernel(D33, D44, t)
#
# # Apply FBC measures
# fbc = FBCMeasures(streamlines, k)
#
# # Calculate LFBC for original fibers
# fbc_sl_orig, clrs_orig, rfbc_orig = fbc.get_points_rfbc_thresholded(0, emphasis=0.01)
# print len(fbc_sl_orig)
# # Apply a threshold on the RFBC to remove spurious fibers
# fbc_sl_thres, clrs_thres, rfbc_thres = fbc.get_points_rfbc_thresholded(0.125, emphasis=0.01)
# print len(fbc_sl_thres)

# # create a rendering renderer
# ren = window.Renderer()
# stream_actor = actor.line(streamlines)

roi_img = nib.load(roi_file)
roi1_img = nib.load(roi_file1)
####################################################
# roi_vis = nib.load(roi_vis)


def set_viz_roi(roi_img, mask=False):
    roi_data = roi_img.get_data()
    if mask:
        roi_data[roi_data > 0] = 1
    label = list(set(roi_data[roi_data.nonzero()]))
    roi_list = []
    for i in xrange(len(label)):
        roi = np.zeros(roi_data.shape)
        roi[roi_data == label[i]] = i + 1
        roi_list.append(roi)

    return roi_list, roi_img.affine


def create_roi_actor(roi_list, affine, opacity=0.8):
    roi_actor_list = []
    for i in xrange(len(roi_list)):
        random = np.random.RandomState(i)
        color = random.uniform(0., 1., size=3)
        print color
        i_actor = actor.contour_from_roi(roi_list[i], affine=affine, color=color, opacity=opacity)
        roi_actor_list.append(i_actor)

    return roi_actor_list

roi, roi_affine = set_viz_roi(roi_img, mask=True)
roi1, roi1_affine = set_viz_roi(roi1_img, mask=True)
roi_actor = create_roi_actor(roi, roi_affine)
roi1_actor = create_roi_actor(roi1, roi1_affine)

# roi_viz, roi_viz_affine = set_viz_roi(roi_vis)
# roi_viz_actor = create_roi_actor(roi_viz, roi_viz_affine)

streamlines = select_by_vol_roi(streamlines, roi[0], roi_img.affine)
print len(streamlines)
# create a rendering renderer
ren = window.Renderer()
stream_actor = actor.line(streamlines)
stream_init_actor = actor.line(streamlines, (1.0, 0.0, 0.0))
vol = nib.load(vol_file)


def create_image_actor(vol, opacity=0.6):
    data = vol.get_data()
    shape = vol.shape
    affine = vol.affine

    image_actor_z = actor.slicer(data, affine)
    slicer_opacity = opacity
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

    return image_actor_x, image_actor_y, image_actor_z


def createCubeActor(bounds=None, size=None, center=None, color=None, opacity=0.8):
    cube = window.vtk.vtkCubeSource()
    if bounds is not None:
        cube.SetBounds(bounds)
    if size is not None:
        cube.SetXLength(size[0])
        cube.SetYLength(size[1])
        cube.SetZLength(size[2])
    if center is not None:
        cube.SetCenter(*center)

    cube_mapper = window.vtk.vtkPolyDataMapper()
    cube_mapper.SetInputConnection(cube.GetOutputPort())
    cube_actor = window.vtk.vtkActor()
    cube_actor.SetMapper(cube_mapper)

    if color is not None:
        cube_actor.GetProperty().SetColor(color)
    if opacity is not None:
        cube_actor.GetProperty().SetOpacity(opacity)
    return cube_actor


image_actor_x, image_actor_y, image_actor_z = create_image_actor(vol)
# assign actor to the renderer
ren.add(stream_actor)

color = roi_actor[0].GetProperty().GetColor()
cube_actor = createCubeActor(roi_actor[0].GetBounds(), color=color)
ren.add(cube_actor)
print roi_actor[0]
#########################################
for act in roi_actor:
    ren.add(act)
print roi_actor[0].GetBounds()
# for act1 in roi1_actor:
#     ren.add(act1)
# for act_viz in roi_viz_actor:
#     ren.add(act_viz)
#########################################
ren.add(image_actor_z)
ren.add(image_actor_x)
ren.add(image_actor_y)
show_m = window.ShowManager(ren, size=(1200, 900), interactor_style=MouseInteractorStylePP(ren, [cube_actor]))
show_m.initialize()


def line_slider(shape, opacity=0.6):
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
                                     initial_value=opacity,
                                     length=140)

    return line_slider_x, line_slider_y, line_slider_z, opacity_slider

line_slider_x, line_slider_y, line_slider_z, opacity_slider = line_slider(vol.shape)
shape = vol.shape


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


def create_panel(line_slider_x, line_slider_label_x, line_slider_y, line_slider_label_y,
                 line_slider_z, line_slider_label_z, opacity_slider, opacity_slider_label):
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

    return panel

panel = create_panel(line_slider_x, line_slider_label_x, line_slider_y, line_slider_label_y,
                     line_slider_z, line_slider_label_z, opacity_slider, opacity_slider_label)
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
        ren.RemoveActor(stream_init_actor)
        # random = np.random.RandomState()
        color = np.random.uniform(0., 1., size=3)
        stream_actor = actor.line(new_f, color)
        ren.add(stream_actor)
    except:
        pass

# enable user interface interactor
iren = show_m.iren
renWin = show_m.window
renWin.AddRenderer(ren)


# A Sphere widget
def create_sphereWidget(center=(3.98, -30.94, 9.16), radius=5, opacity=0.8):
    sphereWidget = vtk.vtkSphereWidget()
    sphereWidget.SetCenter(center)
    sphereWidget.SetRadius(radius)
    sphereWidget.GetSphereProperty().SetOpacity(opacity)
    sphereWidget.SetRepresentationToSurface()
    # sphereWidget.SetKeyPressActivationValue('k')  # By default, the key press activation value is 'i'.
    # sphereWidget.On()
    return sphereWidget

center_x = image_actor_x.GetSliceNumber()
center_y = image_actor_y.GetSliceNumber()
center_z = image_actor_z.GetSliceNumber()
center = vol.affine.dot([center_x, center_y, center_z, 1])[:3]
print center
sphereWidget = create_sphereWidget(center=center)
sphereWidget.SetInteractor(iren)
# Connect the event to a function
# sphereWidget.AddObserver("InteractionEvent", computeFibCallback)
######################################
######################################

"""
Buttons
=======

We first fetch the icons required for making the buttons.
"""

fetch_viz_icons()

"""
Add the icon filenames to a dict.
"""

icon_file = dict()
icon_file['save'] = read_viz_icons(fname='floppy-disk.png')
icon_file['savefinish'] = read_viz_icons(fname='checkmark.png')

"""
Create a button through our API.
"""

button_example = ui.Button2D(icon_fnames=icon_file)

"""
We now add some click listeners.
"""


# def left_mouse_button_click(i_ren, obj, button):
#     print("Left Button Clicked")
#
#
# def left_mouse_button_drag(i_ren, obj, button):
#     print ("Left Button Dragged")

def modify_left_button_callback(i_ren, obj, button):
    print button.current_icon_id
    print button.current_icon_name
    if button.current_icon_id == 0:
        new_f = _computeFib(streamlines, sphereWidget)
        save_tck(new_f, header=fib.header, data_per_streamline=fib.tractogram.data_per_streamline,
                 data_per_point=fib.tractogram.data_per_point, affine_to_rasmm=fib.tractogram.affine_to_rasmm,
                 out_path=os.path.join(os.getcwd(), 'result', '%s.tck') % text.text)
    if button.current_icon_id == 1:
        pass

    button.next_icon()
    i_ren.force_render()
print __file__
print os.getcwd()
# button_example.on_left_mouse_button_drag = left_mouse_button_drag
# button_example.on_left_mouse_button_pressed = left_mouse_button_click
button_example.on_left_mouse_button_pressed = modify_left_button_callback


# def right_mouse_button_drag(i_ren, obj, button):
#     print("Right Button Dragged")
#
#
# def right_mouse_button_click(i_ren, obj, button):
#     print ("Right Button Clicked")
#
#
# button_example.on_right_mouse_button_drag = right_mouse_button_drag
# button_example.on_right_mouse_button_pressed = right_mouse_button_click


icon_files = dict()
icon_files['stop'] = read_viz_icons(fname='stop2.png')
icon_files['play'] = read_viz_icons(fname='play3.png')
"""
Let's have another button.
"""

second_button_example = ui.Button2D(icon_fnames=icon_files)

"""
This time, we will call the built in `next_icon` method
via a callback that is triggered on left click.
"""


def modify_button_callback(i_ren, obj, button):
    print button.current_icon_id
    print button.current_icon_name
    if button.current_icon_id == 0:
        sphereWidget.AddObserver("InteractionEvent", computeFibCallback)
    if button.current_icon_id == 1:
        ren.RemoveActor(stream_actor)
        sphereWidget.RemoveAllObservers()
        ren.add(stream_init_actor)

    button.next_icon()
    i_ren.force_render()


second_button_example.on_left_mouse_button_pressed = modify_button_callback

"""
Panels
======

Simply create a panel and add elements to it.
"""

panel2 = ui.Panel2D(center=(440, 90), size=(300, 150), color=(1, 1, 1),
                   align="right")
panel2.add_element(button_example, 'relative', (0.2, 0.2))
panel2.add_element(second_button_example, 'absolute', (480, 100))


"""
TextBox
=======
"""

text = ui.TextBox2D(height=3, width=10)


def key_press(i_ren, obj, textbox_object):
    """ Key press handler for textbox

    Parameters
    ----------
    i_ren: :class:`CustomInteractorStyle`
    obj: :class:`vtkActor`
        The picked actor
    textbox_object: :class:`TextBox2D`

    """
    key = i_ren.event.key
    print key
    is_done = textbox_object.handle_character(key)
    print is_done
    if is_done:
        i_ren.remove_active_prop(textbox_object.actor.get_actor())
        print textbox_object.text

    i_ren.force_render()

text.on_key_press = key_press

"""
2D Line Slider
==============
"""


def translate_green_cube(i_ren, obj, slider):
    value = slider.value
    roi_actor[0].SetPosition(value, 0, 0)


line_slider_c = ui.LineSlider2D(initial_value=-2,
                              min_value=-5, max_value=5)

line_slider_c.add_callback(line_slider_c.slider_disk,
                         "MouseMoveEvent",
                         translate_green_cube)

"""
2D Disk Slider
==============
"""


def rotate_red_cube(i_ren, obj, slider):
    angle = slider.value
    roi1_actor[0].RotateY(0.005 * angle)


disk_slider = ui.DiskSlider2D()
disk_slider.set_center((200, 200))
disk_slider.add_callback(disk_slider.handle,
                         "MouseMoveEvent",
                         rotate_red_cube)

"""
2D File Select Menu
==============
"""

file_select_menu = ui.FileSelectMenu2D(size=(300, 500),
                                       position=(160, 595),
                                       font_size=16,
                                       extensions=["tck", "gz"],
                                       directory_path=os.getcwd(),
                                       parent=None)
print file_select_menu.text_item_list


def left_button_clicked(i_ren, obj, file_select_text):
    """ A callback to handle left click for this UI element.

    Parameters
    ----------
    i_ren: :class:`CustomInteractorStyle`
    obj: :class:`vtkActor`
        The picked actor
    file_select_text: :class:`FileSelectMenuText2D`

    """

    if file_select_text.file_type == "directory":
        file_select_text.file_select.select_file(file_name="")
        file_select_text.file_select.window_offset = 0
        file_select_text.file_select.current_directory = os.path.abspath(
            os.path.join(file_select_text.file_select.current_directory,
                         file_select_text.text_actor.message))
        file_select_text.file_select.window = 0
        file_select_text.file_select.fill_text_actors()
        print "----------------------"
    else:
        file_select_text.file_select.select_file(
            file_name=file_select_text.file_name)
        file_select_text.file_select.fill_text_actors()
        file_select_text.mark_selected()
        print "+++++++++++++++++++++++"
        data_path = os.path.join(file_select_text.file_select.current_directory, file_select_text.file_name)
        suffix = os.path.split(data_path)[-1].split('.')[-1]
        print
        if suffix == 'tck':
            fibs = nib.streamlines.tck.TckFile.load(data_path)
            ac = actor.line(fibs.streamlines)
            ren.add(ac)
        if suffix == 'gz':
            img = nib.load(data_path)
            im = actor.contour_from_roi(img.get_data(), affine=img.affine)
            ren.add(im)

    i_ren.force_render()
    i_ren.event.abort()  # Stop propagating the event.

for text_actor in file_select_menu.text_item_list:
    text_actor.on_left_mouse_button_clicked = left_button_clicked

show_m.ren.add(panel2)
show_m.ren.add(text)
# show_m.ren.add(line_slider_c)
# show_m.ren.add(disk_slider)
show_m.ren.add(file_select_menu)
show_m.ren.reset_camera()
show_m.ren.azimuth(30)
###################################################

show_m.initialize()
ren.zoom(1.5)
ren.reset_clipping_range()
show_m.add_window_callback(win_callback)
show_m.render()
show_m.start()
