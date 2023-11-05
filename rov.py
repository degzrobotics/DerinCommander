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
from Controller import *
import cv2 as cv
import time
import logging
from typing import Optional, Union, Tuple


class Rov:

    def __init__(self, port: str, cameraSource: Optional[Union[int, str]] = None, delay: Optional[float] = 0.03, baudRate: Optional[int] = 38400, cameraWidth: Optional[int] = None, cameraHeight: Optional[int] = None, speedMultiplier: Optional[float] = 1.0, useController: Optional[bool] = True) -> None:
        self.cap = None
        self.sensors = Sensors()
        self.controller = Controller()
        self.baudRate = baudRate
        self.cameraSource = cameraSource
        self.delay = delay
        self.port = port
        self.speedMultiplier = speedMultiplier
        self.useController = useController
        if not useController:
            self.controller.isConnected = True

        if cameraSource != None:
            self.cap = cv.VideoCapture(cameraSource)
            if not self.cap.isOpened():
                self.cap = None
                logging.critical("Cannot open camera")
            elif cameraWidth != None and cameraHeight != None:
                self.cap.set(cv.CAP_PROP_FRAME_WIDTH, cameraWidth)
                self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, cameraHeight)
        self.link = txfer.SerialTransfer(port, baud=baudRate)
        self.link.open()
        time.sleep(2)

    def run(self, onFrame=None):
        while True:
            if self.useController:
                self.controller.update()
            if self.cap:
                ret, frame = self.cap.read()
                if not ret:
                    logging.info(
                        "Can't receive frame from camera. Exiting ...")
                    break
                if onFrame != None:
                    frame, self.controller.state = onFrame(
                        frame, self.controller.state, self.sensors)
                cv.imshow('frame', frame)
                if cv.waitKey(1) == ord('q'):
                    break
            if self.controller.isConnected:
                self.send()
                self.receive()
            time.sleep(self.delay)

    def send(self):
        serialSend(self.link, self.controller.state, self.speedMultiplier)

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
        if self.cap:
            self.cap.release()
            cv.destroyAllWindows()
            logging.info('Camera is closed')

        try:
            self.link.close()
            logging.info('Serial port is closed')
        except:
            logging.error('Unable to close serial port')
