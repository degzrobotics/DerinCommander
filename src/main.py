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
from rov import *

"""
    When the main.py is first run it automatically arms DerinDiver
    and then starts the main loop of the program. You can run your own
    code in the rovUpdate function but it'll be run at the rate_hz. Higher
    rate_hz values can cause problems in the serial communication. If you 
    want to run your computer vision logic try to run it in a separate thread.
    You can pass the commandData and receivedData to your own functions
    
"""
def rovUpdate(commandData: CommandData, receivedData: ReceivedData) -> CommandData:
    print(receivedData)
    #print(commandData)
    rov.turnDegrees(-70)
    rov.move(0, 0, 500)
    
    return commandData

try:
    rov = Rov(port='COM5', rate_hz=20) # Sublink's port, communication rate in Hz (higher values can cause problems in the serial communication)
    clear_buffers(rov.link)
    rov.run(rovUpdate)
except:
    import traceback
    traceback.print_exc()
finally:
    rov.close()

