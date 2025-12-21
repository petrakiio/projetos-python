import time
import random

<<<<<<< HEAD
#--- Funções ---
def caminhada():
    if random.randint(1,3) == 1:
        print("Caminhando....")
        time.sleep(30)
    elif random.randint(1,3) == 2:
        print("Caminhando...")
        time.sleep(20)
    else:
        print("Caminhando...")
        time.sleep(15)


=======
>>>>>>> c3eb3d1c0f8c49e1c77896914aa536666c39e5bd
class Personagem:
    def __init__(self, nome, vida, ataque, defesa):
        self.nome = nome
        self.vida = vida
        self.ataque = ataque
        self.defesa = defesa
        self.ferido = False
        self.rage = False
<<<<<<< HEAD
        self.inventario = []
=======
>>>>>>> c3eb3d1c0f8c49e1c77896914aa536666c39e5bd

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
<<<<<<< HEAD
    def item_panela(self,item):
        self.inventario.append(item)
        self.vida += self.vida * 0.30
        self.ataque -= self.ataque * 0.20

    def item_faca(self,item):
        self.inventario.append(item)
=======
    def item_panela(self):
        self.vida += self.vida * 0.30
        self.ataque -= self.ataque * 0.20

    def item_faca(self):
>>>>>>> c3eb3d1c0f8c49e1c77896914aa536666c39e5bd
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

<<<<<<< HEAD
#--- mini cheat
if nome_prota == "petrakiiopy":
    prota = Personagem(nome_prota,10000,9999.9,10000)
else:
    prota = Personagem(nome_prota, 100, ataque_prota, 100)

# --- Sistema de itens ---#
if opcão_obj == 1:
    print("Sorteando seu item!\n")
    time.sleep(0.2)
    if item == 'Panela':
        print("O item escolhido foi a panela!!\n A panela te dá 30% de buff de vida!!\n")
        prota.item_panela(item)
        print("Sua vida é:",prota.vida)
    elif item == 'Faca':
        print("Seu item escolhido foi a Faca!!\n A Faca te da um buff de 40% de ataque!!\n")
        prota.item_faca(item)
=======

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
>>>>>>> c3eb3d1c0f8c49e1c77896914aa536666c39e5bd
        print("Seu ataque atual:",prota.ataque)
    else:
        pass

<<<<<<< HEAD
=======

#     ataque_prota = float(input("Ataque (menor que 100): "))
#     if ataque_prota >= 100 or ataque_prota >= 99.9:
#         print("Valor inválido. Ataque deve ser menor que 100.")
#     else:
#         break

# prota = Personagem(nome_prota, 100, ataque_prota, 100)

>>>>>>> c3eb3d1c0f8c49e1c77896914aa536666c39e5bd
# --- Inimigos ---
demiurgo = Personagem("Demiurgo", 100, 80, 80)
goblin = Personagem("Goblin", 70, 30, 80)
escorpiao = Personagem("Escorpião", 100, 20, 80)
vampiro = Personagem("Vampiro", 1000, 45, 20)
gorgona = Personagem("Górgona", 100, 25, 90)

<<<<<<< HEAD

inimigo_inicia = random.choice([demiurgo, goblin, escorpiao, vampiro, gorgona])

falas_inimigos = [
    f"{inimigo_inicia.nome}: Seu nome é {prota.nome}, né? Você morrerá em minhas mãos.",
    f"{inimigo_inicia.nome}: Vou te ensinar a não entrar no meu território.",
    f"{inimigo_inicia.nome}: Hoje será o seu fim, {prota.nome}.",
    f"{inimigo_inicia.nome}: Você teve coragem de vir até aqui? Arrependa-se!",
    f"{inimigo_inicia.nome}: Não há escapatória para você, {prota.nome}!"
]
#--- inimigos caverna
toupera = Personagem("Toupera Humana",85,15,80)
slime = Personagem("Slime",45,25,40)
pedra = Personagem("Pedra-louca",140,1,30)

inimigo_caverna1 = random.choice([toupera,slime,pedra])

falas_inimigos_Caverna1 = [
    f"{inimigo_caverna1}:Vá embora da nossa casa!!",
    f"{inimigo_caverna1}:Você quer mesmo apanhar não é?"
    f"{inimigo_caverna1}:Você teve coragem de achar nosso lar hein?",
    f"{inimigo_caverna1}:Porque você está fazendo isso?"
]


print(f"\nVocê encontrou o temido {inimigo_inicia}!\n")
print(f"Status\nNome → {inimigo_inicia.nome}\nVida → {inimigo_inicia.vida}\nAtaque → {inimigo_inicia.ataque}")
=======
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
>>>>>>> c3eb3d1c0f8c49e1c77896914aa536666c39e5bd

# --- Loop principal da batalha ---
while True:
    print("\n--- Sua vez ---")
<<<<<<< HEAD
    acao = input("Atacar, Curar, Fugir ou Poupar? (1 para status,2 pra inventario): ").lower()

    if acao == "atacar":
        prota.atacar(inimigo_inicia)
=======
    acao = input("Atacar, Curar, Fugir ou Poupar? (1 para status): ").lower()

    if acao == "atacar":
        prota.atacar(inimigo)
>>>>>>> c3eb3d1c0f8c49e1c77896914aa536666c39e5bd
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
<<<<<<< HEAD
            print(f"O inimigo {inimigo_inicia.nome} foi poupado e fugiu!")
            break
        else:
            print(f"{inimigo_inicia.nome}: Você acha que pode me poupar? Ridículo!")
    elif acao == "1":
        prota.status()
        inimigo_inicia.status()
        continue
    elif acao == "2":
        print("Itens:",*prota.inventario)
=======
            print(f"O inimigo {inimigo.nome} foi poupado e fugiu!")
            break
        else:
            print(f"{inimigo.nome}: Você acha que pode me poupar? Ridículo!")
    elif acao == "1":
        prota.status()
        inimigo.status()
        continue
>>>>>>> c3eb3d1c0f8c49e1c77896914aa536666c39e5bd
    else:
        print("Ação inválida.")
        continue

<<<<<<< HEAD
    if inimigo_inicia.morto():
        print(f"\n{inimigo_inicia.nome} foi derrotado! 🏆")
        break

    inimigo_inicia.sistema_ferido()

    # --- Turno do inimigo ---
    print(f"\n--- Turno do {inimigo_inicia.nome} ---")
=======
    if inimigo.morto():
        print(f"\n{inimigo.nome} foi derrotado! 🏆")
        break

    inimigo.sistema_ferido()

    # --- Turno do inimigo ---
    print(f"\n--- Turno do {inimigo.nome} ---")
>>>>>>> c3eb3d1c0f8c49e1c77896914aa536666c39e5bd
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
<<<<<<< HEAD

#--- Escolha de campanha --- 
print(f"você saiu vitorio {prota.nome}\n Quer continuar sua jornada?\n")
resposta_jornada = int(input("1-Sim or 2-Não:"))
if resposta_jornada == 1:
    pass
else:
    print("Você foi um bom guerreiro")

caminhada()

#---Caverna 1 ---
print('"Após um bom tempo de caminhada você acha uma caverna e a adentra"\n Você acha um báu você se aproxima?')
escolha_caverna1 = int(input("1-Sim or 2-Não:"))
if escolha_caverna1 == 1:
    if random.randint(1,2) is not 1:
        print(f"O terrivel {inimigo_caverna1} vem pra te impedir")
        print(random.choice(falas_inimigos_Caverna1))
        prota.status()
=======
>>>>>>> c3eb3d1c0f8c49e1c77896914aa536666c39e5bd
