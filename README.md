# DiveCommander

## A python library to send control commands to DerinPilot

DiveCommander is a python library that allows you to send control commands to DerinPilot. It is designed to be used with the [DerinPilot](https://github.com/degzrobotics/DerinPilot) project.

## Features

* Send control commands to DerinPilot via serial port
* Get sensor data from DerinPilot
* Get the camera feed and easily use it with OpenCV

## Installation

1. Clone the repository
2. Install the requirements with `pip install -r requirements.txt`
3. Run the main script with `python main.py`

## Usage

### Sending control commands

```python
from divecommander import DiveCommander
```

## Dependencies

* opencv-python
* numpy
* pySerialTransfer
* XInput-Python

## How to contribute

You can contribute to the project by creating issues, pull requests, or by contacting us.
The more people contribute, the better the project will be. We are hoping we can keep it simple and easy to use.

## License

DiveCommander is licensed under the General Public License v3.0. See `COPYING.txt` for more information.
[Full Text](https://github.com/degzrobotics/DiveCommander/blob/main/COPYING.txt)
