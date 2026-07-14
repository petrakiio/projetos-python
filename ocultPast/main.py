import questionary

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


        if opcao == "Password":
            pass

        elif opcao == "Validar rosto":
            pass

        elif opcao == "Sair":
            break


menu()