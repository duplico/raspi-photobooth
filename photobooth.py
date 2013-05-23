from StringIO import StringIO

import serial
from PIL import Image

from Adafruit_Thermal import Adafruit_Thermal
import raspi_camera

PORT = raspi_camera.PORT
BAUD = raspi_camera.BAUD
TIMEOUT = raspi_camera.TIMEOUT

s = serial.Serial(PORT, baudrate=BAUD, timeout=TIMEOUT)
raspi_camera.reset()
assert raspi_camera.getversion()

# TODO: wrap in function
success = takephoto()
assert success

photo_bytes = raspi_camera.readbuffer(raspi_camera.getbufferlength())
photo_buffer = StringIO(photo_bytes)
image = Image.open(photo_buffer)

at = Adafruit_Thermal()
at.printImage(image)