from StringIO import StringIO
from datetime import datetime

import serial
from PIL import Image, ImageEnhance

from Adafruit_Thermal import Adafruit_Thermal
import raspi_camera

at = Adafruit_Thermal()

at.println("------PP8------")
at.println(datetime.now().strftime("%I:%M %p, %x"))

PORT = raspi_camera.PORT
BAUD = raspi_camera.BAUD
TIMEOUT = raspi_camera.TIMEOUT

s = serial.Serial(PORT, baudrate=BAUD, timeout=TIMEOUT)

assert raspi_camera.setres(raspi_camera.RES_VGA)
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
    image = image.resize((512, 384))
    image = image.rotate(90, expand=True)
    colorer = ImageEnhance.Color(image)
    sharpener = ImageEnhance.Sharpness(colorer.enhance(0))
    image = sharpener.enhance(2.0)

    contraster = ImageEnhance.Contrast(image)

    at.println("New base image:")
    at.printImage(image, LaaT=True)
    at.println("Contrast 0.5")
    at.printImage(contraster.enhance(0.5), LaaT=True)
    at.println("Contrast 1.5")
    at.printImage(contraster.enhance(1.5), LaaT=True)
