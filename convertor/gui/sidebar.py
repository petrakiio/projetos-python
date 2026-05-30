"""
gui/sidebar.py
Componente da barra lateral com botões de ação principais.
"""

import customtkinter as ctk
from gui.theme import FONTS, PADDING


class SidebarButton(ctk.CTkButton):
    """Botão estilizado para a sidebar com ícone e texto."""

    def __init__(self, parent, icon: str, text: str, command=None, **kwargs):
        super().__init__(
            parent,
            text=f"  {icon}  {text}",
            command=command,
            anchor="w",
            height=44,
            corner_radius=8,
            border_width=0,
            font=ctk.CTkFont(family="Segoe UI", size=13),
            **kwargs,
        )


class Sidebar(ctk.CTkFrame):
    """
    Painel lateral esquerdo com logo, botões de ação e controles de tema.
    """

    def __init__(self, parent, callbacks: dict, theme: str = "dark", **kwargs):
        super().__init__(
            parent,
            width=220,
            corner_radius=0,
            **kwargs,
        )
        self.callbacks = callbacks
        self.theme = theme
        self.grid_propagate(False)
        self._build()

    def _build(self):
        self.grid_columnconfigure(0, weight=1)

        # ── Logo ──────────────────────────────────────────────────
        logo_frame = ctk.CTkFrame(self, fg_color="transparent")
        logo_frame.grid(row=0, column=0, sticky="ew", padx=16, pady=(24, 8))

        ctk.CTkLabel(
            logo_frame,
            text="⬛",
            font=ctk.CTkFont(size=28),
        ).pack(side="left", padx=(0, 10))

        title_frame = ctk.CTkFrame(logo_frame, fg_color="transparent")
        title_frame.pack(side="left")

        ctk.CTkLabel(
            title_frame,
            text="IMG2PDF",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_frame,
            text="Conversor profissional",
            font=ctk.CTkFont(family="Segoe UI", size=10),
        ).pack(anchor="w")

        # ── Separador ─────────────────────────────────────────────
        ctk.CTkFrame(self, height=1, corner_radius=0).grid(
            row=1, column=0, sticky="ew", padx=16, pady=(8, 16)
        )

        # ── Seção: Arquivos ───────────────────────────────────────
        self._section_label(2, "ARQUIVOS")

        self.btn_add = SidebarButton(
            self, "🖼", "Adicionar imagens",
            command=self.callbacks.get("add_files"),
        )
        self.btn_add.grid(row=3, column=0, sticky="ew", padx=12, pady=3)

        self.btn_folder = SidebarButton(
            self, "📁", "Adicionar pasta",
            command=self.callbacks.get("add_folder"),
        )
        self.btn_folder.grid(row=4, column=0, sticky="ew", padx=12, pady=3)

        self.btn_clear = SidebarButton(
            self, "🗑", "Limpar lista",
            command=self.callbacks.get("clear"),
        )
        self.btn_clear.grid(row=5, column=0, sticky="ew", padx=12, pady=3)

        # ── Separador ─────────────────────────────────────────────
        ctk.CTkFrame(self, height=1, corner_radius=0).grid(
            row=6, column=0, sticky="ew", padx=16, pady=(12, 8)
        )

        # ── Seção: Conversão ──────────────────────────────────────
        self._section_label(7, "CONVERSÃO")

        self.btn_convert = SidebarButton(
            self, "⚡", "Converter",
            command=self.callbacks.get("convert"),
        )
        self.btn_convert.grid(row=8, column=0, sticky="ew", padx=12, pady=3)

        self.btn_output = SidebarButton(
            self, "📂", "Pasta de saída",
            command=self.callbacks.get("open_output"),
        )
        self.btn_output.grid(row=9, column=0, sticky="ew", padx=12, pady=3)

        # ── Espaço flexível ───────────────────────────────────────
        self.grid_rowconfigure(10, weight=1)

        # ── Separador ─────────────────────────────────────────────
        ctk.CTkFrame(self, height=1, corner_radius=0).grid(
            row=11, column=0, sticky="ew", padx=16, pady=(8, 8)
        )

        # ── Rodapé: tema ──────────────────────────────────────────
        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.grid(row=12, column=0, sticky="ew", padx=12, pady=(4, 16))
        footer.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            footer,
            text="Tema",
            font=ctk.CTkFont(family="Segoe UI", size=11),
        ).grid(row=0, column=0, sticky="w", padx=4)

        self.theme_switch = ctk.CTkSwitch(
            footer,
            text="Modo escuro",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            command=self.callbacks.get("toggle_theme"),
            onvalue="dark",
            offvalue="light",
        )
        self.theme_switch.grid(row=1, column=0, sticky="w", padx=4, pady=4)

        if self.theme == "dark":
            self.theme_switch.select()
        else:
            self.theme_switch.deselect()

    def _section_label(self, row: int, text: str):
        ctk.CTkLabel(
            self,
            text=text,
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            anchor="w",
        ).grid(row=row, column=0, sticky="ew", padx=20, pady=(4, 2))

    def set_converting(self, converting: bool):
        """Habilita/desabilita botões durante a conversão."""
        state = "disabled" if converting else "normal"
        for btn in [self.btn_add, self.btn_folder, self.btn_clear, self.btn_convert]:
            btn.configure(state=state)
