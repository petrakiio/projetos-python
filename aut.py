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


def enviar_msgs_personalizadas(mensagens_por_pessoa):
    abrirBrave()
    acessarttk()

    for nome, msg in mensagens_por_pessoa.items():
        if not msg:
            continue

        acessarcontato(nome)
        aut.click(position["input"])
        aut.hotkey("ctrl", "a")
        aut.press("backspace")
        aut.write(msg)
        aut.click(position["btn"])
        sleep(2)


def main():
    print("Enviar mensagem personalizada para cada contato.")
    print("Se deixar vazio, usa a mensagem padrão.")

    msg_padrao = input("Mensagem padrão:\nR: ").strip()
    if not msg_padrao:
        print("Mensagem padrão vazia. Operação cancelada.")
        return

    mensagens_por_pessoa = {}

    for _, nome in pessoas.items():
        personalizada = input(
            f"Mensagem para {nome.capitalize()} (enter = padrão):\nR: "
        ).strip()
        mensagens_por_pessoa[nome] = personalizada or msg_padrao

    enviar_msgs_personalizadas(mensagens_por_pessoa)


if __name__ == "__main__":
    main()
