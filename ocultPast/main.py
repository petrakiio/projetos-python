import questionary
import os
from controller.past import PastService

def quebralinha():
    print()

def MenuPaths():
    paths = PastService.query()
    if paths is not None:
        opn = questionary.select(
            "Escolha a pasta",
            choices=[paths]
        )
        

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