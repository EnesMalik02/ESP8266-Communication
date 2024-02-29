from pathlib import Path
import serial
import threading
from tkinter import messagebox, Tk, Canvas, Button, PhotoImage

# Seri portu başlat
ser = serial.Serial('COM4', 115200, timeout=1)

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"build\assets\frame0")

espData = ""

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

# ESP8266'dan gelen verileri okuma ve GUI'yi güncelleme
def read_from_esp():
    global espData
    while True:
        try:
            espData = ser.readline().decode('utf-8', errors='replace').strip()
            if espData and is_same(espData):
                # GUI güncellemelerini ana thread üzerinde yapmak için
                window.event_generate("<<UpdateSensorData>>", when="tail")
        except serial.SerialException as e:
            print("Seri port hatası:", e)
            messagebox.showerror("Seri Port Hatası", e)
            break
        except UnicodeDecodeError as e:
            print("Kod çözme hatası:", e)
            messagebox.showerror("Kod Çözme Hatası", e)
            continue


# Mesafe verisini GUI'ye yazdırma
def sensorControl(event):
    global espData
    canvas.itemconfig(deger, text=espData)


# GUI başlatma ve seri port okuma iş parçacığını başlatma
def start_gui_and_read():
    threading.Thread(target=read_from_esp, daemon=True).start()
    

window = Tk()

window.geometry("306x431")
window.configure(bg="#0CA7FF")

canvas = Canvas(
    window,
    bg="#0CA7FF",
    height=431,
    width=306,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

canvas.create_rectangle(
    26.0,
    19.0,
    281.0,
    49.0,
    fill="#FFFFFF",
    outline=""
)

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
    outline=""
)

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
    font=("RobotoItalic CondensedThin", 75 * -1)
)



window.resizable(False, False)

window.bind("<<UpdateSensorData>>", sensorControl)

if __name__ == "__main__":
    start_gui_and_read()

window.mainloop()
