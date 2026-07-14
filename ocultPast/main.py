import questionary

def menu():

    while True:

        opcao = questionary.select(
            "Cadastrar",
            choices=[
                "Password",
                "Path",
                "Sair"
            ]
        ).ask()


        if opcao == "Cadastrar rosto":
            cadastrar_rosto()

        elif opcao == "Validar rosto":
            validar_rosto()

        elif opcao == "Sair":
            break


menu()