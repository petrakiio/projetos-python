import requests

def Buscar_CEP(cep):
    url = f"https://viacep.com.br/ws/{cep}/json/"
    reposta = requests.get(url)
    dados = reposta.json()
    if "erro" in dados:
        return "Erro no CEP"
    else:
        cidade = {
            "Rua":dados['logradouro'],
            "Bairro":dados["bairro"],
            "Cidade":dados["localidade"],
            "Estado":dados["uf"]
        }
        return cidade
    
def Buscar_ip(ip):
    url = ""