"""
core/logger.py
Sistema de log do aplicativo.
Grava logs em arquivo e permite consulta pelo histórico de ações.
"""

import logging
import os
from datetime import datetime
from pathlib import Path


LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_FILE = LOG_DIR / f"app_{datetime.now().strftime('%Y%m%d')}.log"


def setup_logger(name: str = "img2pdf") -> logging.Logger:
    """
    Configura e retorna o logger principal do aplicativo.
    Grava em arquivo e exibe no console.
    """
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Evita duplicação de handlers em reimportações
    if logger.handlers:
        return logger

    # Handler para arquivo
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_fmt = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S"
    )
    file_handler.setFormatter(file_fmt)

    # Handler para console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_fmt = logging.Formatter("[%(levelname)s] %(message)s")
    console_handler.setFormatter(console_fmt)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# Logger global acessível por outros módulos
log = setup_logger()
