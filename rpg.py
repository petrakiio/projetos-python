import time
import random

class Personagem:
    def __init__(self, nome, vida, ataque, defesa):
        self.nome = nome
        self.vida = vida
        self.ataque = ataque
        self.defesa = defesa
        self.ferido = False
        self.rage = False

    def __str__(self):
        return self.nome

    def atacar(self, alvo):
        n = random.randint(0, 3)
        if n == 1:
            critico = self.ataque * 2
            dano = max(0, critico - alvo.defesa / 10)
            alvo.vida -= dano
            print(f"{self.nome} deu um ATAQUE CRÍTICO de {dano:.0f} em {alvo.nome}!")
        elif n == 2:
            dano = max(0, self.ataque - alvo.defesa / 10)
            alvo.vida -= dano
            print(f"{self.nome} deu {dano:.0f} de dano em {alvo.nome}.")
        elif n == 3:
            print(f"{self.nome} feriu {alvo.nome}!")
            alvo.ferido = True
        else:
            print(f"{alvo.nome} desviou do ataque!")

    def sistema_ferido(self):
        if self.ferido and self.vida > 0:
            ferimento = self.ataque / 2
            self.vida -= ferimento
            print(f"{self.nome} está sangrando e perdeu {ferimento:.0f} de vida!")

    def cura(self):
        bonus = random.randint(1, 2)
        if bonus == 2:
            cura_total = 30
            print(f"{self.nome} recebeu bônus e curou {cura_total} de vida!")
        else:
            cura_total = 15
            print(f"{self.nome} curou {cura_total} de vida!")
        self.vida = min(100, self.vida + cura_total)
    def item_panela(self):
        self.vida += self.vida * 0.30
        self.ataque -= self.ataque * 0.20

    def item_faca(self):
        if not self.rage:
            self.ataque += self.ataque * 0.40
            self.rage = True

    def status(self):
        print(f"{self.nome} → Vida: {self.vida:.0f} | Ataque: {self.ataque} | Defesa: {self.defesa}")

    def morto(self):
        return self.vida <= 0

# --- Itens ---
itens = ['Panela','Faca']
item = random.choice(itens)
# --- Criação do jogador ---
nome_prota = input("Nome do seu personagem: ")
opcão_obj = int(input("Quer um Item Aleatorio?(Isso custa 20% do seu ataque)\n 1-Sim ou 2-Não:"))
ataque_prota = float(input("Ataque (menor que 100): "))

# --- Verificação de Ataque
while ataque_prota >= 100:
    ataque_prota = float(input("Valor inválido. Ataque menor que 100: "))


prota = Personagem(nome_prota, 100, ataque_prota, 100)
# --- Sistema de itens ---#
if opcão_obj == 1:
    print("Sorteando seu item!")
    time.sleep(0.2)
    if item == 'Panela':
        print("O item escolhido foi a panela!!\n A panela te dá 30% de buff de vida!!")
        prota.item_panela()
        print("Sua vida é:",prota.vida)
    elif item == 'Faca':
        print("Seu item escolhido foi a Faca!!\n A Faca te da um buff de 40% de ataque")
        prota.item_faca()
        print("Seu ataque atual:",prota.ataque)
    else:
        pass


#     ataque_prota = float(input("Ataque (menor que 100): "))
#     if ataque_prota >= 100 or ataque_prota >= 99.9:
#         print("Valor inválido. Ataque deve ser menor que 100.")
#     else:
#         break

# prota = Personagem(nome_prota, 100, ataque_prota, 100)

# --- Inimigos ---
demiurgo = Personagem("Demiurgo", 100, 80, 80)
goblin = Personagem("Goblin", 70, 30, 80)
escorpiao = Personagem("Escorpião", 100, 20, 80)
vampiro = Personagem("Vampiro", 1000, 45, 20)
gorgona = Personagem("Górgona", 100, 25, 90)

inimigo = random.choice([demiurgo, goblin, escorpiao, vampiro, gorgona])

falas_inimigos = [
    f"{inimigo.nome}: Seu nome é {prota.nome}, né? Você morrerá em minhas mãos.",
    f"{inimigo.nome}: Vou te ensinar a não entrar no meu território.",
    f"{inimigo.nome}: Hoje será o seu fim, {prota.nome}.",
    f"{inimigo.nome}: Você teve coragem de vir até aqui? Arrependa-se!",
    f"{inimigo.nome}: Não há escapatória para você, {prota.nome}!"
]

print(f"\nVocê encontrou o temido {inimigo}!\n")
print(f"Status\nNome → {inimigo.nome}\nVida → {inimigo.vida}\nAtaque → {inimigo.ataque}")

# --- Loop principal da batalha ---
while True:
    print("\n--- Sua vez ---")
    acao = input("Atacar, Curar, Fugir ou Poupar? (1 para status): ").lower()

    if acao == "atacar":
        prota.atacar(inimigo)
    elif acao == "curar":
        prota.cura()
    elif acao == "fugir":
        if random.randint(1, 2) == 1:
            print("Você conseguiu fugir com sucesso!")
            break
        else:
            print("O inimigo impediu sua fuga!")
            continue
    elif acao == "poupar":
        if random.randint(1, 2) == 1:
            print(f"O inimigo {inimigo.nome} foi poupado e fugiu!")
            break
        else:
            print(f"{inimigo.nome}: Você acha que pode me poupar? Ridículo!")
    elif acao == "1":
        prota.status()
        inimigo.status()
        continue
    else:
        print("Ação inválida.")
        continue

    if inimigo.morto():
        print(f"\n{inimigo.nome} foi derrotado! 🏆")
        break

    inimigo.sistema_ferido()

    # --- Turno do inimigo ---
    print(f"\n--- Turno do {inimigo.nome} ---")
    time.sleep(1)
    if random.randint(1, 2) == 1:
        inimigo.atacar(prota)
    else:
        inimigo.cura()

    if random.randint(1, 2) == 1:
        print(random.choice(falas_inimigos))

    prota.sistema_ferido()

    if prota.morto():
        print(f"\n{prota.nome} foi derrotado...")
        print(f"{prota.nome}, não desista! Tenha determinação ❤️")
        determinacao = input("Você tem determinação? (sim/não): ").lower()
        if determinacao == "sim":
            print(f"*{prota.nome} retornou ao mundo e continuou sua jornada...*")
            break
        else:
            print(f"*{prota.nome} morreu na batalha contra {inimigo.nome}*")
            break

    print("\nStatus:")
    prota.status()
    inimigo.status()

    # pode relatar os erros?