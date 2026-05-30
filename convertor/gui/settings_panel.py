"""
gui/settings_panel.py
Painel de configurações de conversão (nome, qualidade, saída, modo).
"""

import os
from pathlib import Path
import customtkinter as ctk
from tkinter import filedialog
from core.settings import SettingsManager


class SettingsPanel(ctk.CTkFrame):
    """
    Painel lateral direito com configurações de conversão.
    Permite definir nome do PDF, qualidade, pasta de saída e modo.
    """

    def __init__(self, parent, settings: SettingsManager, **kwargs):
        super().__init__(parent, corner_radius=12, **kwargs)
        self.settings = settings
        self._build()

    def _build(self):
        self.grid_columnconfigure(0, weight=1)
        pad = {"padx": 16, "pady": 6}

        # ── Título ────────────────────────────────────────────────
        ctk.CTkLabel(
            self,
            text="⚙  Configurações",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            anchor="w",
        ).grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 12))

        ctk.CTkFrame(self, height=1, corner_radius=0).grid(
            row=1, column=0, sticky="ew", padx=16, pady=(0, 8)
        )

        # ── Nome do PDF ───────────────────────────────────────────
        ctk.CTkLabel(self, text="Nome do PDF", font=ctk.CTkFont(size=11), anchor="w").grid(
            row=2, column=0, sticky="ew", **pad
        )
        self.pdf_name_var = ctk.StringVar(value=self.settings.get("default_pdf_name", "documento"))
        self.entry_name = ctk.CTkEntry(
            self,
            textvariable=self.pdf_name_var,
            placeholder_text="ex: relatorio_final",
            height=36,
            corner_radius=8,
        )
        self.entry_name.grid(row=3, column=0, sticky="ew", padx=16, pady=(0, 8))

        # ── Pasta de saída ────────────────────────────────────────
        ctk.CTkLabel(self, text="Pasta de saída", font=ctk.CTkFont(size=11), anchor="w").grid(
            row=4, column=0, sticky="ew", **pad
        )

        out_frame = ctk.CTkFrame(self, fg_color="transparent")
        out_frame.grid(row=5, column=0, sticky="ew", padx=16, pady=(0, 8))
        out_frame.grid_columnconfigure(0, weight=1)

        self.output_folder_var = ctk.StringVar(value=self.settings.get("output_folder"))
        self.entry_output = ctk.CTkEntry(
            out_frame,
            textvariable=self.output_folder_var,
            height=36,
            corner_radius=8,
            state="readonly",
        )
        self.entry_output.grid(row=0, column=0, sticky="ew", padx=(0, 6))

        ctk.CTkButton(
            out_frame,
            text="…",
            width=36,
            height=36,
            corner_radius=8,
            command=self._browse_output,
        ).grid(row=0, column=1)

        # ── Qualidade ─────────────────────────────────────────────
        ctk.CTkLabel(self, text="Qualidade de imagem", font=ctk.CTkFont(size=11), anchor="w").grid(
            row=6, column=0, sticky="ew", **pad
        )

        quality_frame = ctk.CTkFrame(self, fg_color="transparent")
        quality_frame.grid(row=7, column=0, sticky="ew", padx=16, pady=(0, 8))
        quality_frame.grid_columnconfigure(0, weight=1)

        self.quality_var = ctk.IntVar(value=self.settings.get("pdf_quality", 85))
        self.quality_label = ctk.CTkLabel(
            quality_frame,
            text=f"{self.quality_var.get()}%",
            font=ctk.CTkFont(size=12, weight="bold"),
            width=40,
        )
        self.quality_label.grid(row=0, column=1, padx=(8, 0))

        self.quality_slider = ctk.CTkSlider(
            quality_frame,
            from_=10,
            to=100,
            variable=self.quality_var,
            command=self._on_quality_change,
            height=18,
        )
        self.quality_slider.grid(row=0, column=0, sticky="ew")

        # ── Compressão ────────────────────────────────────────────
        self.compress_var = ctk.BooleanVar(value=self.settings.get("compression", True))
        ctk.CTkCheckBox(
            self,
            text="Aplicar compressão",
            variable=self.compress_var,
            font=ctk.CTkFont(size=12),
            corner_radius=4,
            command=self._save,
        ).grid(row=8, column=0, sticky="w", padx=16, pady=(4, 8))

        # ── Modo de conversão ─────────────────────────────────────
        ctk.CTkLabel(self, text="Modo de conversão", font=ctk.CTkFont(size=11), anchor="w").grid(
            row=9, column=0, sticky="ew", **pad
        )

        self.separate_var = ctk.StringVar(value="single")
        ctk.CTkRadioButton(
            self, text="Um único PDF",
            variable=self.separate_var, value="single",
            font=ctk.CTkFont(size=12),
        ).grid(row=10, column=0, sticky="w", padx=24, pady=3)

        ctk.CTkRadioButton(
            self, text="PDFs separados",
            variable=self.separate_var, value="separate",
            font=ctk.CTkFont(size=12),
        ).grid(row=11, column=0, sticky="w", padx=24, pady=3)

        # ── Espaço flexível ───────────────────────────────────────
        self.grid_rowconfigure(12, weight=1)

        # ── Dica ──────────────────────────────────────────────────
        ctk.CTkLabel(
            self,
            text="💡  Arraste imagens para a área central",
            font=ctk.CTkFont(size=10),
            wraplength=180,
            justify="left",
        ).grid(row=13, column=0, sticky="ew", padx=16, pady=(4, 16))

    def _on_quality_change(self, value):
        self.quality_label.configure(text=f"{int(value)}%")
        self._save()

    def _browse_output(self):
        folder = filedialog.askdirectory(
            initialdir=self.output_folder_var.get(),
            title="Escolha a pasta de saída",
        )
        if folder:
            self.output_folder_var.set(folder)
            self._save()

    def _save(self):
        self.settings.set("default_pdf_name", self.pdf_name_var.get())
        self.settings.set("output_folder", self.output_folder_var.get())
        self.settings.set("pdf_quality", self.quality_var.get())
        self.settings.set("compression", self.compress_var.get())

    # ── API pública ───────────────────────────────────────────────

    def get_pdf_name(self) -> str:
        return self.pdf_name_var.get().strip() or "documento"

    def get_output_folder(self) -> str:
        return self.output_folder_var.get()

    def get_quality(self) -> int:
        return self.quality_var.get()

    def get_compression(self) -> bool:
        return self.compress_var.get()

    def is_separate(self) -> bool:
        return self.separate_var.get() == "separate"
