from pathlib import Path
import serial
import threading
from tkinter import messagebox, Tk, Canvas, Button, PhotoImage
from ESP_DataBase import *  

# Seri portu başlat
#ser = serial.Serial('COM4', 115200, timeout=1)
espDatas = dataBase()

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\zKodlama\Python\IpekYolu\ESP8266-Communication-main\ESP8266-Communication\build\assets\frame0")

espDistance = ""
espHumidity = ""
espHeat = ""

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

#if the data is same as the previous data, return False, else return True
def is_same(x):
    if is_same.x==x:
        return False
    else:
        is_same.x = x
        return True
is_same.x = None

#DISTANCE SENSOR
# ESP8266'dan gelen mesafe verileri okuma ve GUI'yi güncelleme
def read_distance_esp():
    global espDistance
    while True:
        try:
            espDistance = espDatas.get_distance()
            if espDistance and is_same(espDistance):
                # GUI güncellemelerini ana thread üzerinde yapmak için
                window.event_generate("<<UpdateDistanceSensorData>>", when="tail")
        except Exception as e:
            print("read_distance_esp() de hata:", e)
           


# Mesafe verisini GUI'ye yazdırma
def DistanceSensorControl(event):
    global espDistance
    canvas.itemconfig(distance, text=espDistance)
#-----ESP8266'dan gelen mesafe verileri okuma ve GUI'yi güncelleme

#HUMIDITY SENSOR
# ESP8266'dan gelen nem verileri okuma ve GUI'yi güncelleme
def read_humidity_esp():
    global espHumidity
    while True:
        try:
            espHumidity = espDatas.get_humidity()
            if espHumidity and is_same(espHumidity):
                # GUI güncellemelerini ana thread üzerinde yapmak için
                window.event_generate("<<UpdateHumiditySensorData>>", when="tail")
        except Exception as e:
            print("read_humidity_esp() de hata:", e)


# Mesafe verisini GUI'ye yazdırma
def HumiditySensorControl(event):
    global espHumidity
    canvas.itemconfig(humidity, text=espHumidity)
#-----ESP8266'dan gelen nem verileri okuma ve GUI'yi güncelleme

#HEAT SENSOR
# ESP8266'dan gelen sıcaklık verileri okuma ve GUI'yi güncelleme
def read_heat_esp():
    global espHeat
    while True:
        try:
            espHeat = espDatas.get_heath()
            if espHeat and is_same(espHeat):
                # GUI güncellemelerini ana thread üzerinde yapmak için
                window.event_generate("<<UpdateHeatSensorData>>", when="tail")
        except Exception as e:
            print("read_heat_esp() de hata:", e)
           


# Mesafe verisini GUI'ye yazdırma
def HeatSensorControl(event):
    global espHeat
    canvas.itemconfig(heat, text=espHeat)

#------ESP8266'dan gelen sıcaklık verileri okuma ve GUI'yi güncelleme
    


# GUI başlatma ve seri port okuma iş parçacığını başlatma
def start_gui_and_read():
    threading.Thread(target=read_distance_esp, daemon=True).start()
    threading.Thread(target=read_humidity_esp, daemon=True).start()
    threading.Thread(target=read_heat_esp, daemon=True).start()


########################################################
#-------------------GUI DESİGN CODES-------------------#
########################################################
window = Tk()

window.geometry("780x541")
window.configure(bg = "#0CA7FF")


canvas = Canvas(
    window,
    bg = "#0CA7FF",
    height = 541,
    width = 780,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    390.0,
    129.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    388.0,
    295.0,
    image=image_image_2
)
#----------------DISTANCE----------------#
canvas.create_text(
    333.0,
    61.0,
    anchor="nw",
    text="MESAFE",
    fill="#FFFFFF",
    font=("RobotoRoman Regular", 30 * -1)
)

distance = canvas.create_text(
    363.0,
    89.0,
    anchor="nw",
    text="0",
    fill="#FFFFFF",
    font=("RobotoRoman Bold", 100 * -1)
)
#----------------DISTANCE----------------#

#----------------HEATH----------------#
image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    387.0,
    459.0,
    image=image_image_3
)

canvas.create_text(
    319.0,
    395.0,
    anchor="nw",
    text="SICAKLIK",
    fill="#FFFFFF",
    font=("RobotoRoman Regular", 30 * -1)
)

heat = canvas.create_text(
    367.0,
    423.0,
    anchor="nw",
    text="0",
    fill="#FFFFFF",
    font=("RobotoRoman Bold", 100 * -1)
)
#----------------HEATH----------------#

#----------------HUMIDITY----------------#
canvas.create_text(
    367.0,
    230.0,
    anchor="nw",
    text="NEM",
    fill="#FFFFFF",
    font=("RobotoRoman Regular", 30 * -1)
)

humidity =canvas.create_text(
    367.0,
    262.0,
    anchor="nw",
    text="0",
    fill="#FFFFFF",
    font=("RobotoRoman Bold", 100 * -1)
)


#----------------HUMUDITY----------------#

#----------------TITLE ----------------#
image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    388.0,
    34.0,
    image=image_image_4
)

canvas.create_text(
    311.0,
    24.0,
    anchor="nw",
    text="İpek Yolu ESP Robot",
    fill="#000000",
    font=("RobotoRoman Regular", 17 * -1)
)

window.resizable(True, True)

window.bind("<<UpdateHeatSensorData>>", HeatSensorControl)
window.bind("<<UpdateHumiditySensorData>>", HumiditySensorControl)
window.bind("<<UpdateDistanceSensorData>>", DistanceSensorControl)

if __name__ == "__main__":
    start_gui_and_read()

window.mainloop()
########################################################
#-------------------GUI DESİGN CODES-------------------#
########################################################