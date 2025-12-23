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
def testar(digito,tipo,opn,senha):
    numeros = "1234567890"
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    simbolos = "!@#$%^&*()-_=+[{]};:,.<>?/|"
    tentativa = 0 

    if tipo == "MISTA":
        dado = numeros+alfabeto+simbolos
    elif tipo == "SIMBOLOS":
        dado = simbolos
    elif tipo == "LETRAS":
        dado = alfabeto
    elif tipo == "NUM":
        dado = numeros
    else:
        dado = numeros+alfabeto+simbolos
    
    if opn == True:
        while True:
            combinação = "".join(random.choices(dado,k=digito))
            tentativa +=1
            print(f"Senha testada:{combinação}.Tentativa:{tentativa}")
            if combinação == senha:
                print("Sua senha foi quebrada pelo computador!")
                if tentativa >= 10000000000:
                    print("Paramos os testes por segurança!")
                    break
                else:
                    pass
            else:
                pass
    else:
        while True:
            combinação = random.choices(dado,k=digito)
            if combinação == senha:
                print("Sua senha foi quebrada pelo computador!")
            else:
                pass
  
        
numeros = "1234567890"
alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
simbolos = "!@#$%^&*()-_=+[{]};:,.<>?/|" 
tentativas = 0

senha = input("Me diga sua senha forte:")
tipo_de_senha = analisar(senha,numeros,alfabeto,simbolos)
digitos = contar_caracteres(senha)
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
            tentativas +=1 
            print(f"Senha testada:{senhas},Tentiva:{tentativas}")
            if senhas == senha:
                print("Sua senha foi achada na wordlist!")
                break
        else:
            if senhas == senha:
                print("Sua senha foi achada na wordlist!")
                break
    else:
        opn2 = int(input("Sua senha não foi encontrada na wordlist,você deseja tentar um ataque de força bruta nela?\n 1-Sim/2-Não:"))
        if opn2 == 1:
            print(*"=")
            print("Vamos testar sua senha!")
            print(*"=")
            testar(digitos,tipo_de_senha,ver_senhas,senha)
        else:
            print("tudo bem,sua senha é forte!")