from pathlib import Path
import time
import serial
import threading
from tkinter import messagebox
from tkinter import Tk, Canvas, PhotoImage, Button

# Seri portu başlat
ser = serial.Serial('COM4', 115200, timeout=1)
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Ömer Kısa\Desktop\ESP8266-Communication\build\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# ESP8266'dan gelen verileri okuma ve GUI'yi güncelleme
def read_from_esp():
    while True:
        try:
            espData = ser.readline().decode('utf-8', errors='replace').strip()
            if espData:  # Veri alındığında GUI'yi güncelle
                # GUI güncellemelerini ana thread üzerinde yapmak için
                time.sleep(10)
                canvas.after(0, sensorControl, espData)
        except serial.SerialException as e:
            print("Seri port hatası:", e)
            messagebox.showerror("Seri Port Hatası", e)
            break  # Hata oluştuğunda döngüden çık
        except UnicodeDecodeError as e:
            print("Kod çözme hatası:", e)
            messagebox.showerror("Kod Çözme Hatası", e)
            continue  # Döngüyü devam ettir

# Mesafe verisini GUI'ye yazdırma
def sensorControl(espData):
    if canvas and deger:
        canvas.itemconfig(deger, text=espData)

# GUI başlatma ve seri port okuma iş parçacığını başlatma
def start_gui_and_read():
    # Arka planda ESP8266'dan veri okuma
    threading.Thread(target=read_from_esp, daemon=True).start()

    # GUI kodları burada yer alacak
    # Örneğin:
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
    command= lambda: read_from_esp(),
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

# Programı başlat
if __name__ == "__main__":
    start_gui_and_read()
