"""
core/converter.py
Motor de conversão de imagens para PDF.
Suporta conversão em PDF único ou PDFs separados, com controle de qualidade.
Toda conversão ocorre em thread separada para não travar a interface.
"""

import os
import threading
from pathlib import Path
from typing import List, Callable, Optional
from PIL import Image
import img2pdf

from core.logger import log


class ConversionConfig:
    """Configurações para uma conversão."""

    def __init__(
        self,
        image_paths: List[str],
        output_folder: str,
        pdf_name: str = "documento",
        quality: int = 85,
        compress: bool = True,
        separate_files: bool = False,
    ):
        self.image_paths = image_paths
        self.output_folder = Path(output_folder)
        self.pdf_name = pdf_name.strip() or "documento"
        self.quality = max(10, min(100, quality))
        self.compress = compress
        self.separate_files = separate_files


class ConversionResult:
    """Resultado de uma operação de conversão."""

    def __init__(self):
        self.success = False
        self.output_files: List[str] = []
        self.error_message: str = ""
        self.total_pages: int = 0


class PDFConverter:
    """
    Converte imagens para PDF usando img2pdf + Pillow.
    Notifica progresso via callbacks para atualização da interface.
    """

    def __init__(self):
        self._cancel_flag = threading.Event()

    def cancel(self):
        """Sinaliza cancelamento da conversão em andamento."""
        self._cancel_flag.set()
        log.info("Cancelamento de conversão solicitado.")

    def convert(
        self,
        config: ConversionConfig,
        on_progress: Optional[Callable[[int, int, str], None]] = None,
        on_complete: Optional[Callable[[ConversionResult], None]] = None,
    ):
        """
        Inicia conversão em thread separada.

        Args:
            config: Configurações da conversão
            on_progress: callback(atual, total, mensagem)
            on_complete: callback(resultado)
        """
        self._cancel_flag.clear()
        thread = threading.Thread(
            target=self._run,
            args=(config, on_progress, on_complete),
            daemon=True,
        )
        thread.start()

    def _run(
        self,
        config: ConversionConfig,
        on_progress: Optional[Callable],
        on_complete: Optional[Callable],
    ):
        """Execução real da conversão (em thread worker)."""
        result = ConversionResult()

        try:
            config.output_folder.mkdir(parents=True, exist_ok=True)
            paths = config.image_paths

            if not paths:
                result.error_message = "Nenhuma imagem para converter."
                self._finish(on_complete, result)
                return

            if config.separate_files:
                self._convert_separate(config, paths, result, on_progress)
            else:
                self._convert_single(config, paths, result, on_progress)

        except Exception as e:
            log.error(f"Erro inesperado na conversão: {e}")
            result.error_message = str(e)

        self._finish(on_complete, result)

    def _convert_single(self, config, paths, result, on_progress):
        """Converte todas as imagens em um único PDF."""
        total = len(paths)
        prepared = []

        for i, path in enumerate(paths):
            if self._cancel_flag.is_set():
                result.error_message = "Conversão cancelada pelo usuário."
                return

            msg = f"Preparando {Path(path).name} ({i + 1}/{total})…"
            self._emit_progress(on_progress, i, total, msg)
            log.debug(msg)

            try:
                prepared_path = self._prepare_image(path, config.quality, config.compress)
                prepared.append(prepared_path)
            except Exception as e:
                log.warning(f"Ignorando {path}: {e}")

        if not prepared:
            result.error_message = "Nenhuma imagem válida para converter."
            return

        output_path = config.output_folder / f"{config.pdf_name}.pdf"
        self._emit_progress(on_progress, total - 1, total, "Gerando PDF…")

        try:
            with open(output_path, "wb") as f:
                f.write(img2pdf.convert(prepared))
            result.output_files.append(str(output_path))
            result.total_pages = len(prepared)
            result.success = True
            self._emit_progress(on_progress, total, total, "Concluído!")
            log.info(f"PDF gerado: {output_path} ({len(prepared)} páginas)")
        except Exception as e:
            result.error_message = f"Erro ao salvar PDF: {e}"
            log.error(result.error_message)
        finally:
            # Limpa arquivos temporários
            for p in prepared:
                if "_tmp_" in str(p):
                    try:
                        os.remove(p)
                    except Exception:
                        pass

    def _convert_separate(self, config, paths, result, on_progress):
        """Converte cada imagem em um PDF separado."""
        total = len(paths)

        for i, path in enumerate(paths):
            if self._cancel_flag.is_set():
                result.error_message = "Conversão cancelada pelo usuário."
                return

            name = Path(path).stem
            msg = f"Convertendo {Path(path).name} ({i + 1}/{total})…"
            self._emit_progress(on_progress, i, total, msg)
            log.debug(msg)

            try:
                prepared_path = self._prepare_image(path, config.quality, config.compress)
                output_path = config.output_folder / f"{name}.pdf"

                with open(output_path, "wb") as f:
                    f.write(img2pdf.convert([prepared_path]))

                result.output_files.append(str(output_path))
                result.total_pages += 1

                if "_tmp_" in str(prepared_path):
                    try:
                        os.remove(prepared_path)
                    except Exception:
                        pass

            except Exception as e:
                log.warning(f"Erro ao converter {path}: {e}")

        if result.output_files:
            result.success = True
            self._emit_progress(on_progress, total, total, "Concluído!")
            log.info(f"{len(result.output_files)} PDFs gerados em {config.output_folder}")
        else:
            result.error_message = "Nenhum PDF foi gerado."

    def _prepare_image(self, path: str, quality: int, compress: bool) -> str:
        """
        Prepara imagem para conversão.
        Converte WEBP/RGBA para JPEG temporário se necessário.
        Retorna caminho do arquivo pronto para img2pdf.
        """
        p = Path(path)
        ext = p.suffix.lower()

        # img2pdf suporta diretamente PNG e JPEG
        # WEBP precisa ser convertido
        if ext in (".jpg", ".jpeg") and not compress:
            return path

        img = Image.open(path)

        # Converte modos incompatíveis com JPEG
        if img.mode in ("RGBA", "LA", "P"):
            background = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode == "P":
                img = img.convert("RGBA")
            background.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
            img = background
        elif img.mode != "RGB":
            img = img.convert("RGB")

        # Para PNG sem compressão, retorna direto se não precisar converter
        if ext == ".png" and not compress and img.mode == "RGB":
            return path

        # Salva como JPEG temporário com qualidade definida
        tmp_path = p.parent / f"_tmp_{p.stem}_q{quality}.jpg"
        img.save(str(tmp_path), "JPEG", quality=quality, optimize=True)
        return str(tmp_path)

    @staticmethod
    def _emit_progress(callback, current, total, message):
        """Emite progresso de forma segura."""
        if callback:
            try:
                callback(current, total, message)
            except Exception as e:
                log.error(f"Erro ao emitir progresso: {e}")

    @staticmethod
    def _finish(callback, result):
        """Chama callback de conclusão de forma segura."""
        if callback:
            try:
                callback(result)
            except Exception as e:
                log.error(f"Erro em callback de conclusão: {e}")
