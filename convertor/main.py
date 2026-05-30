"""
main.py
Ponto de entrada do aplicativo IMG2PDF.

Uso:
    python main.py

Instalação das dependências:
    pip install customtkinter pillow img2pdf tkinterdnd2
"""

import sys
import os

# Garante que o diretório do projeto está no PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def check_dependencies():
    """Verifica se todas as dependências estão instaladas."""
    missing = []
    deps = {
        "customtkinter": "customtkinter",
        "PIL": "Pillow",
        "img2pdf": "img2pdf",
        "tkinterdnd2": "tkinterdnd2",
    }
    for module, package in deps.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(package)

    if missing:
        print("=" * 60)
        print("  ⚠  Dependências ausentes!")
        print("=" * 60)
        print("\nInstale com o comando:\n")
        print(f"  pip install {' '.join(missing)}\n")
        print("=" * 60)
        sys.exit(1)


def main():
    check_dependencies()

    # Importa tkinterdnd2 primeiro para habilitar drag and drop
    try:
        from tkinterdnd2 import TkinterDnD
        import customtkinter as ctk

        # Hack: integra TkinterDnD com CustomTkinter
        # Necessário pois CustomTkinter herda de tk.Tk, não de TkinterDnD.Tk
        original_tk = ctk.windows.ctk_tk.CTk.__bases__
        if TkinterDnD.Tk not in original_tk:
            ctk.windows.ctk_tk.CTk.__bases__ = (TkinterDnD.Tk,)
    except Exception as e:
        print(f"[AVISO] Drag and drop não disponível: {e}")

    from gui.main_window import MainWindow

    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
