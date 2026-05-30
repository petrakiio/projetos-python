"""
gui/main_window.py
Janela principal do aplicativo IMG2PDF.
Integra todos os componentes da interface e coordena as ações do usuário.
"""

import os
import sys
import platform
import subprocess
import customtkinter as ctk
from tkinter import filedialog, messagebox

from core.image_manager import ImageManager, SUPPORTED_EXTENSIONS
from core.converter import PDFConverter, ConversionConfig
from core.settings import SettingsManager
from core.logger import log

from gui.sidebar import Sidebar
from gui.image_card import ImageCard
from gui.settings_panel import SettingsPanel
from gui.statusbar import StatusBar


class MainWindow(ctk.CTk):
    """
    Janela principal do aplicativo IMG2PDF.
    Orquestra todos os subsistemas: UI, imagens, conversão e configurações.
    """

    def __init__(self):
        super().__init__()

        self.settings = SettingsManager()
        self.image_manager = ImageManager()
        self.converter = PDFConverter()
        self._converting = False

        # Configura tema inicial
        self._apply_theme(self.settings.get("theme", "dark"))

        self._setup_window()
        self._build_layout()
        self._setup_dnd()
        self._setup_bindings()

        # Observa mudanças na lista de imagens
        self.image_manager.on_change(self._refresh_image_list)

        log.info("Aplicativo iniciado.")

    # ─── Configuração inicial ─────────────────────────────────────────────────

    def _apply_theme(self, theme: str):
        ctk.set_appearance_mode(theme)
        ctk.set_default_color_theme("blue")

    def _setup_window(self):
        self.title("IMG2PDF — Conversor de Imagens para PDF")
        self.minsize(900, 600)
        geo = self.settings.get("window_geometry", "1200x700")
        self.geometry(geo)
        self.resizable(True, True)

        # Ícone (ignora se não encontrar)
        icon_path = os.path.join(os.path.dirname(__file__), "..", "assets", "icon.ico")
        try:
            if os.path.exists(icon_path) and platform.system() == "Windows":
                self.iconbitmap(icon_path)
        except Exception:
            pass

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build_layout(self):
        """Monta o layout principal com sidebar, área central e painel direito."""
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ── Sidebar esquerda ──────────────────────────────────────
        self.sidebar = Sidebar(
            self,
            callbacks={
                "add_files": self._cmd_add_files,
                "add_folder": self._cmd_add_folder,
                "clear": self._cmd_clear,
                "convert": self._cmd_convert,
                "open_output": self._cmd_open_output,
                "toggle_theme": self._cmd_toggle_theme,
            },
            theme=self.settings.get("theme", "dark"),
        )
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")

        # ── Área central ──────────────────────────────────────────
        center = ctk.CTkFrame(self, fg_color="transparent")
        center.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        center.grid_columnconfigure(0, weight=1)
        center.grid_rowconfigure(1, weight=1)

        # Header da área central
        self._build_center_header(center)

        # Lista de imagens (scrollable)
        self._build_image_list(center)

        # ── Painel de configurações direito ───────────────────────
        self.settings_panel = SettingsPanel(
            self,
            settings=self.settings,
            width=230,
        )
        self.settings_panel.grid(row=0, column=2, rowspan=2, sticky="nsew", padx=(0, 12), pady=12)
        self.settings_panel.grid_propagate(False)

        # ── Barra de status ───────────────────────────────────────
        self.statusbar = StatusBar(self)
        self.statusbar.grid(row=1, column=1, sticky="ew", padx=0, pady=0)

    def _build_center_header(self, parent):
        """Cabeçalho da área central com stats e drop hint."""
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=16, pady=(12, 8))
        header.grid_columnconfigure(2, weight=1)

        # Contadores
        self.lbl_count = ctk.CTkLabel(
            header,
            text="0 imagens",
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
        )
        self.lbl_count.grid(row=0, column=0, sticky="w")

        sep = ctk.CTkLabel(header, text="·", font=ctk.CTkFont(size=18))
        sep.grid(row=0, column=1, padx=10)

        self.lbl_size = ctk.CTkLabel(
            header,
            text="0 KB",
            font=ctk.CTkFont(family="Segoe UI", size=14),
        )
        self.lbl_size.grid(row=0, column=2, sticky="w")

        # Botão de converter rápido (canto direito)
        self.btn_quick_convert = ctk.CTkButton(
            header,
            text="⚡  Converter para PDF",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            height=38,
            corner_radius=10,
            command=self._cmd_convert,
        )
        self.btn_quick_convert.grid(row=0, column=3, sticky="e", padx=(16, 0))

    def _build_image_list(self, parent):
        """Área scrollável com a lista de imagens."""
        # Container com borda para drop zone
        self.list_container = ctk.CTkFrame(parent, corner_radius=12)
        self.list_container.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 8))
        self.list_container.grid_columnconfigure(0, weight=1)
        self.list_container.grid_rowconfigure(0, weight=1)

        # Frame scrollável
        self.scroll_frame = ctk.CTkScrollableFrame(
            self.list_container,
            corner_radius=10,
            label_text="",
        )
        self.scroll_frame.grid(row=0, column=0, sticky="nsew", padx=4, pady=4)
        self.scroll_frame.grid_columnconfigure(0, weight=1)

        # Estado vazio
        self._build_empty_state()

    def _build_empty_state(self):
        """Exibe a tela de estado vazio com instruções."""
        self.empty_frame = ctk.CTkFrame(
            self.scroll_frame,
            fg_color="transparent",
        )
        self.empty_frame.grid(row=0, column=0, sticky="nsew", padx=40, pady=60)
        self.empty_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self.empty_frame,
            text="🖼️",
            font=ctk.CTkFont(size=52),
        ).grid(row=0, column=0, pady=(0, 12))

        ctk.CTkLabel(
            self.empty_frame,
            text="Arraste imagens aqui",
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
        ).grid(row=1, column=0, pady=(0, 8))

        ctk.CTkLabel(
            self.empty_frame,
            text="ou use os botões na barra lateral para\nadicionar arquivos e pastas",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            justify="center",
        ).grid(row=2, column=0, pady=(0, 24))

        ctk.CTkLabel(
            self.empty_frame,
            text="PNG  ·  JPG  ·  JPEG  ·  WEBP",
            font=ctk.CTkFont(family="Segoe UI", size=11),
        ).grid(row=3, column=0)

    # ─── Drag and Drop ────────────────────────────────────────────────────────

    def _setup_dnd(self):
        """Configura drag and drop na janela e na área de lista."""
        try:
            self.drop_target_register("DND_Files")
            self.dnd_bind("<<Drop>>", self._on_drop)
            self.list_container.drop_target_register("DND_Files")
            self.list_container.dnd_bind("<<Drop>>", self._on_drop)
            log.info("Drag and drop configurado com sucesso.")
        except Exception as e:
            log.warning(f"Drag and drop não disponível: {e}")

    def _on_drop(self, event):
        """Processa arquivos arrastados para a janela."""
        raw = event.data
        # tkinterdnd2 retorna paths entre {} no Windows e separados por espaço no Linux
        paths = self._parse_dnd_paths(raw)
        added = 0
        for path in paths:
            if os.path.isdir(path):
                added += self.image_manager.add_folder(path)
            else:
                if self.image_manager.add_file(path):
                    added += 1
        if added:
            self.statusbar.set_status(f"{added} imagem(ns) adicionada(s).", "success")
        else:
            self.statusbar.set_status("Nenhum arquivo suportado foi encontrado.", "error")

    @staticmethod
    def _parse_dnd_paths(raw: str) -> list:
        """Parseia string de caminhos do DND em lista de paths."""
        paths = []
        raw = raw.strip()
        if raw.startswith("{"):
            # Múltiplos arquivos entre chaves: {path1} {path2}
            import re
            paths = re.findall(r"\{([^}]+)\}", raw)
            remaining = re.sub(r"\{[^}]+\}", "", raw).strip()
            if remaining:
                paths += remaining.split()
        else:
            paths = raw.split()
        return [p.strip() for p in paths if p.strip()]

    # ─── Callbacks de interface ───────────────────────────────────────────────

    def _refresh_image_list(self):
        """Reconstrói a lista visual de imagens após qualquer mudança."""
        # Remove widgets existentes
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        images = self.image_manager.images
        total = len(images)

        # Atualiza contadores
        self.lbl_count.configure(text=f"{total} {'imagem' if total == 1 else 'imagens'}")
        self.lbl_size.configure(text=self.image_manager.total_size_display)

        if total == 0:
            self._build_empty_state()
            return

        # Cria um card para cada imagem
        for i, item in enumerate(images):
            card = ImageCard(
                self.scroll_frame,
                item=item,
                index=i,
                on_remove=lambda idx=i: self._cmd_remove(idx),
                on_move_up=lambda idx=i: self._cmd_move_up(idx),
                on_move_down=lambda idx=i: self._cmd_move_down(idx),
                can_move_up=(i > 0),
                can_move_down=(i < total - 1),
            )
            card.grid(row=i, column=0, sticky="ew", padx=4, pady=4)

    def _setup_bindings(self):
        """Configura atalhos de teclado."""
        self.bind("<Control-o>", lambda e: self._cmd_add_files())
        self.bind("<Control-Return>", lambda e: self._cmd_convert())
        self.bind("<Delete>", lambda e: None)  # Placeholder

    # ─── Comandos ─────────────────────────────────────────────────────────────

    def _cmd_add_files(self):
        """Abre diálogo para seleção de imagens."""
        initial = self.settings.get("last_input_folder")
        types = [
            ("Imagens suportadas", "*.png *.jpg *.jpeg *.webp"),
            ("PNG", "*.png"),
            ("JPEG", "*.jpg *.jpeg"),
            ("WebP", "*.webp"),
        ]
        files = filedialog.askopenfilenames(
            title="Selecione as imagens",
            initialdir=initial,
            filetypes=types,
        )
        if files:
            added = self.image_manager.add_files(list(files))
            folder = os.path.dirname(files[0])
            self.settings.set("last_input_folder", folder)
            self.statusbar.set_status(f"{added} imagem(ns) adicionada(s).", "success" if added else "idle")

    def _cmd_add_folder(self):
        """Abre diálogo para seleção de pasta."""
        initial = self.settings.get("last_input_folder")
        folder = filedialog.askdirectory(
            title="Selecione uma pasta com imagens",
            initialdir=initial,
        )
        if folder:
            added = self.image_manager.add_folder(folder)
            self.settings.set("last_input_folder", folder)
            msg = f"{added} imagem(ns) adicionada(s) de '{os.path.basename(folder)}'."
            self.statusbar.set_status(msg, "success" if added else "idle")

    def _cmd_clear(self):
        """Limpa a lista de imagens após confirmação."""
        if self.image_manager.count == 0:
            return
        if messagebox.askyesno(
            "Limpar lista",
            f"Remover todas as {self.image_manager.count} imagens da lista?",
        ):
            self.image_manager.clear()
            self.statusbar.reset()

    def _cmd_remove(self, index: int):
        self.image_manager.remove(index)

    def _cmd_move_up(self, index: int):
        self.image_manager.move_up(index)

    def _cmd_move_down(self, index: int):
        self.image_manager.move_down(index)

    def _cmd_convert(self):
        """Inicia o processo de conversão."""
        if self._converting:
            return

        if self.image_manager.count == 0:
            messagebox.showwarning("Sem imagens", "Adicione pelo menos uma imagem antes de converter.")
            return

        config = ConversionConfig(
            image_paths=self.image_manager.get_paths(),
            output_folder=self.settings_panel.get_output_folder(),
            pdf_name=self.settings_panel.get_pdf_name(),
            quality=self.settings_panel.get_quality(),
            compress=self.settings_panel.get_compression(),
            separate_files=self.settings_panel.is_separate(),
        )

        self._set_converting(True)
        self.statusbar.set_status("Iniciando conversão…", "working")
        self.statusbar.set_progress(0)

        self.converter.convert(
            config=config,
            on_progress=self._on_progress,
            on_complete=self._on_complete,
        )

    def _cmd_open_output(self):
        """Abre a pasta de saída no gerenciador de arquivos."""
        folder = self.settings_panel.get_output_folder()
        if not os.path.isdir(folder):
            messagebox.showwarning("Pasta não encontrada", f"A pasta '{folder}' não existe.")
            return
        try:
            if platform.system() == "Windows":
                os.startfile(folder)
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", folder])
            else:
                subprocess.Popen(["xdg-open", folder])
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir a pasta:\n{e}")

    def _cmd_toggle_theme(self):
        """Alterna entre tema claro e escuro."""
        current = self.settings.get("theme", "dark")
        new_theme = "light" if current == "dark" else "dark"
        self.settings.set("theme", new_theme)
        self._apply_theme(new_theme)
        log.info(f"Tema alterado para: {new_theme}")

    # ─── Callbacks de conversão ───────────────────────────────────────────────

    def _on_progress(self, current: int, total: int, message: str):
        """Atualiza a barra de progresso (chamado do thread worker)."""
        def update():
            progress = current / total if total > 0 else 0
            self.statusbar.set_progress(progress)
            self.statusbar.set_status(message, "working")
        self.after(0, update)

    def _on_complete(self, result):
        """Chamado quando a conversão termina (do thread worker)."""
        def update():
            self._set_converting(False)
            if result.success:
                files_str = ", ".join(os.path.basename(f) for f in result.output_files[:3])
                if len(result.output_files) > 3:
                    files_str += f" e mais {len(result.output_files) - 3}…"
                self.statusbar.set_status(
                    f"✓ {len(result.output_files)} PDF(s) gerado(s) com {result.total_pages} página(s).",
                    "success",
                )
                self.statusbar.set_progress(1.0)
                if result.output_files:
                    self.statusbar.set_file(os.path.basename(result.output_files[0]))
                messagebox.showinfo(
                    "Conversão concluída",
                    f"PDF(s) gerado(s) com sucesso!\n\n{files_str}\n\nPasta: {self.settings_panel.get_output_folder()}",
                )
            else:
                self.statusbar.set_status(f"✗ Erro: {result.error_message}", "error")
                self.statusbar.set_progress(0)
                messagebox.showerror("Erro na conversão", result.error_message)
        self.after(0, update)

    def _set_converting(self, converting: bool):
        """Atualiza estado de conversão na interface."""
        self._converting = converting
        self.sidebar.set_converting(converting)
        self.btn_quick_convert.configure(
            state="disabled" if converting else "normal",
            text="⏳  Convertendo…" if converting else "⚡  Converter para PDF",
        )

    # ─── Ciclo de vida ────────────────────────────────────────────────────────

    def _on_close(self):
        """Salva estado e fecha o aplicativo."""
        geo = self.geometry()
        self.settings.set("window_geometry", geo)
        self.settings_panel._save()
        log.info("Aplicativo encerrado.")
        self.destroy()
