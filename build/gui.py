from pathlib import Path
import threading
from tkinter import *
from ESP_DataBase import *  

# Seri portu başlat
getEspDatas = getDataBase()
setEspDatas = setDataBase()

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
    

##############################################################
#--------------------DATA SEND FUNCTIONS---------------------#
##############################################################


def send_led_on():
    led1 = getEspDatas.get_led()
    if led1 == "ON":
        led1 = "OFF"
    else:
        led1 = "ON"

    setEspDatas.set_led(led1)
    print(led1)


# GUI başlatma ve seri port okuma iş parçacığını başlatma
def start_gui_and_read():
    threading.Thread(target=read_distance_esp, daemon=True).start()
    threading.Thread(target=read_humidity_esp, daemon=True).start()
    threading.Thread(target=read_heat_esp, daemon=True).start()


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

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command = send_led_on,
    relief="flat"
)

button_1.place(
    x=12.0,
    y=422.0,
    width=167.0,
    height=78.0
)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    560.0,
    148.0,
    image=image_image_1
)


#----------------MAP----------------#

canvas.create_rectangle(
    205.0,
    276.0,
    1092.0,
    646.0,
    fill="#D9D9D9",
    outline="")

#----------------MAP----------------#

#----------------MESAFE----------------#
canvas.create_text(
    214.0,
    116.0,
    anchor="nw",
    text="MESAFE",
    fill="#8EA5BD",
    font=("RobotoRoman Regular", 30 * -1)
)

distance = canvas.create_text(
    205.0,
    189.0,
    anchor="nw",
    text="0",
    fill="#000000",
    font=("RobotoRoman Regular", 30 * -1)
)
#----------------MESAFE----------------#

#----------------NEM----------------#
canvas.create_text(
    575.0,
    116.0,
    anchor="nw",
    text="NEM",
    fill="#8EA5BD",
    font=("RobotoRoman Regular", 30 * -1)
)

humidity = canvas.create_text(
    548.0,
    189.0,
    anchor="nw",
    text="0",
    fill="#000000",
    font=("RobotoRoman Regular", 30 * -1)
)
#----------------NEM----------------#

#----------------SICAKLIK----------------#
canvas.create_text(
    888.0,
    116.0,
    anchor="nw",
    text="SICAKLIK",
    fill="#8EA5BD",
    font=("RobotoRoman Regular", 30 * -1)
)

heat = canvas.create_text(
    868.0,
    189.0,
    anchor="nw",
    text="0",
    fill="#000000",
    font=("RobotoRoman Regular", 30 * -1)
)
#----------------SICAKLIK----------------#

#-------------------BAŞLIK-------------------#
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
    start_gui_and_read()

window.mainloop()
########################################################
#-------------------GUI DESİGN CODES-------------------#
########################################################