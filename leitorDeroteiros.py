"""
docx_to_speech.py
Lê arquivos .docx em voz alta usando pyttsx3.
Compatível com Windows, macOS e Linux.
"""

import sys
import os

# ---------------------------------------------------------------------------
# Verificação de dependências
# ---------------------------------------------------------------------------
def check_dependencies():
    missing = []
    try:
        import docx  # noqa: F401
    except ImportError:
        missing.append("python-docx")
    try:
        import pyttsx3  # noqa: F401
    except ImportError:
        missing.append("pyttsx3")
    if missing:
        print("❌ Dependências faltando. Instale com:")
        print(f"   pip install {' '.join(missing)}")
        sys.exit(1)

check_dependencies()

# ---------------------------------------------------------------------------
# Imports após verificação
# ---------------------------------------------------------------------------
import glob
import textwrap
import pyttsx3
from docx import Document


# ---------------------------------------------------------------------------
# 1. Selecionar arquivo .docx
# ---------------------------------------------------------------------------
def selecionar_arquivo() -> str:
    """Lista arquivos .docx no diretório atual e permite digitar um caminho."""
    arquivos = sorted(glob.glob("**/*.docx", recursive=True))

    print("\n" + "=" * 60)
    print("  📄  LEITOR DE DOCUMENTOS WORD  ")
    print("=" * 60)

    if arquivos:
        print("\nArquivos .docx encontrados:")
        for i, arq in enumerate(arquivos, 1):
            print(f"  [{i}] {arq}")
        print()

    caminho = input("Digite o número do arquivo ou o caminho completo: ").strip()

    # Tentativa de usar número da lista
    if caminho.isdigit():
        idx = int(caminho) - 1
        if 0 <= idx < len(arquivos):
            return arquivos[idx]
        else:
            print("❌ Número inválido.")
            sys.exit(1)

    # Caminho digitado diretamente
    if not os.path.isfile(caminho):
        print(f"❌ Arquivo não encontrado: {caminho}")
        sys.exit(1)

    return caminho


# ---------------------------------------------------------------------------
# 2. Extrair texto do .docx
# ---------------------------------------------------------------------------
def extrair_texto(caminho: str) -> str:
    """Extrai todo o texto visível do documento Word."""
    doc = Document(caminho)
    paragrafos = [p.text for p in doc.paragraphs if p.text.strip()]
    texto = "\n".join(paragrafos)
    if not texto:
        print("⚠️  O documento parece estar vazio ou só contém imagens.")
        sys.exit(1)
    return texto


# ---------------------------------------------------------------------------
# 3. Inicializar engine e configurar velocidade
# ---------------------------------------------------------------------------
def criar_engine(taxa: int = 150) -> pyttsx3.Engine:
    """
    Cria a engine pyttsx3.
    taxa: palavras por minuto (padrão do sistema ≈ 150–200 wpm → 1×).
    """
    engine = pyttsx3.init()
    engine.setProperty("rate", taxa)
    engine.setProperty("volume", 1.0)  # volume máximo
    return engine


# ---------------------------------------------------------------------------
# 4. Listar e escolher voz PT-BR (ou qualquer voz disponível)
# ---------------------------------------------------------------------------
def escolher_voz(engine: pyttsx3.Engine) -> str | None:
    """
    Lista as vozes disponíveis, destaca as PT-BR e deixa o usuário escolher.
    Retorna o ID da voz selecionada (ou None para manter o padrão).
    """
    vozes = engine.getProperty("voices")

    # Separa PT-BR das demais
    vozes_ptbr = [v for v in vozes if "pt" in (v.languages[0] if v.languages else "").lower()
                  or "pt" in v.id.lower()
                  or "brazil" in v.name.lower()
                  or "português" in v.name.lower()
                  or "portuguese" in v.name.lower()]
    vozes_outras = [v for v in vozes if v not in vozes_ptbr]

    print("\n" + "-" * 60)
    print("  🎙️  VOZES DISPONÍVEIS  ")
    print("-" * 60)

    todas = vozes_ptbr + vozes_outras
    for i, voz in enumerate(todas, 1):
        lingua = voz.languages[0] if voz.languages else "desconhecida"
        tag = " ★ PT-BR" if voz in vozes_ptbr else ""
        print(f"  [{i:2}] {voz.name:<40} | {lingua}{tag}")

    print(f"  [ 0] Manter voz padrão do sistema")
    print("-" * 60)

    escolha = input("Escolha uma voz (número): ").strip()

    if escolha == "0" or escolha == "":
        print("✅ Usando voz padrão do sistema.")
        return None

    if escolha.isdigit():
        idx = int(escolha) - 1
        if 0 <= idx < len(todas):
            voz_escolhida = todas[idx]
            print(f"✅ Voz selecionada: {voz_escolhida.name}")
            return voz_escolhida.id

    print("❌ Escolha inválida. Usando voz padrão.")
    return None


# ---------------------------------------------------------------------------
# 5. Configurar velocidade
# ---------------------------------------------------------------------------
def configurar_velocidade(engine: pyttsx3.Engine) -> None:
    """Permite ajustar a velocidade de leitura."""
    print("\n" + "-" * 60)
    print("  ⚡  VELOCIDADE DE LEITURA  ")
    print("-" * 60)
    print("  [1] 0.75× – Lenta       (~112 wpm)")
    print("  [2] 1.0×  – Normal      (~150 wpm)  ← padrão")
    print("  [3] 1.25× – Rápida      (~187 wpm)")
    print("  [4] 1.5×  – Muito rápida (~225 wpm)")
    print("  [5] Personalizada")
    print("-" * 60)

    opcao = input("Escolha a velocidade [2]: ").strip() or "2"

    mapa = {"1": 112, "2": 150, "3": 187, "4": 225}
    if opcao in mapa:
        taxa = mapa[opcao]
    elif opcao == "5":
        try:
            taxa = int(input("  Digite a taxa em palavras por minuto (ex: 160): ").strip())
        except ValueError:
            taxa = 150
    else:
        taxa = 150

    engine.setProperty("rate", taxa)
    print(f"✅ Velocidade configurada: {taxa} wpm")


# ---------------------------------------------------------------------------
# 6. Pré-visualização do texto
# ---------------------------------------------------------------------------
def mostrar_preview(texto: str, n_chars: int = 400) -> None:
    preview = texto[:n_chars].replace("\n", " ")
    wrapped = textwrap.fill(preview, width=60)
    print("\n" + "-" * 60)
    print("  📝  PRÉ-VISUALIZAÇÃO DO TEXTO  ")
    print("-" * 60)
    print(wrapped)
    if len(texto) > n_chars:
        print(f"  ... [{len(texto) - n_chars} caracteres restantes]")
    print("-" * 60)


# ---------------------------------------------------------------------------
# 7. Leitura em voz alta
# ---------------------------------------------------------------------------
def ler_em_voz_alta(engine: pyttsx3.Engine, texto: str) -> None:
    print("\n🔊 Iniciando leitura… (feche a janela ou pressione Ctrl+C para parar)\n")
    try:
        engine.say(texto)
        engine.runAndWait()
        print("\n✅ Leitura concluída!")
    except KeyboardInterrupt:
        engine.stop()
        print("\n⏹️  Leitura interrompida pelo usuário.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    # 1. Selecionar arquivo
    caminho = selecionar_arquivo()
    print(f"\n📂 Arquivo: {caminho}")

    # 2. Extrair texto
    texto = extrair_texto(caminho)
    mostrar_preview(texto)

    # 3. Criar engine (velocidade padrão 1×)
    engine = criar_engine(taxa=150)

    # 4. Escolher voz
    voz_id = escolher_voz(engine)
    if voz_id:
        engine.setProperty("voice", voz_id)

    # 5. Configurar velocidade
    configurar_velocidade(engine)

    # 6. Confirmação
    print()
    confirmar = input("▶️  Iniciar leitura? [S/n]: ").strip().lower()
    if confirmar in ("n", "nao", "não"):
        print("Cancelado.")
        sys.exit(0)

    # 7. Ler
    ler_em_voz_alta(engine, texto)


if __name__ == "__main__":
    main()
