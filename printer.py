import serial
from itertools import chain
import random
import json
import requests
from Adafruit_Thermal import *
from bmp2array import *
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
newsize = (380, 530)
img = img.resize(newsize)
img = ImageOps.invert(img)
arr = np.array(img)

r,g,b = np.split(arr, 3, axis=2)
r = r.reshape(-1)
g = g.reshape(-1)
b = b.reshape(-1)

bmp = list(map(lambda x: 0.299*x[0]+0.587*x[1]+0.114*x[2],
               zip(r,g,b)))
bmp = np.array(bmp).reshape([arr.shape[0], arr.shape[1]])
bmp = np.dot((bmp > 128).astype(int), 255)
i = (bmp.astype(np.uint8))

var image = new Bitmap(10, 10);
print(i)


## Print the Card

printer.printBitmap(380, 530, i)
