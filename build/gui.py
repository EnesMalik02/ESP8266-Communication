#---------------ARDUNIO CODES STARTS HERE----------------------#

import serial

ser = serial.Serial('COM4', 115200,timeout=1)

espData = ser.readline().decode('ascii')
print(espData)


#---------------ARDUNIO CODES ENDS HERE----------------------#


#---------------FUNCTIONS STARTS HERE----------------------#

def is_same(x):
    if is_same.x==x:
        return True
    else:
        is_same.x = x
        return False
is_same.x = None

def sensorControl(espData):
    if is_same(espData):
        return
    else:
        print(espData)
        canvas.itemconfig(deger, text=espData)
        return

#---------------FUNCTIONS ENDS HERE----------------------#


#---------------UI CODES STARTS HERE----------------------#
from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\zKodlama\Python\IpekYolu\UI Projesi Demo\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)



window = Tk()

window.geometry("306x431")
window.configure(bg = "#0CA7FF")


canvas = Canvas(
    window,
    bg = "#0CA7FF",
    height = 431,
    width = 306,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    26.0,
    19.0,
    281.0,
    49.0,
    fill="#FFFFFF",
    outline="")

canvas.create_text(
    77.0,
    24.0,
    anchor="nw",
    text="İpek Yolu ESP Robot",
    fill="#000000",
    font=("RobotoRoman Regular", 17 * -1)
)

canvas.create_rectangle(
    26.0,
    81.0,
    281.0,
    376.0,
    fill="#E94444",
    outline="")

canvas.create_text(
    58.0,
    95.0,
    anchor="nw",
    text="MESAFE",
    fill="#FFFFFF",
    font=("RobotoRoman Regular", 50 * -1)
)

deger = canvas.create_text(
    130.0,
    205.0,
    anchor="nw",
    text="0",
    fill="#FFFFFF",
    font=("RobotoItalic CondensedThin", 100 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command= lambda: sensorControl(espData),
    relief="flat"
)
button_1.place(
    x=30.0,
    y=388.0,
    width=247.0,
    height=28.0
)
window.resizable(False, False)
window.mainloop()

#---------------UI CODES ENDS HERE----------------------#