from StringIO import StringIO

import serial
from PIL import Image

from Adafruit_Thermal import Adafruit_Thermal
import raspi_camera

at = Adafruit_Thermal()


PORT = raspi_camera.PORT
BAUD = raspi_camera.BAUD
TIMEOUT = raspi_camera.TIMEOUT

s = serial.Serial(PORT, baudrate=BAUD, timeout=TIMEOUT)
raspi_camera.reset()
assert raspi_camera.getversion()

# TODO: wrap in function
success = raspi_camera.takephoto()
assert success

photo_bytes = raspi_camera.readbuffer(raspi_camera.getbufferlength())
photo_data = ''.join(photo_bytes)
photo_buffer = StringIO()
photo_buffer.write(''.join(photo_bytes))

with open('photo.jpg', 'w') as photo_file:
    photo_file.write(photo_data)

#image = Image.open(photo_buffer)

with open('photo.jpg', 'r') as photo_file:
    image = Image.open(photo_file)
    at.printImage(image, LaaT=True)
