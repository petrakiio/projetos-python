import questionary
import os
from controller.pastaController import PastService

def quebralinha():
    print()

def acessar(path):
    service = PastService()

    senha = input('Diga sua senha:')
    acess = service.AcessPast(path,senha)

    if acess:
        print('Pasta desbloqueada')
    
    print('Acesso bloqueado,senha incorreta!')


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
                "Reecriptografar Past",
                "Cadastrar Past",
                "Sair"
            ]
        ).ask()


        if opcao == "Acessar Past":
            path = MenuPaths()
            acessar(path)


        elif opcao == "Cadastrar Past":
            pass

        elif opcao == "Reecriptografar Past":
            pass

        elif opcao == "Sair":
            break


menu()