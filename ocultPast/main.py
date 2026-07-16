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
        quebralinha()
    else:
        print('Acesso bloqueado, senha incorreta!')
        quebralinha()

def criptografar(path):
    senha = input('Diga sua senha:')
    service = PastService()

    insert = service.cadastrarPath(path,senha)
    if insert:
        print('Pasta adicionada e criptografada')
        quebralinha()
    else:
        print('Erro ao criptografar')
        quebralinha()
 
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
            path = input('Coloque seu diretorio:')
            criptografar(path)



        elif opcao == "Sair":
            break


menu()