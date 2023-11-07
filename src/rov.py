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

from serialLink import *
import time
import logging
from typing import Optional, Union, Tuple

logging.basicConfig(level=logging.ERROR)

class Rov:

    def __init__(self, port: str, delay: Optional[float] = 0.03, baudRate: Optional[int] = 38400) -> None:
        self.receivedData = ReceivedData()
        self.commandData = CommandData(0.0,0.0,0.0,0.0,0.0,0.0,0.0,0)
        self.baudRate = baudRate
        self.delay = delay
        self.port = port

        self.link = txfer.SerialTransfer(port, baud=baudRate)
        self.link.open()
        
        self.arm()
        time.sleep(2)
        

    def run(self, rovUpdate=None):
        while True:
            if rovUpdate != None:
                    self.commandData = rovUpdate(
                        self.commandData, self.receivedData)
            self.send()
            self.receive()
            time.sleep(self.delay)

    def send(self):
        serialSend(self.link, self.commandData)

    def receive(self):
        if self.link.available():
            self.receivedData = serialReceive(self.link)
            logging.debug(self.receivedData)
        elif self.link.status <= 0:
            logging.error('EROR: RS485_WIRE_PROBLEM')
            time.sleep(0.2)
            if self.link.status <= 0:
                if self.link.status == txfer.CRC_ERROR:
                    logging.error('ERROR: CRC_ERROR')
                elif self.link.status == txfer.PAYLOAD_ERROR:
                    logging.error('ERROR: PAYLOAD_ERROR')
                elif self.link.status == txfer.STOP_BYTE_ERROR:
                    logging.error('ERROR: STOP_BYTE_ERROR')
                else:
                    logging.error('ERROR: {}'.format(self.link.status))

    def close(self):
        try:
            self.link.close()
            logging.info('Serial port is closed')
        except:
            logging.error('Unable to close serial port')

    def arm(self):
        """Arms the ROV and sets the default heading and roll set point to current heading and roll.
        It should only be called once. If its called continuously, the ROV will always updates its 
        default set points.
        """        
        sendArmCommand(self.link,armed=True)
        
    def disArm(self):
        """Disarms the ROV.
        """        
        sendArmCommand(self.link,armed=False)
        
    def move(self, heave: float, strafe: float, surge:float):
        """Move the ROV with the given values.

        Args:
            heave (float): Up and Down Movement, -500 to 500
            strafe (float): Side to side Movement, -500 to 500
            surge (float): Forward and Backward Movement, -500 to 500
        """        
        self.commandData.heave = heave
        self.commandData.strafe = strafe
        self.commandData.surge = surge
        
    def turnDegrees(self, degrees: float):
        """Turns the ROV by the given degrees.

        Args:
            degrees (float): Degrees to turn, -180 to 180
        """        
        self.commandData.heading = self.receivedData.yaw + degrees