import tkinter as tk
import time
import random

BG = "#0b1f0b"
GREEN = "#00ff66"
DARK = "#003300"

def atualizar_hora():
    hora = time.strftime("%d/%m/%Y  %H:%M:%S")
    rodape.config(text=f"SYSTEM TIME: {hora}")
    janela.after(1000, atualizar_hora)

def mudar_tela(nome):
    conteudo.delete("1.0", tk.END)

    if nome == "STATUS":
        conteudo.insert(tk.END, ">> STATUS DO SISTEMA\n\n")
        conteudo.insert(tk.END, "Microfone: ONLINE\n")
        conteudo.insert(tk.END, "Câmera: DISPONÍVEL\n")
        conteudo.insert(tk.END, "API: CONECTADA\n")

    elif nome == "CAMERA":
        conteudo.insert(tk.END, ">> MODO CÂMERA ATIVO\n\n")
        conteudo.insert(tk.END, "[SIMULAÇÃO DE CAPTURA]\n")
        conteudo.insert(tk.END, "Detectando ambiente...\n")

    elif nome == "SINAIS":
        conteudo.insert(tk.END, ">> TRADUÇÃO DE SINAIS\n\n")
        sinais = ["Olá", "Tudo bem?", "Ajuda", "Obrigado"]
        conteudo.insert(tk.END, "Reconhecendo gesto...\n\n")
        conteudo.insert(tk.END, f"Tradução: {random.choice(sinais)}")

# =========================
# JANELA
# =========================
janela = tk.Tk()
janela.title("Pip-Boy Assistivo")
janela.geometry("850x500")
janela.configure(bg=BG)

frame_principal = tk.Frame(janela, bg=DARK, bd=4, relief="ridge")
frame_principal.pack(fill="both", expand=True, padx=20, pady=20)

# MENU
menu = tk.Frame(frame_principal, bg=BG, width=220)
menu.pack(side="left", fill="y")

titulo = tk.Label(
    menu,
    text="PIP-BOY\nASSISTIVO",
    bg=BG,
    fg=GREEN,
    font=("Courier", 16, "bold")
)
titulo.pack(pady=20)

for item in ["STATUS", "CAMERA", "SINAIS"]:
    btn = tk.Button(
        menu,
        text=item,
        bg=BG,
        fg=GREEN,
        activebackground=DARK,
        activeforeground=GREEN,
        font=("Courier", 12, "bold"),
        borderwidth=0,
        command=lambda i=item: mudar_tela(i)
    )
    btn.pack(pady=10, fill="x")

# CONTEÚDO
conteudo = tk.Text(
    frame_principal,
    bg=BG,
    fg=GREEN,
    insertbackground=GREEN,
    font=("Courier", 12),
    borderwidth=0
)
conteudo.pack(side="right", fill="both", expand=True, padx=20, pady=20)

rodape = tk.Label(janela, bg=BG, fg=GREEN, font=("Courier", 10))
rodape.pack()

mudar_tela("STATUS")
atualizar_hora()

janela.mainloop()
