"""
Automação foginho(Tik Tok)
"""
import pyautogui as aut
from time import sleep

n = 1
position = {
    "Kesy": (1605, 573),
    "Mar":(1665,503),
    "lipe":(1601,647),
    "grupo":(1673,420),
    "lele":(1647,424),
    "input":(1975,720),
    "btn":(2767,729)
}
pessoas = ["kesy","mar","lipe","lele"]
def get_position():
    sleep(2)
    mouse_pos = aut.position()
    x, y = mouse_pos.x, mouse_pos.y
    print(f"x={x}, y={y}")

def enviarMsg(msg):
    pass

def Main():
    print('Ativar foginho com quem?')

    for pessoa in pessoas:
        print(f'{n}-{pessoa}')
        n += 1
    n +=1
    print(f'{n}-Todos')
    if n != 6:
