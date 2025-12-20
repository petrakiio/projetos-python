senha_user = input("Me diga sua senha:")

with open("rockyou.txt") as wordlist:
    for senhas in wordlist:
        if senhas.strip() == senha_user:
            print("Sua Senha está na wordlist")
            break
    else:
        print("Sua senha está a salvo")
        