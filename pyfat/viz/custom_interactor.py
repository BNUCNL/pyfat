#!/usr/bin/env python
# -*- coding: utf-8 -*-

import vtk
from dipy.viz.interactor import CustomInteractorStyle


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
            print actor_new
            world_pos_new = self.picker.GetPickPosition()
            print world_pos_new

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
