from core.faces import questionary,cadastrar_rosto,validar_rosto

def menu():

    while True:

        opcao = questionary.select(
            "Sistema facial",
            choices=[
                "Cadastrar rosto",
                "Validar rosto",
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