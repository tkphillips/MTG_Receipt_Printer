import serial
import random
import json
import requests
from Adafruit_Thermal import *
printer = Adafruit_Thermal("/dev/ttyAMA0", 9600, timeout=5)

AllCardsJson = requests.get("https://api.scryfall.com/catalog/card-names")

randomCard = random.choice(AllCardsJson.json()["data"])
randomCard.replace(" ", "+")
randomCardImage = requests.get("https://api.scryfall.com/cards/named?exact=" + randomCard + "&format=image&version=border_crop").content
with open('image_name.jpg', 'wb') as handler:
    handler.write(randomCardImage)

## Print the Card
#import gfx.adalogo as adalogo
#printer.printBitmap(adalogo.width, adalogo.height, adalogo.data)
