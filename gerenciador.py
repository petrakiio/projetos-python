from cryptography.fernet import Fernet
from pathlib import Path

CHAVE_FILE = "chave.key"

def carregar_ou_gerar_chave():
    """Carrega a chave se existir, senão, gera uma nova e a salva."""
    chave_path = Path(CHAVE_FILE)
    if chave_path.is_file():
        print("Chave de criptografia carregada.")
        return chave_path.read_bytes()
    else:
        nova_chave = Fernet.generate_key()
        chave_path.write_bytes(nova_chave)
        print(f"Nova chave gerada e salva em '{CHAVE_FILE}'.")
        return nova_chave

chave = carregar_ou_gerar_chave()
fernet = Fernet(chave)
caminho_arquivo_hash = Path("hash.txt")

def criptografar(dado):
    return fernet.encrypt(dado.encode()).decode() 

def descriptografar(dado_criptografado_str):
    return fernet.decrypt(dado_criptografado_str.encode()).decode()

def buscar_senhas(caminho):
    if not caminho.is_file():
        return []
        
    senhas_descriptografadas = []
    
    try:
        with open(caminho, "r") as hashs:
            for linha_criptografada in hashs:
                linha_limpa = linha_criptografada.strip()

                if linha_limpa: 
                    try:
                        senha_descriptografada = descriptografar(linha_limpa)
                        senhas_descriptografadas.append(senha_descriptografada)
                    except Exception as e:
                        print(f"ATENÇÃO: Não foi possível descriptografar uma linha. Chave errada ou dado corrompido.")
        return senhas_descriptografadas
        
    except Exception as error:
        print(f"Erro ao ler o arquivo: {error}")
        return []


def adicionar_senha(senha_criptografada_str, arquivo_path):
    try:
        with open(arquivo_path, "a") as f:
            f.write(senha_criptografada_str + "\n") 
            return True
    except Exception as e:
        print(f"Erro ao escrever no arquivo: {e}")
        return False

if not caminho_arquivo_hash.is_file():
     with open(caminho_arquivo_hash, "w") as f:
         pass

while True:
    print("\n" + "="*40)
    print("Bem Vindo ao gerenciador de senhas!!!")
    print("="*40)
    print("1- Ver senhas")
    print("2- Adicionar Senha")
    print("3- Sair")
    
    try:
        opn = int(input("R: "))
    except ValueError:
        print("Digite um número válido (1, 2 ou 3).")
        continue

    if opn == 1:
        senhas_opn1 = buscar_senhas(caminho_arquivo_hash)
        
        if not senhas_opn1:
            print("Nenhuma senha armazenada ou erro na leitura.")
        else:
            print("\n--- SENHAS ARMAZENADAS ---")
            for n, senha in enumerate(senhas_opn1, 1):
                print(f"{n}º Senha: {senha}")
            print("---------------------------")      
    elif opn == 2:
        senha_limpa = input("Digite a senha a ser armazenada: ")
        senha_criptografada_str = criptografar(senha_limpa)
        
        retorno = adicionar_senha(senha_criptografada_str, caminho_arquivo_hash)
        
        if retorno:
            print("✅ Senha adicionada e criptografada com sucesso!")
        else:
            print("❌ Erro ao adicionar senha.") 
    elif opn == 3:
        print("Saindo. Não perca seu arquivo 'chave.key'!")
        break  
    else:
        print("Digite um número válido (1, 2 ou 3).")