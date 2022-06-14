import tkinter as tk
from tkinter import ttk
import requests
import json
import tkinter.font as font
import easyocr
import cv2

cam = cv2.VideoCapture(0)

cName = ""


def scancard():
    cardName.set("scanning")
    ret, image = cam.read()
    frame = cv2.resize(image, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    reader = easyocr.Reader(['en'])
    result = reader.readtext(frame, paragraph="False")
    try:
        print(result[0][1])
        fetchautocomplete(result[0][1])
    except:
        cardName.set("Unvalid Scan")


def fetchautocomplete(name):
    url = 'https://api.scryfall.com/cards/autocomplete?q=' + name
    response = requests.get(url)
    try:
        responsename = response.json()['data'][0]
        cardName.set(responsename)
        global cName
        cName = responsename
    except:
        cardName.set("Unvalid Scan")


def fetchname():
    global cName
    url = 'https://api.scryfall.com/cards/named?exact=' + cName
    response = requests.get(url)
    responsejson = response.json()
    price = 0
    if responsejson['prices']['eur'] is not None:
        price = responsejson['prices']['eur']

    fetchstorage(responsejson['name'], responsejson['id'], price)


def fetchstorage(name, cardid, price):
    url = 'https://magikatg.herokuapp.com/card/'
    card = {'_id': cardid, 'cardQuantity': 1, 'cardName': name, 'cardPrice': price}
    response = requests.post(url, data=card)


window = tk.Tk()

window.geometry("640x480")
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=1)
window.grid_rowconfigure(2, weight=1)

cardName = tk.StringVar(value="")
window.title("Magika inventory")
# window.attributes('-fullscreen', True)
#window.config(width=640, height=480)


fontExample = font.Font(family="Arial", size=30, weight="bold", slant="italic")

buttonscan = tk.Button(text="Scan", width=10, command=scancard)
buttonscan.grid(row=0, column=0)
buttonscan.configure(font=fontExample)

buttonfetch = tk.Button(text="Save card", width=10, command=fetchname)
buttonfetch.grid(row=1, column=0)
buttonfetch.configure(font=fontExample)

labelName = ttk.Label(window, textvariable=cardName, font=("Arial", 25))
labelName.grid(row=2, column=0)

window.mainloop()