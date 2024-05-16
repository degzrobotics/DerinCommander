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
import threading
import logging
from typing import Optional

logging.basicConfig(level=logging.ERROR)

class Rov:
    def __init__(self, port: str, rate_hz: Optional[int] = 28, baudRate: Optional[int] = 38400) -> None:
        self.receivedData = ReceivedData()
        self.commandData = CommandData(2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0)
        self.baudRate = baudRate
        self.rate_hz = rate_hz
        self.port = port
        self.callback_list = [ self.receive ]
        self.link = txfer.SerialTransfer(port, baud=baudRate)
        self.link.open()
        self.link.set_callbacks(self.callback_list)
        clear_buffers(self.link)
        self.yaw_set_point = 0.0
        self.roll_set_point = 0.0
        self.arm()

        self.interval = 1.0 / rate_hz  # Interval in seconds
        self.is_running = True

        # Start a separate thread for receiving data
        self.receive_thread = threading.Thread(target=self.receive_loop)
        self.receive_thread.daemon = True
        self.receive_thread.start()

    def run(self, rovUpdate=None):
        next_time = time.monotonic() + self.interval
        while self.is_running:
            current_time = time.monotonic()
            if current_time >= next_time:
                if rovUpdate is not None:
                    self.commandData = rovUpdate(self.commandData, self.receivedData)
                self.send()
                next_time += self.interval
                if next_time <= current_time:
                    next_time = current_time + self.interval

    def send(self):
        serialSend(self.link, self.commandData, self.yaw_set_point)

    def receive_loop(self):
        while self.is_running:
            self.link.tick()
            time.sleep(0.01)

    def receive(self):
        self.receivedData = serialReceive(self.link)
        
    def close(self):
        self.is_running = False
        try:
            self.receive_thread.join()
            self.link.close()
            logging.info('Serial port is closed')
        except Exception as e:
            logging.error(f'Unable to close serial port: {e}')

    def arm(self):
        """Arms the ROV and sets the default heading and roll set point to current heading and roll.
        It should only be called once. If its called continuously, the ROV will always updates its 
        default set points.
        """        
        sendArmCommand(self.link,armed=True, commandData=self.commandData, receivedData=self.receivedData)
        
    def disArm(self):
        """Disarms the ROV.
        """
        sendArmCommand(self.link, armed=False, commandData=self.commandData, receivedData=self.receivedData)
        
    def move(self, heave: float, strafe: float, surge:float, roll: float, pitch: float):
        """Move the ROV with the given values.

        Args:
            heave (float): Up and Down Movement, -500 to 500
            strafe (float): Side to side Movement, -500 to 500
            surge (float): Forward and Backward Movement, -500 to 500
        """
        self.commandData.heave = heave
        self.commandData.strafe = strafe
        self.commandData.surge = surge
        self.commandData.roll = roll
        self.commandData.pitch = pitch

    def turn(self, degrees: float):
        """Turns the ROV to the given degree.

        Args:
            degrees (float): Degrees to turn, -180 to 180
        """
        self.yaw_set_point = self.receivedData.yaw + degrees
        # print("self.commandData.heading", self.commandData.heading)

    def turnDegrees(self, degrees: float):
        """Turns the ROV by the given degrees.

        Args:
            degrees (float): Degrees to turn, -180 to 180
        """
        self.commandData.heading = self.receivedData.yaw + degrees