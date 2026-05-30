"""
gui/image_card.py
Card visual representando uma imagem na lista.
Exibe miniatura, nome, tamanho e botões de ação (mover/remover).
"""

import customtkinter as ctk
from PIL import ImageTk, Image
from typing import Callable, Optional
from core.image_manager import ImageItem


class ImageCard(ctk.CTkFrame):
    """
    Cartão visual para uma imagem da lista.
    Exibe preview, metadados e controles de reordenação.
    """

    def __init__(
        self,
        parent,
        item: ImageItem,
        index: int,
        on_remove: Callable,
        on_move_up: Callable,
        on_move_down: Callable,
        can_move_up: bool = True,
        can_move_down: bool = True,
        **kwargs,
    ):
        super().__init__(parent, corner_radius=10, **kwargs)
        self.item = item
        self.index = index
        self._thumb_ref = None  # Evita garbage collection da imagem

        self._build(on_remove, on_move_up, on_move_down, can_move_up, can_move_down)

    def _build(self, on_remove, on_move_up, on_move_down, can_move_up, can_move_down):
        self.grid_columnconfigure(1, weight=1)

        # ── Número de ordem ───────────────────────────────────────
        ctk.CTkLabel(
            self,
            text=f"{self.index + 1:02d}",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            width=28,
        ).grid(row=0, column=0, rowspan=2, padx=(10, 6), pady=10)

        # ── Miniatura ─────────────────────────────────────────────
        thumb_label = ctk.CTkLabel(self, text="", width=72, height=72)
        thumb_label.grid(row=0, column=1, rowspan=2, padx=(0, 10), pady=8, sticky="w")
        self._load_thumbnail(thumb_label)

        # ── Info textual ──────────────────────────────────────────
        info_frame = ctk.CTkFrame(self, fg_color="transparent")
        info_frame.grid(row=0, column=2, sticky="sw", padx=0, pady=(10, 2))

        name = self.item.name
        if len(name) > 38:
            name = name[:35] + "…"

        ctk.CTkLabel(
            info_frame,
            text=name,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            anchor="w",
        ).pack(anchor="w")

        dims = self.item.dimensions
        meta = f"{dims[0]}×{dims[1]}px  ·  {self.item.size_display}"
        ctk.CTkLabel(
            info_frame,
            text=meta,
            font=ctk.CTkFont(family="Segoe UI", size=10),
            anchor="w",
        ).pack(anchor="w")

        # ── Botões de ação ────────────────────────────────────────
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=0, column=3, rowspan=2, padx=(0, 10), pady=8, sticky="e")

        btn_cfg = dict(width=30, height=28, corner_radius=6, border_width=0, font=ctk.CTkFont(size=12))

        ctk.CTkButton(
            btn_frame, text="↑",
            command=on_move_up,
            state="normal" if can_move_up else "disabled",
            **btn_cfg,
        ).pack(pady=2)

        ctk.CTkButton(
            btn_frame, text="↓",
            command=on_move_down,
            state="normal" if can_move_down else "disabled",
            **btn_cfg,
        ).pack(pady=2)

        ctk.CTkButton(
            btn_frame, text="✕",
            command=on_remove,
            fg_color="#3a1a1a",
            hover_color="#5a2020",
            **btn_cfg,
        ).pack(pady=2)

    def _load_thumbnail(self, label: ctk.CTkLabel):
        """Carrega a miniatura da imagem de forma assíncrona-segura."""
        try:
            thumb = self.item.get_thumbnail((72, 72))
            if thumb:
                # Cria imagem com fundo para preencher o quadrado
                bg = Image.new("RGB", (72, 72), (30, 33, 48))
                w, h = thumb.size
                offset = ((72 - w) // 2, (72 - h) // 2)
                if thumb.mode == "RGBA":
                    bg.paste(thumb, offset, thumb)
                else:
                    bg.paste(thumb, offset)
                ctk_img = ctk.CTkImage(light_image=bg, dark_image=bg, size=(72, 72))
                label.configure(image=ctk_img)
                self._thumb_ref = ctk_img  # Evita garbage collection
        except Exception:
            label.configure(text="🖼", font=ctk.CTkFont(size=24))
