import time
import random
import qrcode

# --- Funções ---
def apoiar():
    opn = int(input("Gostaria de me apoiar olhando outros projetos?\n1-Sim/2-Não:"))
    if opn == 1:
        url = "https://petrakiio.github.io/WoodLab/"
        img = qrcode.make(url)
        img.save("Qrcode.png")
        img.show()
    else:
        print("Tudo bem,Obrigado por jogar meu mini jogo!")

def caminhada(item,prota):
    print("\nCaminhando...")
    tempo = random.choice([15, 20, 30])
    time.sleep(tempo / 10) 
    print("Você seguiu adiante...")
    chance = random.randint(1,10)
    if chance == 5:
        print(*"=")
        print("Você achou um báu,quer abrir?")
        print(*"=")
        opn = int(input("1-Sim/2-Não:"))
        if opn == 1:
            if prota.inventario_cheio == True:
                print("Inventario cheio")
            else:
                prota.inventario.append(item)
                print("item adicionado ao jogador")
        else:
            print("Você ignora o item")


def credibilidade_bondade(resultado,prota):
    if resultado == 'vitoria':
        prota.credibilidade += 20
    elif resultado == 'poupado':
        prota.bondade += 20
    elif resultado == 'fugiu':
        prota.fuga += 20
    else:
        pass
def dar_item(prota,itens):
    item_nome = random.choice(list(itens.keys()))
    item = itens[item_nome]

    prota.inventario.append(item_nome)
    print(item["msg"])

    prota.max_vida *= item["vida_mult"]
    prota.vida = prota.max_vida
    prota.ataque *= item["ataque_mult"]

def agradecimentos(final):
    print("="*30)
    print(f" ~~~ Desbloqueou final:{final.upper()} ~~~")
    print("="*30)
    print("Obrigado por jogar,espero que tenha gostado da minha experiencia!!")
    print("Este é dos meus primeiros projetos de game em python!")
    print("="*30)

class Personagem:
    def __init__(self, nome, vida, ataque, defesa):
        self.nome = nome
        self.vida = vida
        self.max_vida = vida
        self.ataque = ataque
        self.defesa = defesa
        self.ferido = False
        self.rage = False
        self.credibilidade = 0
        self.bondade = 0
        self.fuga = 0
        self.inventario = []
        self.inventario_cheio = False
        self.contado = 0

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
    while True:
        for itens in inventario:
            self.contado +=1
            if contado >=5:
                self.inventario_cheio = True
                break
            else:
                pass

    def cura(self):
        bonus = random.randint(1, 2)
        cura_total = 30 if bonus == 2 else 15
        print(f"{self.nome} curou {cura_total} de vida!")
        self.vida = min(self.max_vida, self.vida + cura_total)

    def status(self):
        print(f"{self.nome} → Vida: {self.vida:.0f} | Ataque: {self.ataque:.1f} | Defesa: {self.defesa}")

    def morto(self):
        return self.vida <= 0

    def verificar_final(self):
        if self.credibilidade >= 40:
            return "hero"
        elif self.bondade >= 40:
            return "pacifist"
        elif self.fuga >=40:
            return "cagão"
        else:
            return "neutro"

# --- Lógica de Combate ---
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
#itens baús
itens_bau = {
    ""
}
# Itens Iniciais
itens = {
    "Panela": {
        "vida_mult": 1.3,
        "ataque_mult": 0.8,
        "msg": "Você pegou a Panela! (+Vida, -Ataque)"
    },
    "Faca": {
        "vida_mult": 1.0,
        "ataque_mult": 1.4,
        "msg": "Você pegou a Faca! (+Ataque)"
    },
    "Espada":{
        "vida_mult":1.0,
        "ataque_mult":2.5,
        "msg":"Você pegou a espada!(+Ataque)"
    },
    "Armadura":{
        "vida_mult":2.5,
        "ataque_mult":0.6,
        "msg":"Você pegou a armadura(+Vida,-Ataque)"
    }
}

if input("Quer um Item Aleatorio? (1-Sim / 2-Não): ") == "1":
    dar_item(prota,itens)
else:
    pass

inimigos_mundo = [
    Personagem("Demiurgo", 100, 40, 50),
    Personagem("Goblin", 70, 30, 40),
    Personagem("Vampiro", 120, 45, 20)
]

inimigo_atual = random.choice(inimigos_mundo)
falas = ["Vou te esmagar!", "Você é fraco!", "Sinta minha fúria!"]

# Boss final
king = Personagem("Rei Demonio", 200,40,50)
falas_boss = ["Você ousa desafiar o rei?","Vá embora humano,você não é ninguém","Você conhecerá o poder de um rei!"]



resultado = sistema_de_combate(prota, inimigo_atual, falas)

if resultado == "vitoria" or resultado == "poupado":
    credibilidade_bondade(resultado,prota)
    print(f"\nVocê seguiu adiante, {prota.nome}!")
    caminhada()
    
    #Caverna
    print("\nVocê encontrou uma caverna escura. Entrar?")
    if input("1-Sim / 2-Não: ") == "1":
        caverna_inimigo = Personagem("Toupeira Humana", 85, 15, 80)
        falas_caverna = ["Saia da minha casa!", "O brilho nos seus olhos me irrita!"]
        resultado_caverna = sistema_de_combate(prota, caverna_inimigo, falas_caverna)
        if resultado_caverna == "vitoria" or  resultado_caverna == "poupado":
            credibilidade_bondade(resultado_caverna,prota)  
            print("--- Você abre o báu e encontra uma espada sagrada,Você a pega?")
            escolha_espada = int(input("1-Sim/2-Não:"))
            if escolha_espada == 1:
                print("--- Você pegou a espada ---")
                prota.inventario.append("Espada Sagrada")
                print("--- um anjo desce do céu e te da uma missão pra derrotar o rei demonio,Você aceita? ---")
                escolha_quest = int(input("1-Sim/2-Não:"))
                if escolha_quest == 1:
                    print("--- Você aceita a missão do anjo e marcha até os confins do submundo atrás do rei demonio --- \n")
                    print(f"{king.nome}:Você não é só corajoso de me enfrentar é um tolo por vir morrer nas minhas mãos!")
                    luta_final = sistema_de_combate(prota,king,falas_boss)
                    credibilidade_bondade(luta_final,prota)
                    if luta_final == "vitoria" or luta_final == "poupado":
                        final = prota.verificar_final()
                        if  final  == "hero":
                            print("--- Após derotar o famoso e temido rei demonio você continua sua jornada como guerreio,porém sendo lembrado como 'O Herio' ")
                            agradecimentos(final)
                            apoiar()
                        elif final == "pacifist":
                            print("--- No final você poupa o rei demonio e o tira do trono unificando todas as raças ---")
                            agradecimentos(final)
                            apoiar()
                        else:
                            print("--- Você consegue comprir a missão do anjo e trazer paz a terra,continuando sua jornada! ---")
                            agradecimentos(final)
                            apoiar()
                else:
                    print("--- Você nega o pedido do anjo,afinal isso não é problema seu --- ")
                    final = "Isso é problema meu?"
                    agradecimentos(final)
                    apoiar()
            else:
                print("--- Você sai da caverna,uma batalha ganha atoa porém a jornada continua --- ")
                final = "guerreiro nada sagrado"
                agradecimentos(final)
                apoiar()
    else:
        print("--- Você ignora a caverna e continua suar jornada ---")
        final = "e eu sou mineiro?"
        agradecimentos(final)
        apoiar()
else:
    print("Fim da linha para você.")
    final = "heroi fracasso"
    agradecimentos(final)
    apoiar()