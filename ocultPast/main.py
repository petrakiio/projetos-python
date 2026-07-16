import questionary
from controller.pastaController import PastService


def quebralinha():
    print()


def acessar(path):
    if path is None:
        return

    service = PastService()

    senha = input('Diga sua senha: ')

    acess = service.AcessPast(path, senha)

    if acess:
        print('Pasta desbloqueada')
    else:
        print('Acesso bloqueado, senha incorreta!')

def criptografar(path):
    pass

def MenuPaths(value):
    service = PastService()

    paths = service.queryLocked(value)

    if not paths:
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

            path = MenuPaths(0)  # bloqueadas

            acessar(path)


        elif opcao == "Reecriptografar Past":

            path = MenuPaths(1)  # desbloqueadas

            if path:
                print(f"Selecionado: {path}")


        elif opcao == "Cadastrar Past":
            pass


        elif opcao == "Sair":
            break


menu()