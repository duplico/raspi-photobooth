from StringIO import StringIO
from datetime import datetime

import serial
from PIL import Image, ImageEnhance

from Adafruit_Thermal import Adafruit_Thermal
import raspi_camera

at = Adafruit_Thermal()

with open('pp8.bmp') as pp8_file:
    image = Image.open(pp8_file)
    resized_image = image.resize((384, 94))
    at.printImage(resized_image, LaaT=True)

#at.println("------PP8------")

PORT = raspi_camera.PORT
BAUD = raspi_camera.BAUD
TIMEOUT = raspi_camera.TIMEOUT

s = serial.Serial(PORT, baudrate=BAUD, timeout=TIMEOUT)

#assert raspi_camera.setres(raspi_camera.RES_VGA)
raspi_camera.setres(raspi_camera.RES_VGA)
raspi_camera.reset()
assert raspi_camera.getversion()

# TODO: wrap in function
success = raspi_camera.takephoto()
assert success

# TODO: signal "taken"???

photo_bytes = raspi_camera.readbuffer(raspi_camera.getbufferlength())
photo_data = ''.join(photo_bytes)
photo_buffer = StringIO()
photo_buffer.write(''.join(photo_bytes))

with open('photo.jpg', 'w') as photo_file:
    photo_file.write(photo_data)


#image = Image.open(photo_buffer)

with open('photo.jpg', 'r') as photo_file:
    # The width of the paper is 384 px
    # 4:3 landscape on the paper is 384x288
    # 4:3 portrait on the paper is 512x384
    # If we want to crop landscape into portrait, we need 683x512.

#    image = image.rotate(90, expand=True)

    image = Image.open(photo_file)
    doubled_image = image.resize((683, 512))
    portrait_doubled_image = doubled_image.crop((150,0,534,512))

    image = portrait_doubled_image

    colorer = ImageEnhance.Color(image)
    sharpener = ImageEnhance.Sharpness(colorer.enhance(0))
    image = sharpener.enhance(2.0)

    contraster = ImageEnhance.Contrast(image)

#    at.println("New base image:")
#    at.printImage(image, LaaT=True)
#    at.println("Contrast 1.5")
#    at.printImage(contraster.enhance(1.5), LaaT=True)
#    at.println("Contrast 2.0")
    at.printImage(contraster.enhance(2.0), LaaT=True)
#    at.println("Contrast 2.5")
#    at.printImage(contraster.enhance(2.5), LaaT=True)
at.println(datetime.now().strftime("%I:%M %p, %x"))
at.println()
at.println()
