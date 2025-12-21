import time
import threading
import tkinter as tk
from tkinter import messagebox
import sys
import termios
import tty

INTERVALO = 600  # 10 minutos
rodando = True

def popup():
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Timer", "Já se passaram 10 minutos!")
    root.destroy()

def timer_loop():
    global rodando
    while rodando:
        time.sleep(INTERVALO)
        if rodando:
            popup()

def esc_listener():
    global rodando
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setraw(fd)
        while rodando:
            ch = sys.stdin.read(1)
            if ch == '\x1b':  # ESC
                rodando = False
                print("\nESC pressionado. Encerrando timer...")
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

# Threads
t1 = threading.Thread(target=timer_loop, daemon=True)
t2 = threading.Thread(target=esc_listener, daemon=True)

t1.start()
t2.start()

print("Timer iniciado.")
print("Pop-up a cada 10 minutos.")
print("Pressione ESC para parar.")

while rodando:
    time.sleep(0.5)

