"""
Get Arquives with python
"""

#Import libs
import os

home = os.path.expanduser("~")
pastas = ['Documentos','Imagens','Downloads','Vídeos','Músicas','Modelos']

def search(arq):
    for p in pastas:
        caminho = os.path.join(home, p)
        if os.path.isdir(caminho):
            arquivos = os.listdir(caminho)
            if arq in arquivos:
                print(f'Arquivo encontrado em:[{caminho}/{arq}]')
                break
        else:
            print(f"\nPasta não encontrada: {caminho}")

def Main():
    print('='*30)
    print('1-Buscar Arquivos')
    print('2-fechar')
    print('='*30)