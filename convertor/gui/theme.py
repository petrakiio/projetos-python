"""
gui/theme.py
Definições de tema visual do aplicativo.
Paleta de cores, fontes e estilos para dark/light mode.
"""

# ─── Paleta Dark (padrão) ─────────────────────────────────────────────────────

DARK = {
    # Fundos
    "bg_root": "#0d0f14",
    "bg_sidebar": "#13151c",
    "bg_card": "#1a1d27",
    "bg_card_hover": "#1f2235",
    "bg_input": "#0f1118",
    "bg_progress_track": "#1a1d27",

    # Texto
    "text_primary": "#e8eaf0",
    "text_secondary": "#8b90a8",
    "text_muted": "#565a74",
    "text_accent": "#ffffff",

    # Acento principal — violeta elétrico
    "accent": "#7c6af7",
    "accent_hover": "#9484ff",
    "accent_dim": "#2d2860",

    # Status
    "success": "#3fcf8e",
    "warning": "#f5a623",
    "error": "#f0584a",
    "info": "#4dabf7",

    # Bordas
    "border": "#252838",
    "border_focus": "#7c6af7",

    # Scrollbar
    "scroll_bg": "#13151c",
    "scroll_thumb": "#2d3050",

    # Botões sidebar
    "btn_sidebar_bg": "#1a1d27",
    "btn_sidebar_hover": "#252838",
    "btn_sidebar_active": "#2d2860",

    # Separador
    "divider": "#1e2132",
}

# ─── Paleta Light ─────────────────────────────────────────────────────────────

LIGHT = {
    "bg_root": "#f0f2f8",
    "bg_sidebar": "#e4e7f0",
    "bg_card": "#ffffff",
    "bg_card_hover": "#f5f7ff",
    "bg_input": "#eef0f8",
    "bg_progress_track": "#e0e3ef",

    "text_primary": "#1a1d2e",
    "text_secondary": "#5a607a",
    "text_muted": "#9499b4",
    "text_accent": "#ffffff",

    "accent": "#6558f5",
    "accent_hover": "#7c6af7",
    "accent_dim": "#e8e5ff",

    "success": "#2db37a",
    "warning": "#e8930a",
    "error": "#d94034",
    "info": "#1c8ef0",

    "border": "#d8dce8",
    "border_focus": "#6558f5",

    "scroll_bg": "#e4e7f0",
    "scroll_thumb": "#c0c5d8",

    "btn_sidebar_bg": "#e8ebf5",
    "btn_sidebar_hover": "#dde0ee",
    "btn_sidebar_active": "#c9c3ff",

    "divider": "#dce0ee",
}


def get_palette(theme: str = "dark") -> dict:
    """Retorna a paleta de cores para o tema especificado."""
    return DARK if theme == "dark" else LIGHT


# ─── Fontes ───────────────────────────────────────────────────────────────────

FONTS = {
    "title": ("Segoe UI", 20, "bold"),
    "subtitle": ("Segoe UI", 13, "bold"),
    "body": ("Segoe UI", 12),
    "body_bold": ("Segoe UI", 12, "bold"),
    "small": ("Segoe UI", 10),
    "small_bold": ("Segoe UI", 10, "bold"),
    "mono": ("Consolas", 10),
    "logo": ("Segoe UI", 16, "bold"),
    "counter": ("Segoe UI", 28, "bold"),
}

# ─── Dimensões ────────────────────────────────────────────────────────────────

SIDEBAR_WIDTH = 220
THUMB_SIZE = (72, 72)
CARD_RADIUS = 10
BTN_RADIUS = 8
PADDING = 16
