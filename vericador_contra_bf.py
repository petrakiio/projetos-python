import time
from itertools import product

# Conjuntos de caracteres
NUMEROS = "0123456789"
ALFABETO = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
SIMBOLOS = "!@#$%^&*()-_=+[{]};:,.<>?/|"


def analisar_senha(senha):
    tem_num = any(c in NUMEROS for c in senha)
    tem_letra = any(c in ALFABETO for c in senha)
    tem_simbolo = any(c in SIMBOLOS for c in senha)

    if tem_num and tem_letra and tem_simbolo:
        return "MISTA"
    elif tem_num and not tem_letra and not tem_simbolo:
        return "NUM"
    elif tem_letra and not tem_num and not tem_simbolo:
        return "LETRAS"
    elif tem_simbolo and not tem_num and not tem_letra:
        return "SIMBOLOS"
    else:
        return "COMPOSTA"


def escolher_charset(tipo):
    if tipo == "NUM":
        return NUMEROS
    elif tipo == "LETRAS":
        return ALFABETO
    elif tipo == "SIMBOLOS":
        return SIMBOLOS
    else:
        return NUMEROS + ALFABETO + SIMBOLOS


def ataque_wordlist(senha, ver):
    tentativas = 0
    try:
        with open("password-wordlist.txt", "r", encoding="utf-8", errors="ignore") as wordlist:
            for linha in wordlist:
                tentativa = linha.strip()
                tentativas += 1

                if ver:
                    print(f"[{tentativas}] Testando: {tentativa}")

                if tentativa == senha:
                    print(f"\nSenha encontrada na wordlist em {tentativas} tentativas!")
                    return True
    except FileNotFoundError:
        print("Wordlist não encontrada.")

    return False


def ataque_bruteforce(senha, ver):
    tipo = analisar_senha(senha)
    charset = escolher_charset(tipo)
    tamanho = len(senha)

    print(f"\nIniciando brute force | Tipo: {tipo} | Charset: {len(charset)} caracteres")

    inicio = time.time()
    tentativas = 0

    for comb in product(charset, repeat=tamanho):
        tentativa = "".join(comb)
        tentativas += 1

        if ver:
            print(f"[{tentativas}] {tentativa}")

        if tentativa == senha:
            fim = time.time()
            print("\n🔥 SENHA QUEBRADA 🔥")
            print(f"Senha: {tentativa}")
            print(f"Tentativas: {tentativas}")
            print(f"Tempo: {fim - inicio:.2f} segundos")
            return

    print("Não foi possível quebrar a senha.")


# ================= PROGRAMA PRINCIPAL =================

senha = input("Digite sua senha para teste: ")

ver = input("Deseja ver as tentativas? (s/n): ").lower() == "s"

print("\nAnalisando senha...")
tipo = analisar_senha(senha)
print(f"Tipo da senha: {tipo}")
print(f"Tamanho: {len(senha)} caracteres")

print("\nTentando wordlist...")
if not ataque_wordlist(senha, ver):
    escolha = input("\nSenha não encontrada. Tentar brute force? (s/n): ").lower()
    if escolha == "s":
        ataque_bruteforce(senha, ver)
    else:
        print("Ok! Senha considerada segura contra wordlist.")
