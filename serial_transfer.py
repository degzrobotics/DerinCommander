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

from pySerialTransfer import pySerialTransfer as txfer
from Controller import *


class Sensors:
    roll = 0
    pitch = 0
    yaw = 0
    depth = 0
    batteryVoltage = 0
    systemCurrent = 0
    waterTemp = 0
    internalTemp = 0

    def __str__(self) -> str:
        return f"roll: {self.roll}, pitch: {self.pitch}, yaw: {self.yaw}, depth: {self.depth}, batteryVoltage: {self.batteryVoltage}, systemCurrent: {self.systemCurrent} waterTemp: {self.waterTemp}, internalTemp: {self.internalTemp}"


class ControllerData(object):
    def __init__(self, buttons, leftTrigger, rightTrigger, leftThumbX, leftThumbY, rightThumbX, rightThumbY):
        self.buttons = buttons
        self.leftTrigger = leftTrigger
        self.rightTrigger = rightTrigger
        self.leftThumbX = leftThumbX
        self.leftThumbY = leftThumbY
        self.rightThumbX = rightThumbX
        self.rightThumbY = rightThumbY


def serialSend(link: txfer.SerialTransfer, controllerState: ControllerState, speedMultiplier: float):
    sendSize = 0
    controllerData = ControllerData(controllerState.buttons, int(controllerState.leftTrigger), int(controllerState.rightTrigger),
                                    int(controllerState.leftThumbX * speedMultiplier), int(controllerState.leftThumbY * speedMultiplier), int(controllerState.rightThumbX * speedMultiplier), int(controllerState.rightThumbY * speedMultiplier))
    sendSize = link.tx_obj(controllerData.buttons, start_pos=sendSize)
    sendSize = link.tx_obj(
        controllerData.leftTrigger, start_pos=sendSize)
    sendSize = link.tx_obj(
        controllerData.rightTrigger, start_pos=sendSize)
    sendSize = link.tx_obj(
        controllerData.leftThumbX, start_pos=sendSize)
    sendSize = link.tx_obj(
        controllerData.leftThumbY, start_pos=sendSize)
    sendSize = link.tx_obj(
        controllerData.rightThumbX, start_pos=sendSize)
    sendSize = link.tx_obj(
        controllerData.rightThumbY, start_pos=sendSize)

    link.send(sendSize)


def serialReceive(link: txfer.SerialTransfer) -> Sensors:
    recSize = 0
    sensors = Sensors()
    sensors.roll = link.rx_obj(obj_type=type(
        Sensors.roll), obj_byte_size=4, start_pos=recSize)
    sensors.pitch = link.rx_obj(obj_type=type(
        Sensors.pitch), obj_byte_size=4, start_pos=recSize + 4)
    sensors.yaw = link.rx_obj(obj_type=type(
        Sensors.yaw), obj_byte_size=4, start_pos=recSize + 8)
    sensors.depth = link.rx_obj(obj_type=type(
        Sensors.depth), obj_byte_size=4, start_pos=recSize + 12)
    sensors.batteryVoltage = link.rx_obj(obj_type=type(
        Sensors.batteryVoltage), obj_byte_size=4, start_pos=recSize + 16)
    sensors.systemCurrent = link.rx_obj(obj_type=type(
        Sensors.systemCurrent), obj_byte_size=4, start_pos=recSize + 20)
    sensors.waterTemp = link.rx_obj(obj_type=type(
        Sensors.waterTemp), obj_byte_size=4, start_pos=recSize + 24)
    sensors.internalTemp = link.rx_obj(obj_type=type(
        Sensors.internalTemp), obj_byte_size=4, start_pos=recSize + 28)
    return sensors
