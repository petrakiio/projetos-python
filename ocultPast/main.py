import questionary
from models.db 

def visualizarPast():
    

def menu():

    while True:

        opcao = questionary.select(
            "Menu",
            choices=[
                "Acessar Past"
                "Cadastrar Past",
                "Sair"
            ]
        ).ask()


        if opcao == "Acessar Past":
            

        elif opcao == "Cadastrar Past":
            pass

        elif opcao == "Sair":
            break


menu()