import random

ver_senhas = None

def contar_caracteres(senha):
    digitos = 0
    for letras in senha:
        digitos +=1
    return digitos

def analisar(senha,numeros,alfabeto,simbolos):
    if all(c in numeros for c in senha):
        return "NUM"
    
    elif all(c in alfabeto for c in senha):
        return "LETRAS"
    
    elif all(c in simbolos for c in senha):
        return "SIMBOLOS"
    
    # Se tiver uma mistura de tudo
    elif any(c in numeros for c in senha) and any(c in alfabeto for c in senha) and any(c in simbolos for c in senha):
        return "MISTA"
    
    else:
        return "COMPOSTO"
 
tentativas = 0
numeros = "1234567890"
alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
simbolos = "!@#$%^&*()-_=+[{]};:,.<>?/|"
dados = numeros+alfabeto+simbolos

senha = input("Me diga sua senha forte:")
print("O progama vai tentar quebra-lá")
opn = int(input("Você quer ver o programa testando as senhas?\n1-Sim/2-Não:"))
if opn == 1:
    ver_senhas = True
else:
    ver_senhas = False

with open("password-wordlist.txt") as wordlist:
    for senhas in wordlist:
        senhas = senhas.strip()
        if ver_senhas == True:
            print(f"Senha testada:{senhas},Tentiva:{tentativas +1}")
            if senhas == senha:
                print("Sua senha foi achada na wordlist!")
                break
        else:
            if senhas == senha:
                print("Sua senha foi achada na wordlist!")
                break
    else:
        opn2 = int(input("Sua senha não foi encontrada na wordlist,você deseja tentar um ataque de força bruta nela?\n 1-Sim/2-Não:"))
        if opn2 == 1 and ver_senhas == True:
            while True:
                digitos = contar_caracteres(senha)
                combinação = "".join(random.choices(dados, k=digitos))
                print(f"Senha testada:{combinação},Tentiva:{tentativas +1}")
                if combinação == senha:
                    print("Sua senha foi quebrada!")
                    break
                else:
                    pass
        elif opn2 == 1 and ver_senhas == False:
            while True:
                digitos = contar_caracteres(senha)
                combinação = "".join(random.choices(dados, k=digitos))
                if combinação == senha:
                    print("Sua senha foi querada!")
                    break
                else:
                    pass
        else:
            print("Tudo bem,sua senha é forte!")