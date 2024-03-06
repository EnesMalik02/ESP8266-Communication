from pathlib import Path
import threading
from tkinter import *
from ESP_DataBase import *  
import time

# Seri portu başlat
getEspDatas = getDataBase()
setEspDatas = setDataBase()

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Ömer Kısa\Desktop\ESP8266-Communication\build\assets\frame0")

espDistance = ""
espHumidity = ""
espHeat = ""

#################################################
#-------------------FUNCTIONS-------------------#
#################################################

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
            espDistance = getEspDatas.get_distance()
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
            espHumidity = getEspDatas.get_humidity()
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
            espHeat = getEspDatas.get_heath()
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

def changeColor(btnName,ledID):
    if setup() == True:
        send_led_on(ledID)
    value = getEspDatas.get_led(ledID)
    if value == "OFF":
        canvas.itemconfig(btnName, fill="#FF0F0F")
    else:
        canvas.itemconfig(btnName, fill="#59FF3E")

def get_led_value(btnName,ledID):
    value = getEspDatas.get_led(ledID)
    if value == "OFF":
        canvas.itemconfig(btnName, fill="#FF0F0F")
    else:
        canvas.itemconfig(btnName, fill="#59FF3E")

def send_led_on(ledID):
    led1 = getEspDatas.get_led(ledID)
    if led1 == "ON":
        led1 = "OFF"
    else:
        led1 = "ON"

    setEspDatas.set_led(led1,ledID)
    print(led1)
    return led1

#################################################
#-------------------FUNCTIONS-------------------#
#################################################
    
# GUI başlatma ve seri port okuma iş parçacığını başlatma
def start_gui_and_read():
    threading.Thread(target=read_distance_esp, daemon=True).start()
    threading.Thread(target=read_humidity_esp, daemon=True).start()
    threading.Thread(target=read_heat_esp, daemon=True).start()

###################################################
#-------------------SETUP CODES-------------------#
###################################################

def setup():
    get_led_value(btn1, ledID="led")
    get_led_value(btn2, ledID="led2")
    get_led_value(btn3, ledID="led3")
    return True

###################################################
#-------------------SETUP CODES-------------------#
###################################################

########################################################
#-------------------GUI DESİGN CODES-------------------#
########################################################
window = Tk()

window.title("İPEKYOLU ESP KART")
window.geometry("1120x681")
window.configure(bg = "#E4E9E7")
    

canvas = Canvas(
    window,
    bg = "#E4E9E7",
    height = 681,
    width = 1120,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
btn1 = canvas.create_rectangle(
    141.0,
    410.0,
    217.0,
    446.0,
    fill="#59FF3E",
    outline="")

btn2 = canvas.create_rectangle(
    511.0,
    410.0,
    587.0,
    446.0,
    fill="#FF0F0F",
    outline="")

btn3 = canvas.create_rectangle(
    883.0,
    410.0,
    959.0,
    446.0,
    fill="#FF0F0F",
    outline="")

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: changeColor(btn1, ledID="led"),
    relief="flat"
)
button_1.place(
    x=88.0,
    y=310.0,
    width=186.36886596679688,
    height=86.95082092285156
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: changeColor(btn2, ledID="led2"),
    relief="flat"
)
button_2.place(
    x=458.0,
    y=310.0,
    width=186.46722412109375,
    height=86.95082092285156
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: changeColor(btn3, ledID="led3"),
    relief="flat"
)
button_3.place(
    x=830.6311645507812,
    y=310.0,
    width=186.1639404296875,
    height=86.95082092285156
)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    560.0,
    173.0,
    image=image_image_1
)

distance = canvas.create_text(
    145.0,
    199.0,
    anchor="nw",
    text="Mesafe Text",
    fill="#000000",
    font=("RobotoRoman Regular", 30 * -1)
)

canvas.create_text(
    154.0,
    126.0,
    anchor="nw",
    text="MESAFE",
    fill="#8EA5BD",
    font=("RobotoRoman Regular", 30 * -1)
)

humidity = canvas.create_text(
    488.0,
    199.0,
    anchor="nw",
    text="Nem Text",
    fill="#000000",
    font=("RobotoRoman Regular", 30 * -1)
)

canvas.create_text(
    515.0,
    126.0,
    anchor="nw",
    text="NEM",
    fill="#8EA5BD",
    font=("RobotoRoman Regular", 30 * -1)
)

heat = canvas.create_text(
    808.0,
    199.0,
    anchor="nw",
    text="Sıcaklık Text",
    fill="#000000",
    font=("RobotoRoman Regular", 30 * -1)
)

canvas.create_text(
    828.0,
    126.0,
    anchor="nw",
    text="SICAKLIK",
    fill="#8EA5BD",
    font=("RobotoRoman Regular", 30 * -1)
)

canvas.create_text(
    421.0,
    25.0,
    anchor="nw",
    text="İPEKYOLU ESP KART",
    fill="#000000",
    font=("RobotoRoman Regular", 30 * -1)
)
#-------------------BAŞLIK-------------------#

window.resizable(True, True)

window.bind("<<UpdateHeatSensorData>>", HeatSensorControl)
window.bind("<<UpdateHumiditySensorData>>", HumiditySensorControl)
window.bind("<<UpdateDistanceSensorData>>", DistanceSensorControl)

if __name__ == "__main__":
    setup()
    time.sleep(0.2)
    start_gui_and_read()

window.mainloop()
########################################################
#-------------------GUI DESİGN CODES-------------------#
########################################################