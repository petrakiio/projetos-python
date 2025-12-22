import time
import random

# --- Funções de Utilidade ---
def caminhada():
    print("\nCaminhando...")
    tempo = random.choice([15, 20, 30])
    time.sleep(tempo / 10) # Reduzi o tempo para testes, mude para 'tempo' para o original
    print("Você seguiu adiante...")

class Personagem:
    def __init__(self, nome, vida, ataque, defesa):
        self.nome = nome
        self.vida = vida
        self.max_vida = vida
        self.ataque = ataque
        self.defesa = defesa
        self.ferido = False
        self.rage = False
        self.inventario = []

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
        cura_total = 30 if bonus == 2 else 15
        print(f"{self.nome} curou {cura_total} de vida!")
        self.vida = min(self.max_vida, self.vida + cura_total)

    def status(self):
        print(f"{self.nome} → Vida: {self.vida:.0f} | Ataque: {self.ataque:.1f} | Defesa: {self.defesa}")

    def morto(self):
        return self.vida <= 0

# --- Lógica de Combate Centralizada ---
def sistema_de_combate(prota, inimigo, falas_inimigo):
    print(f"\n--- INÍCIO DA BATALHA: {prota.nome} VS {inimigo.nome} ---")
    
    while not prota.morto() and not inimigo.morto():
        print("\n--- Sua vez ---")
        acao = input("Atacar, Curar, Fugir ou Poupar? (1: Status | 2: Itens): ").lower()

        if acao == "atacar":
            prota.atacar(inimigo)
        elif acao == "curar":
            prota.cura()
        elif acao == "fugir":
            if random.randint(1, 2) == 1:
                print("Você fugiu!")
                return "fugiu"
            print("Fuga falhou!")
        elif acao == "poupar":
            if random.randint(1, 2) == 1:
                print(f"O inimigo {inimigo.nome} foi poupado!")
                return "poupado"
            print(f"{inimigo.nome} recusa sua piedade!")
        elif acao == "1":
            prota.status()
            inimigo.status()
            continue
        elif acao == "2":
            print("Inventário:", prota.inventario)
            continue
        
        if inimigo.morto():
            print(f"\n{inimigo.nome} foi derrotado! 🏆")
            return "vitoria"

        # Turno do Inimigo
        print(f"\n--- Turno do {inimigo.nome} ---")
        time.sleep(0.5)
        inimigo.sistema_ferido()
        
        if random.random() > 0.3:
            inimigo.atacar(prota)
        else:
            inimigo.cura()
            
        if random.randint(1, 2) == 1:
            print(f"> {inimigo.nome}: {random.choice(falas_inimigo)}")

        prota.sistema_ferido()
        prota.status()
        inimigo.status()

    if prota.morto():
        print(f"\n{prota.nome} caiu em batalha...")
        return "derrota"


nome_prota = input("Nome do seu personagem: ")
ataque_prota = float(input("Ataque (menor que 100): "))
if ataque_prota >= 100: ataque_prota = 99

prota = Personagem(nome_prota, 100, ataque_prota, 100)

# Cheat Mode
if nome_prota == "petrakiiopy":
    prota.vida = prota.max_vida = 10000
    prota.ataque = 9999

# Itens Iniciais
if input("Quer um Item Aleatorio? (1-Sim / 2-Não): ") == "1":
    item = random.choice(['Panela', 'Faca'])
    prota.inventario.append(item)
    if item == 'Panela':
        print("Você pegou a Panela! (+Vida, -Ataque)")
        prota.max_vida *= 1.3
        prota.vida = prota.max_vida
        prota.ataque *= 0.8
    else:
        print("Você pegou a Faca! (+Ataque)")
        prota.ataque *= 1.4

# --- Início da Jornada ---
inimigos_mundo = [
    Personagem("Demiurgo", 100, 40, 50),
    Personagem("Goblin", 70, 30, 40),
    Personagem("Vampiro", 120, 45, 20)
]

inimigo_atual = random.choice(inimigos_mundo)
falas = ["Vou te esmagar!", "Você é fraco!", "Sinta minha fúria!"]

resultado = sistema_de_combate(prota, inimigo_atual, falas)

if resultado == "vitoria" or resultado == "poupado":
    print(f"\nVocê seguiu adiante, {prota.nome}!")
    caminhada()
    
    #Caverna
    print("\nVocê encontrou uma caverna escura. Entrar?")
    if input("1-Sim / 2-Não: ") == "1":
        caverna_inimigo = Personagem("Toupeira Humana", 85, 15, 80)
        falas_caverna = ["Saia da minha casa!", "O brilho nos seus olhos me irrita!"]
        sistema_de_combate(prota, caverna_inimigo, falas_caverna)
else:
    print("Fim da linha para você.")