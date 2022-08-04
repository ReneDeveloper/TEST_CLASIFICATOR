#FOCUS.PY


import pygetwindow as pg
import time
import ctypes
import winsound

duration = 100  # milliseconds
freq = 600  # Hz
time_on_window = 0 # Seconds

while True:
    window = pg.getActiveWindow()
    WnName = window.title 
    if window.title != "Chrome Remote Desktop - <MY-PC>":
        time_on_window += 1
    if window.title == "Chrome Remote Desktop - <MY-PC>":
        time_on_window = 0
    if time_on_window >= 10:
        top_window = pg.getActiveWindow()
        top_window.close()
        winsound.Beep(freq, duration)
        winsound.Beep(freq, duration)
        winsound.Beep(freq, duration)
        ctypes.windll.user32.MessageBoxW(0, "VUELVE A TRABAJAR MALDITO FLOJO HIJO DE LA CHINGADERA:" +  WnName, "PARA DE FLOJEAR FLOJO CULIAO:" , 0x1000)
        time_on_window = 0
    print(time_on_window)
    time.sleep(1)

