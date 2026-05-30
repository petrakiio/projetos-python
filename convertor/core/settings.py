"""
core/settings.py
Gerenciamento de configurações e preferências do usuário.
Salva e carrega preferências em arquivo JSON local.
"""

import json
import os
from pathlib import Path


# Caminho do arquivo de configurações
SETTINGS_FILE = Path(__file__).parent.parent / "assets" / "settings.json"

# Configurações padrão
DEFAULT_SETTINGS = {
    "theme": "dark",
    "output_folder": str(Path.home() / "Documents"),
    "pdf_quality": 85,
    "compression": True,
    "default_pdf_name": "documento",
    "last_input_folder": str(Path.home()),
    "window_geometry": "1200x700",
    "window_maximized": False,
}


class SettingsManager:
    """
    Gerenciador de configurações do aplicativo.
    Persiste preferências do usuário entre sessões.
    """

    def __init__(self):
        self._settings = DEFAULT_SETTINGS.copy()
        self._ensure_assets_dir()
        self.load()

    def _ensure_assets_dir(self):
        """Garante que o diretório de assets existe."""
        SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)

    def load(self):
        """Carrega configurações do arquivo JSON."""
        try:
            if SETTINGS_FILE.exists():
                with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                    saved = json.load(f)
                    # Mescla com defaults para garantir chaves novas
                    self._settings.update(saved)
        except (json.JSONDecodeError, IOError) as e:
            print(f"[Settings] Erro ao carregar configurações: {e}. Usando padrões.")
            self._settings = DEFAULT_SETTINGS.copy()

    def save(self):
        """Salva configurações atuais no arquivo JSON."""
        try:
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(self._settings, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"[Settings] Erro ao salvar configurações: {e}")

    def get(self, key: str, fallback=None):
        """Retorna valor de uma configuração pelo nome."""
        return self._settings.get(key, fallback if fallback is not None else DEFAULT_SETTINGS.get(key))

    def set(self, key: str, value):
        """Define valor de uma configuração e salva."""
        self._settings[key] = value
        self.save()

    def reset(self):
        """Restaura todas as configurações para os valores padrão."""
        self._settings = DEFAULT_SETTINGS.copy()
        self.save()
