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

from serial_transfer import *
import time
import logging
from typing import Optional, Union, Tuple


class Rov:

    def __init__(self, port: str, delay: Optional[float] = 0.03, baudRate: Optional[int] = 38400) -> None:
        self.sensors = Sensors()
        self.commandData = CommandData(0.0,0.0,0.0,0.0,0.0,0.0,0.0,0)
        self.baudRate = baudRate
        self.delay = delay
        self.port = port

        self.link = txfer.SerialTransfer(port, baud=baudRate)
        self.link.open()
        time.sleep(2)

    def run(self, rovUpdate=None):
        while True:
            if rovUpdate != None:
                    self.commandData = rovUpdate(
                        self.commandData, self.sensors)
            self.send()
            self.receive()
            time.sleep(self.delay)

    def send(self):
        serialSend(self.link, self.commandData)

    def receive(self):
        if self.link.available():
            self.sensors = serialReceive(self.link)
            logging.debug(self.sensors)
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
        self.commandData.buttons = 16
        
    def disArm(self):
        self.commandData.buttons = 32