"""
  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import logging
import sys

if sys.platform != 'darwin':
    from XInput import *


class ControllerState:
    def __init__(self, buttons, leftTrigger, rightTrigger, leftThumbX, leftThumbY, rightThumbX, rightThumbY):
        self.buttons = buttons
        self.leftTrigger = leftTrigger
        self.rightTrigger = rightTrigger
        self.leftThumbX = leftThumbX
        self.leftThumbY = leftThumbY
        self.rightThumbX = rightThumbX
        self.rightThumbY = rightThumbY

    def __str__(self) -> str:
        return f"buttons: {self.buttons}, leftTrigger: {self.leftTrigger}, rightTrigger: {self.rightTrigger}, leftThumbX: {self.leftThumbX}, leftThumbY: {self.leftThumbY}, rightThumbX: {self.rightThumbX}, rightThumbY: {self.rightThumbY}"


class Controller:
    def __init__(self) -> None:
        self.state = ControllerState(0, 0, 0, 0, 0, 0, 0)
        self.isConnected = False

    def setDeadzone(trigger, leftThumb, rightThumb):
        if sys.platform == 'darwin':
            return
        set_deadzone(DEADZONE_TRIGGER, trigger)
        set_deadzone(DEADZONE_LEFT_THUMB, leftThumb)
        set_deadzone(DEADZONE_RIGHT_THUMB, rightThumb)

    def update(self):
        if sys.platform == 'darwin':
            return
        events = get_events()
        for event in events:
            self._updateHelper(event)

            logging.debug(self.state)

    def _updateHelper(self, event):
        if sys.platform == 'darwin':
            return
        if event.type == EVENT_CONNECTED:
            logging.info("Controller Connected")
            self.isConnected = True
        elif event.type == EVENT_DISCONNECTED:
            logging.info("Controller Disconnected")
            self.isConnected = False
        elif event.type == EVENT_STICK_MOVED:
            if event.stick == LEFT:
                self.state.leftThumbX = event.x * 250
                self.state.leftThumbY = event.y * 250
            elif event.stick == RIGHT:
                self.state.rightThumbX = event.x * 250
                self.state.rightThumbY = event.y * 250
        elif event.type == EVENT_TRIGGER_MOVED:
            if event.trigger == LEFT:
                self.state.leftTrigger = event.value * 250
            elif event.trigger == RIGHT:
                self.state.rightTrigger = event.value * 250
        elif event.type == EVENT_BUTTON_PRESSED:
            if event.button == "LEFT_THUMB":
                self.state.buttons = self.state.buttons | BUTTON_LEFT_THUMB
            elif event.button == "RIGHT_THUMB":
                self.state.buttons = self.state.buttons | BUTTON_RIGHT_THUMB
            elif event.button == "LEFT_SHOULDER":
                self.state.buttons = self.state.buttons | BUTTON_LEFT_SHOULDER
            elif event.button == "RIGHT_SHOULDER":
                self.state.buttons = self.state.buttons | BUTTON_RIGHT_SHOULDER
            elif event.button == "BACK":
                self.state.buttons = self.state.buttons | BUTTON_BACK
            elif event.button == "START":
                self.state.buttons = self.state.buttons | BUTTON_START
            elif event.button == "DPAD_LEFT":
                self.state.buttons = self.state.buttons | BUTTON_DPAD_LEFT
            elif event.button == "DPAD_RIGHT":
                self.state.buttons = self.state.buttons | BUTTON_DPAD_RIGHT
            elif event.button == "DPAD_UP":
                self.state.buttons = self.state.buttons | BUTTON_DPAD_UP
            elif event.button == "DPAD_DOWN":
                self.state.buttons = self.state.buttons | BUTTON_DPAD_DOWN
            elif event.button == "A":
                self.state.buttons = self.state.buttons | BUTTON_A
            elif event.button == "B":
                self.state.buttons = self.state.buttons | BUTTON_B
            elif event.button == "X":
                self.state.buttons = self.state.buttons | BUTTON_X
            elif event.button == "Y":
                self.state.buttons = self.state.buttons | BUTTON_Y
        elif event.type == EVENT_BUTTON_RELEASED:
            if event.button == "LEFT_THUMB":
                self.state.buttons = self.state.buttons & (~ BUTTON_LEFT_THUMB)
            elif event.button == "RIGHT_THUMB":
                self.state.buttons = self.state.buttons & (
                    ~ BUTTON_RIGHT_THUMB)
            elif event.button == "LEFT_SHOULDER":
                self.state.buttons = self.state.buttons & (
                    ~ BUTTON_LEFT_SHOULDER)
            elif event.button == "RIGHT_SHOULDER":
                self.state.buttons = self.state.buttons & (
                    ~ BUTTON_RIGHT_SHOULDER)
            elif event.button == "BACK":
                self.state.buttons = self.state.buttons & (~ BUTTON_BACK)
            elif event.button == "START":
                self.state.buttons = self.state.buttons & (~ BUTTON_START)
            elif event.button == "DPAD_LEFT":
                self.state.buttons = self.state.buttons & (~ BUTTON_DPAD_LEFT)
            elif event.button == "DPAD_RIGHT":
                self.state.buttons = self.state.buttons & (~ BUTTON_DPAD_RIGHT)
            elif event.button == "DPAD_UP":
                self.state.buttons = self.state.buttons & (~ BUTTON_DPAD_UP)
            elif event.button == "DPAD_DOWN":
                self.state.buttons = self.state.buttons & (~ BUTTON_DPAD_DOWN)
            elif event.button == "A":
                self.state.buttons = self.state.buttons & (~ BUTTON_A)
            elif event.button == "B":
                self.state.buttons = self.state.buttons & (~ BUTTON_B)
            elif event.button == "X":
                self.state.buttons = self.state.buttons & (~ BUTTON_X)
            elif event.button == "Y":
                self.state.buttons = self.state.buttons & (~ BUTTON_Y)
