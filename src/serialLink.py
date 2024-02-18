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


class ReceivedData:
    rovState = 0
    pitch = 0
    roll = 0
    yaw = 0
    accelX = 0
    accelY = 0
    accelZ = 0
    depth = 0
    battV = 0
    battA = 0
    waterTemp = 0
    internalTemp = 0
    errCode = 0

    def __str__(self) -> str:
        return f"Rov State: {self.rovState}, Pitch: {self.pitch}, Roll: {self.roll}, Yaw: {self.yaw}, AccelX: {self.accelX}, AccelY: {self.accelY}, AccelZ: {self.accelZ}, Depth: {self.depth}, BattV: {self.battV}, BattA: {self.battA}, WaterTemp: {self.waterTemp}, InternalTemp: {self.internalTemp}, ErrCode: {self.errCode}"


class CommandData(object):
    def __init__(self, rovState, heading, heave, strafe, surge, roliCamPitchControl, lightControl, buttons, linkCommand):
        self.rovState = rovState
        self.heading = heading
        self.heave = heave
        self.strafe = strafe
        self.surge = surge
        self.roliCamPitchControl = roliCamPitchControl
        self.lightControl = lightControl
        self.buttons = buttons
        self.linkCommand = linkCommand

    def __str__(self) -> str:
        return f"Rov State : {self.rovState}, Heading: {self.heading}, Heave: {self.heave}, Strafe: {self.strafe}, Surge: {self.surge}, RoliCamPitchControl: {self.roliCamPitchControl}, LightControl: {self.lightControl}, Buttons: {self.buttons}, LinkCommand: {self.linkCommand}"

def serialSend(link: txfer.SerialTransfer, commandData: CommandData):
    sendSize = 0
    sendSize = link.tx_obj(commandData.rovState, start_pos=sendSize, val_type_override="i")
    sendSize = link.tx_obj(commandData.heading, start_pos=sendSize, val_type_override="f")
    sendSize = link.tx_obj(commandData.heave, start_pos=sendSize, val_type_override="f")
    sendSize = link.tx_obj(commandData.strafe, start_pos=sendSize, val_type_override="f")
    sendSize = link.tx_obj(commandData.surge, start_pos=sendSize, val_type_override="f")
    sendSize = link.tx_obj(commandData.roliCamPitchControl, start_pos=sendSize, val_type_override="f")
    sendSize = link.tx_obj(commandData.lightControl, start_pos=sendSize, val_type_override="f")
    sendSize = link.tx_obj(commandData.buttons, start_pos=sendSize, val_type_override="f")
    sendSize = link.tx_obj(commandData.linkCommand, start_pos=sendSize, val_type_override="H")
    
    link.send(sendSize)


def serialReceive(link: txfer.SerialTransfer) -> ReceivedData:
    recSize = 0
    receivedData = ReceivedData()
    receivedData.rovState = link.rx_obj(obj_type=float, obj_byte_size=4, start_pos=recSize)
    recSize += 4
    receivedData.pitch = link.rx_obj(obj_type=float, obj_byte_size=4, start_pos=recSize)
    recSize += 4
    receivedData.roll = link.rx_obj(obj_type=float, obj_byte_size=4, start_pos=recSize)
    recSize += 4
    receivedData.yaw = link.rx_obj(obj_type=float, obj_byte_size=4, start_pos=recSize)
    recSize += 4
    receivedData.accelX = link.rx_obj(obj_type=float, obj_byte_size=4, start_pos=recSize)
    recSize += 4
    receivedData.accelY = link.rx_obj(obj_type=float, obj_byte_size=4, start_pos=recSize)
    recSize += 4
    receivedData.accelZ = link.rx_obj(obj_type=float, obj_byte_size=4, start_pos=recSize)
    recSize += 4
    receivedData.depth = link.rx_obj(obj_type=float, obj_byte_size=4, start_pos=recSize)
    recSize += 4
    receivedData.battV = link.rx_obj(obj_type=float, obj_byte_size=4, start_pos=recSize)
    recSize += 4
    receivedData.battA = link.rx_obj(obj_type=float, obj_byte_size=4, start_pos=recSize)
    recSize += 4
    receivedData.waterTemp = link.rx_obj(obj_type=float, obj_byte_size=4, start_pos=recSize)
    recSize += 4
    receivedData.internalTemp = link.rx_obj(obj_type=float, obj_byte_size=4, start_pos=recSize)
    recSize += 4
    receivedData.errCode = link.rx_obj(obj_type='H', obj_byte_size=2, start_pos=recSize)
    
    return receivedData

def sendArmCommand(link: txfer.SerialTransfer, armed: bool = True, commandData: CommandData = None, receivedData: ReceivedData = None):
    sendSize = 0    
    sendSize = link.tx_obj(commandData.rovState, start_pos=sendSize, val_type_override="f")
    sendSize = link.tx_obj(receivedData.yaw, start_pos=sendSize, val_type_override="f")
    sendSize = link.tx_obj(commandData.heave, start_pos=sendSize, val_type_override="f")
    sendSize = link.tx_obj(commandData.strafe, start_pos=sendSize, val_type_override="f")
    sendSize = link.tx_obj(commandData.surge, start_pos=sendSize, val_type_override="f")
    sendSize = link.tx_obj(commandData.roliCamPitchControl, start_pos=sendSize, val_type_override="f")
    sendSize = link.tx_obj(commandData.lightControl, start_pos=sendSize, val_type_override="f")
    sendSize = link.tx_obj(16 if armed else 2, start_pos=sendSize, val_type_override="f")
    sendSize = link.tx_obj(commandData.linkCommand, start_pos=sendSize, val_type_override="H")
    link.send(sendSize)
