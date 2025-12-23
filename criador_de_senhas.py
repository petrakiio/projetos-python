import random 

numeros = "1234567890"
alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
simbolos = "!@#$%^&*()-_=+[{]};:,.<>?/|"

dados = numeros+alfabeto+simbolos

vezes = int(input("Me diga quantas vocês você quer refazer uma senha?:"))
digitos = int(input("Ela deve ter quantos digitos?:"))

print("Vamos gerar sua senha!")

for i in range(vezes):
    senha = "".join(random.choices(dados,k=digitos))
    
print("Sua senha:",senha)