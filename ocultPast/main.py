import questionary
import os
from controller.pastaController import PastService

def quebralinha():
    print()

def MenuPaths():
    service = PastService()
    paths = service.query()

    if paths is None:
        print("Nenhuma pasta encontrada.")
        return None

    choices = [path[0] for path in paths]

    opn = questionary.select(
        "Escolha a pasta",
        choices=choices
    ).ask()

    return opn

def menu():

    while True:

        opcao = questionary.select(
            "Menu",
            choices=[
                "Acessar Past",
                "Cadastrar Past",
                "Sair"
            ]
        ).ask()


        if opcao == "Acessar Past":
            path = MenuPaths()


        elif opcao == "Cadastrar Past":
            pass

        elif opcao == "Sair":
            break


menu()