"""
core/image_manager.py
Gerenciamento da lista de imagens selecionadas.
Responsável por adicionar, remover, reordenar e validar imagens.
"""

import os
from pathlib import Path
from typing import List, Optional, Callable
from PIL import Image

from core.logger import log


# Extensões suportadas
SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}


class ImageItem:
    """
    Representa uma imagem na lista do aplicativo.
    Armazena metadados e a miniatura para preview.
    """

    def __init__(self, path: str):
        self.path = Path(path)
        self.name = self.path.name
        self.size_bytes = self.path.stat().st_size if self.path.exists() else 0
        self._dimensions: Optional[tuple] = None

    @property
    def dimensions(self) -> tuple:
        """Retorna as dimensões da imagem (largura, altura)."""
        if self._dimensions is None:
            try:
                with Image.open(self.path) as img:
                    self._dimensions = img.size
            except Exception:
                self._dimensions = (0, 0)
        return self._dimensions

    @property
    def size_kb(self) -> float:
        """Tamanho do arquivo em KB."""
        return self.size_bytes / 1024

    @property
    def size_display(self) -> str:
        """Tamanho formatado para exibição."""
        kb = self.size_kb
        if kb >= 1024:
            return f"{kb / 1024:.1f} MB"
        return f"{kb:.0f} KB"

    def get_thumbnail(self, size: tuple = (80, 80)) -> Optional[object]:
        """
        Gera miniatura da imagem para preview.
        Retorna objeto PIL Image ou None se falhar.
        """
        try:
            img = Image.open(self.path)
            img.thumbnail(size, Image.LANCZOS)
            return img
        except Exception as e:
            log.warning(f"Não foi possível gerar miniatura para {self.name}: {e}")
            return None

    def is_valid(self) -> bool:
        """Verifica se o arquivo é uma imagem válida e acessível."""
        try:
            with Image.open(self.path) as img:
                img.verify()
            return True
        except Exception:
            return False

    def __repr__(self):
        return f"ImageItem({self.name})"


class ImageManager:
    """
    Gerencia a coleção de imagens adicionadas pelo usuário.
    Suporta adição, remoção, reordenação e notificação de mudanças.
    """

    def __init__(self):
        self._images: List[ImageItem] = []
        self._on_change_callbacks: List[Callable] = []

    # ─── Callbacks ──────────────────────────────────────────────

    def on_change(self, callback: Callable):
        """Registra callback chamado ao alterar a lista."""
        self._on_change_callbacks.append(callback)

    def _notify(self):
        """Notifica todos os observadores sobre mudança na lista."""
        for cb in self._on_change_callbacks:
            try:
                cb()
            except Exception as e:
                log.error(f"Erro em callback de mudança: {e}")

    # ─── Consulta ───────────────────────────────────────────────

    @property
    def images(self) -> List[ImageItem]:
        return list(self._images)

    @property
    def count(self) -> int:
        return len(self._images)

    @property
    def total_size_bytes(self) -> int:
        return sum(img.size_bytes for img in self._images)

    @property
    def total_size_display(self) -> str:
        total = self.total_size_bytes
        if total >= 1024 ** 2:
            return f"{total / 1024 ** 2:.1f} MB"
        return f"{total / 1024:.0f} KB"

    def get_paths(self) -> List[str]:
        return [str(img.path) for img in self._images]

    # ─── Modificação ────────────────────────────────────────────

    def add_file(self, path: str) -> bool:
        """
        Adiciona uma imagem à lista.
        Retorna True se adicionada com sucesso.
        """
        p = Path(path)
        if not p.exists():
            log.warning(f"Arquivo não encontrado: {path}")
            return False
        if p.suffix.lower() not in SUPPORTED_EXTENSIONS:
            log.warning(f"Formato não suportado: {p.suffix}")
            return False
        # Evita duplicatas
        if any(img.path == p for img in self._images):
            log.info(f"Imagem já adicionada: {p.name}")
            return False
        item = ImageItem(str(p))
        self._images.append(item)
        log.info(f"Imagem adicionada: {p.name}")
        self._notify()
        return True

    def add_files(self, paths: List[str]) -> int:
        """Adiciona múltiplas imagens. Retorna quantidade adicionada."""
        count = sum(1 for p in paths if self.add_file(p))
        return count

    def add_folder(self, folder: str) -> int:
        """
        Adiciona todas as imagens suportadas de uma pasta.
        Retorna quantidade adicionada.
        """
        folder_path = Path(folder)
        if not folder_path.is_dir():
            log.warning(f"Pasta inválida: {folder}")
            return 0
        files = sorted([
            str(f) for f in folder_path.iterdir()
            if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS
        ])
        added = self.add_files(files)
        log.info(f"Pasta escaneada: {folder_path.name} — {added} imagens adicionadas")
        return added

    def remove(self, index: int):
        """Remove imagem pelo índice."""
        if 0 <= index < len(self._images):
            name = self._images[index].name
            self._images.pop(index)
            log.info(f"Imagem removida: {name}")
            self._notify()

    def move_up(self, index: int):
        """Move imagem uma posição acima."""
        if index > 0:
            self._images[index], self._images[index - 1] = (
                self._images[index - 1],
                self._images[index],
            )
            self._notify()

    def move_down(self, index: int):
        """Move imagem uma posição abaixo."""
        if index < len(self._images) - 1:
            self._images[index], self._images[index + 1] = (
                self._images[index + 1],
                self._images[index],
            )
            self._notify()

    def clear(self):
        """Remove todas as imagens da lista."""
        self._images.clear()
        log.info("Lista de imagens limpa.")
        self._notify()
