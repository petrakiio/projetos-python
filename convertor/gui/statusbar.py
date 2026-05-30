"""
gui/statusbar.py
Barra de status inferior com progresso, mensagens e indicador de estado.
"""

import customtkinter as ctk


class StatusBar(ctk.CTkFrame):
    """
    Barra de status na parte inferior da janela.
    Exibe mensagem atual, barra de progresso e nome do último arquivo gerado.
    """

    def __init__(self, parent, **kwargs):
        super().__init__(parent, corner_radius=0, height=56, **kwargs)
        self.grid_propagate(False)
        self._build()

    def _build(self):
        self.grid_columnconfigure(1, weight=1)

        # ── Indicador de estado (bolinha colorida) ────────────────
        self.indicator = ctk.CTkLabel(
            self,
            text="●",
            font=ctk.CTkFont(size=14),
            width=24,
        )
        self.indicator.grid(row=0, column=0, padx=(16, 8), pady=8, rowspan=2)

        # ── Mensagem de status ────────────────────────────────────
        self.status_label = ctk.CTkLabel(
            self,
            text="Pronto. Adicione imagens para começar.",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            anchor="w",
        )
        self.status_label.grid(row=0, column=1, sticky="ew", padx=(0, 16), pady=(8, 0))

        # ── Barra de progresso ────────────────────────────────────
        self.progress = ctk.CTkProgressBar(
            self,
            height=4,
            corner_radius=2,
            mode="determinate",
        )
        self.progress.set(0)
        self.progress.grid(row=1, column=1, sticky="ew", padx=(0, 16), pady=(2, 8))

        # ── Nome do arquivo gerado ─────────────────────────────────
        self.file_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            width=220,
            anchor="e",
        )
        self.file_label.grid(row=0, column=2, rowspan=2, padx=(0, 16), pady=8)

    def set_status(self, message: str, state: str = "idle"):
        """
        Atualiza mensagem e cor do indicador.
        state: 'idle' | 'working' | 'success' | 'error'
        """
        self.status_label.configure(text=message)

        colors = {
            "idle": "#565a74",
            "working": "#f5a623",
            "success": "#3fcf8e",
            "error": "#f0584a",
        }
        self.indicator.configure(text_color=colors.get(state, "#565a74"))

    def set_progress(self, value: float):
        """
        Define o progresso da barra.
        value: 0.0 a 1.0
        """
        self.progress.set(max(0.0, min(1.0, value)))

    def set_file(self, filename: str):
        """Exibe o nome do arquivo gerado no canto direito."""
        if filename:
            name = filename if len(filename) <= 30 else "…" + filename[-27:]
            self.file_label.configure(text=f"📄 {name}")
        else:
            self.file_label.configure(text="")

    def reset(self):
        """Restaura o status para o estado inicial."""
        self.set_status("Pronto. Adicione imagens para começar.", "idle")
        self.set_progress(0)
        self.set_file("")

    def set_indeterminate(self, active: bool):
        """Alterna modo indeterminado (animação de carregamento)."""
        if active:
            self.progress.configure(mode="indeterminate")
            self.progress.start()
        else:
            self.progress.stop()
            self.progress.configure(mode="determinate")
            self.progress.set(0)
