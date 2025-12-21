import socket
from datetime import datetime
import sys

# Intervalo de portas a serem verificadas
PORTAS_COMUNS = range(1, 1025)

def scan_portas(ip_alvo):
    """
    Realiza a varredura das portas de um IP alvo.
    """
    print("-" * 50)
    print(f"Iniciando varredura em: {ip_alvo}")
    print("-" * 50)
    
    # Registra o tempo de início para calcular a duração total
    tempo_inicio = datetime.now()
    
    portas_abertas = {}
    
    # 1. Tenta resolver o nome do host (DNS)
    try:
        nome_host = socket.gethostbyaddr(ip_alvo)[0]
    except socket.error:
        nome_host = "N/A"
        
    print(f"Nome do Host: {nome_host}")
    print("-" * 50)

    try:
        for porta in PORTAS_COMUNS:
            # Cria um objeto socket
            # AF_INET = IPv4, SOCK_STREAM = TCP
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Define um timeout de 1 segundo para não travar o script
            s.settimeout(1.0) 
            
            # Tenta se conectar à porta
            resultado = s.connect_ex((ip_alvo, porta))
            
            if resultado == 0:
                # Se connect_ex retornar 0, a conexão foi bem-sucedida (porta aberta)
                
                # Tenta descobrir o serviço (HTTP, SSH, etc.) associado à porta
                try:
                    servico = socket.getservbyport(porta, 'tcp')
                except OSError:
                    servico = "Serviço Desconhecido"
                    
                portas_abertas[porta] = servico
                print(f"Porta {porta} aberta ({servico})")
            
            s.close() # Fecha a conexão
            
    except KeyboardInterrupt:
        print("\nVarredura interrompida pelo usuário.")
        sys.exit()
    except socket.gaierror:
        print("Nome do Host não pôde ser resolvido.")
        sys.exit()
    except socket.error:
        print("Não foi possível conectar ao servidor.")
        sys.exit()
        
    # Exibe o resultado final no formato solicitado (adaptado)
    print("\n" + "=" * 50)
    print("RESUMO DAS PORTAS ABERTAS")
    print("=" * 50)
    
    if portas_abertas:
        for porta, servico in portas_abertas.items():
            print(f"Porta {porta}: {servico}")
    else:
        print("Nenhuma porta comum aberta encontrada neste intervalo.")

    # Calcula e exibe o tempo total
    tempo_fim = datetime.now()
    duracao = tempo_fim - tempo_inicio
    print("-" * 50)
    print(f"Varredura concluída em: {duracao}")
    print("-" * 50)

# --- Execução Principal ---
if __name__ == "__main__":
    
    print("\n--- Python Port Scanner Simples ---")
    
    # 2. Recebe o IP ou Hostname do usuário
    ip_do_usuario = input("Digite o endereço IP ou nome de host para varrer: ")
    
    # 3. Tenta converter o host em IP, se for um nome (ex: google.com)
    try:
        ip_alvo = socket.gethostbyname(ip_do_usuario)
        scan_portas(ip_alvo)
    except socket.gaierror:
        print(f"\n[ERRO] Não foi possível resolver o endereço '{ip_do_usuario}'. Verifique o IP/Host.")
