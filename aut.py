"""
Automação foginho(Tik Tok)
"""
import os
import subprocess
from time import sleep

import pyautogui as aut
from dotenv import load_dotenv

load_dotenv()

aut.PAUSE = 1
aut.FAILSAFE = True

position = {
    "kesy": (1605, 573),
    "mar": (1665, 503),
    "lipe": (1601, 647),
    "grupo": (1673, 420),
    "lele": (1647, 424),
    "input": (1975, 720),
    "btn": (2767, 729),
    "btn-brave": (1856, 58),
}
pessoas = {
    1: "kesy",
    2: "mar",
    3: "lipe",
    4: "lele",
    5: "grupo",
}


def get_position():
    sleep(2)
    mouse_pos = aut.position()
    x, y = mouse_pos.x, mouse_pos.y
    print(f"x={x}, y={y}")


def abrirBrave():
    subprocess.Popen(["brave-browser"])
    sleep(3)
    aut.click(position["btn-brave"])


def acessarttk():
    link = os.getenv("TTK")
    if not link:
        raise RuntimeError("A variável TTK não foi definida no arquivo .env.")

    aut.write(link)
    aut.press("enter")
    sleep(15)


def acessarcontato(nome):
    aut.click(position[nome])


def enviarMsg(msg, nome):
    abrirBrave()
    acessarttk()
    acessarcontato(nome)
    aut.click(position["input"])
    aut.write(msg)
    aut.click(position["btn"])


def main():
    print("Ativar foginho com quem?")

    for numero, nome in pessoas.items():
        print(f"{numero}-{nome.capitalize()}")

    pessoa_input = input("R: ").strip()
    if not pessoa_input.isdigit() or int(pessoa_input) not in pessoas:
        print("Opção inválida. Escolha um número da lista.")
        return

    pessoa = int(pessoa_input)
    msg = input("Me diga a mensagem de foguinho:\nR: ").strip()
    if not msg:
        print("Mensagem vazia. Operação cancelada.")
        return

    nome = pessoas[pessoa]
    enviarMsg(msg, nome)


if __name__ == "__main__":
    main()
