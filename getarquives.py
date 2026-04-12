"""
Get Arquives with python
"""

#Import libs
import os

home = os.path.expanduser("~")
pastas = ['Documentos','Imagens','Downloads','Vídeos','Músicas','Modelos']

def search():
    for p in pastas:
        caminho = os.path.join(home, p)
        if os.path.isdir(caminho):
            arquivos = os.listdir(caminho)
            print(f"\n== {caminho} ==")
            print(arquivos)
        else:
            print(f"\nPasta não encontrada: {caminho}")

search()
