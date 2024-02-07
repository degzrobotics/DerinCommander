# DerinCommander

## A python library to send autonomous control commands to DerinDiver

DerinCommander is a python library that allows you to send control commands to DerinDiver. It is designed to be used with the [DerinDiver](https://github.com/degzrobotics/DerinDiver) project.

## Features

* Send control commands to DerinDiver via serial port
* Get sensor data from DerinDiver
* Get the camera feed and easily use it with OpenCV

## Installation

1. Clone the repository
2. Install the requirements with `pip install -r requirements.txt`
3. Run the main script with `python main.py`

## Usage

### Sending control commands

```python
from DerinCommander import DerinCommander
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

DerinCommander is licensed under the General Public License v3.0. See `COPYING.txt` for more information.
[Full Text](https://github.com/degzrobotics/DerinCommander/blob/main/COPYING.txt)
