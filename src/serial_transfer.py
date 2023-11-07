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


class Sensors:
    def __init__(self):
        self.pitch = 0.0
        self.roll = 0.0
        self.yaw = 0.0
        self.accelX = 0.0
        self.accelY = 0.0
        self.accelZ = 0.0
        self.depth = 0.0
        self.battV = 0.0
        self.battA = 0.0
        self.waterTemp = 0.0
        self.internalTemp = 0.0
        self.errCode = 0

    def __str__(self) -> str:
        return f"Pitch: {self.pitch}, Roll: {self.roll}, Yaw: {self.yaw}, AccelX: {self.accelX}, AccelY: {self.accelY}, AccelZ: {self.accelZ}, Depth: {self.depth}, BattV: {self.battV}, BattA: {self.battA}, WaterTemp: {self.waterTemp}, InternalTemp: {self.internalTemp}, ErrCode: {self.errCode}"


class CommandData(object):
    def __init__(self, heading, heave, strafe, surge, roliCamPitchControl, lightControl, buttons, linkCommand):
        self.heading = heading
        self.heave = heave
        self.strafe = strafe
        self.surge = surge
        self.roliCamPitchControl = roliCamPitchControl
        self.lightControl = lightControl
        self.buttons = buttons
        self.linkCommand = linkCommand

    def __str__(self) -> str:
        return f"Heading: {self.heading}, Heave: {self.heave}, Strafe: {self.strafe}, Surge: {self.surge}, RoliCamPitchControl: {self.roliCamPitchControl}, LightControl: {self.lightControl}, Buttons: {self.buttons}, LinkCommand: {self.linkCommand}"

def serialSend(link: txfer.SerialTransfer, commandData: CommandData):
    sendSize = 0

    sendSize = link.tx_obj(commandData.heading, start_pos=sendSize, val_type_override="f")
    sendSize = link.tx_obj(commandData.heave, start_pos=sendSize, val_type_override="f")
    sendSize = link.tx_obj(commandData.strafe, start_pos=sendSize, val_type_override="f")
    sendSize = link.tx_obj(commandData.surge, start_pos=sendSize, val_type_override="f")
    sendSize = link.tx_obj(commandData.roliCamPitchControl, start_pos=sendSize, val_type_override="f")
    sendSize = link.tx_obj(commandData.lightControl, start_pos=sendSize, val_type_override="f")
    sendSize = link.tx_obj(commandData.buttons, start_pos=sendSize, val_type_override="f")
    sendSize = link.tx_obj(commandData.linkCommand, start_pos=sendSize, val_type_override="H")
    
    print(link.txBuff) 
    
    link.send(sendSize)


def serialReceive(link: txfer.SerialTransfer) -> Sensors:
    recSize = 0
    sensors = Sensors()
    sensors.pitch = link.rx_obj(obj_type=float, obj_byte_size=4, start_pos=recSize)
    recSize += 4
    sensors.roll = link.rx_obj(obj_type=float, obj_byte_size=4, start_pos=recSize)
    recSize += 4
    sensors.yaw = link.rx_obj(obj_type=float, obj_byte_size=4, start_pos=recSize)
    recSize += 4
    sensors.accelX = link.rx_obj(obj_type=float, obj_byte_size=4, start_pos=recSize)
    recSize += 4
    sensors.accelY = link.rx_obj(obj_type=float, obj_byte_size=4, start_pos=recSize)
    recSize += 4
    sensors.accelZ = link.rx_obj(obj_type=float, obj_byte_size=4, start_pos=recSize)
    recSize += 4
    sensors.depth = link.rx_obj(obj_type=float, obj_byte_size=4, start_pos=recSize)
    recSize += 4
    sensors.battV = link.rx_obj(obj_type=float, obj_byte_size=4, start_pos=recSize)
    recSize += 4
    sensors.battA = link.rx_obj(obj_type=float, obj_byte_size=4, start_pos=recSize)
    recSize += 4
    sensors.waterTemp = link.rx_obj(obj_type=float, obj_byte_size=4, start_pos=recSize)
    recSize += 4
    sensors.internalTemp = link.rx_obj(obj_type=float, obj_byte_size=4, start_pos=recSize)
    recSize += 4
    sensors.errCode = link.rx_obj(obj_type='H', obj_byte_size=2, start_pos=recSize)
    
    return sensors
