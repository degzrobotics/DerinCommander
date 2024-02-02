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

def rovUpdate(commandData: CommandData, receivedData: ReceivedData) -> Tuple[CommandData]:
    
    #print(commandData)
    #print(receivedData)
    rov.arm()
    rov.turnDegrees(-70)
    rov.move(0,0,500)
    return commandData

try:
    rov = Rov(port='COM10')
    rov.run(rovUpdate)

except:
    import traceback
    traceback.print_exc()

finally:
    rov.close()

