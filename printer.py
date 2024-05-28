import serial
from itertools import chain
import random
import itertools
import json
import requests
from Adafruit_Thermal import *
from bmp2array import img_to_bmp
import numpy as np
import io
from PIL import Image, ImageOps


printer = Adafruit_Thermal("/dev/ttyAMA0", 9600, timeout=5)

AllCardsJson = requests.get("https://api.scryfall.com/catalog/card-names")

randomCard = random.choice(AllCardsJson.json()["data"])
randomCard.replace(" ", "+")
randomCardImage = requests.get("https://api.scryfall.com/cards/named?exact=" + randomCard + "&format=image&version=border_crop").content
with open('temp_img.jpg', 'wb') as handler:
    handler.write(randomCardImage)


img = Image.open("temp_img.jpg")
newsize = (384, 536)
img = img.resize(newsize)
img = img.convert("1", dither=Image.Dither.FLOYDSTEINBERG, palette=Image.Palette.ADAPTIVE, colors = 256)
img = ImageOps.invert(img)

bmp = np.array(img).flatten().astype(np.bool_).tolist()

final = []
for x in range(0, len(bmp), 8):
    temp = bmp[x:x+8]
    n = int(''.join(['1' if i else '0' for i in temp]), 2)
    final.append(n)

with open('your_file.txt', 'w') as f:
    for line in final:
        f.write(f"{line}\n")

## Print the Card
printer.printBitmap(384, 536, final)
printer.feed(2)