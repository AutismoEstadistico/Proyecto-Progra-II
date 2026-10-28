"""
Football theme for the whole app.
  - CSS            -> import FOOTBALL_CSS and the Google font link
  - ggplot (plotnine) theme -> theme_pitch(), plus colour scales
  - Colours        -> import any colour constant to stay consistent

Nothing in here touches data, so it can be reused as-is for every graph.
"""
from plotnine import (
    theme, theme_minimal, element_text, element_rect, element_line,
    element_blank, scale_fill_manual, scale_color_manual,
    scale_fill_gradient, scale_color_gradient,
)

# ---------------------------------------------------------------
# COLOURS
# ---------------------------------------------------------------
PITCH_DARK = "#0d3a18"    # plot panel background
CARD_BG = "#0a2d13"       # card + plot outer background (kept identical on purpose)
SIDEBAR_BG = "#071f0d"
GRASS = "#1b5e20"
GRASS_LIGHT = "#226b27"
GRID = "#2f6b3a"
WHITE = "#ffffff"
GOLD = "#ffd60a"
BLUE = "#4cc9f0"
RED = "#ff5d5d"
ORANGE = "#ff9f1c"

# Discrete palette: use for any categorical variable (positions, leagues, ...)
PALETTE = [GOLD, BLUE, RED, "#80ed99", ORANGE, "#c77dff", "#ffffff", "#f15bb5"]

# ---------------------------------------------------------------
# GGPLOT (plotnine) THEME
# Usage:  ggplot(df, aes(...)) + geom_...() + theme_pitch()
# ---------------------------------------------------------------
def theme_pitch(base_size: int = 12, figure_size=(8, 5)):
    return theme_minimal(base_size=base_size) + theme(
        figure_size=figure_size,
        text=element_text(color=WHITE),
        plot_background=element_rect(fill=CARD_BG, color=CARD_BG),
        panel_background=element_rect(fill=PITCH_DARK, color=PITCH_DARK),
        panel_grid_major=element_line(color=GRID, size=0.6),
        panel_grid_minor=element_blank(),
        axis_text=element_text(color=WHITE),
        axis_title=element_text(color=GOLD, weight="bold"),
        axis_ticks=element_line(color=WHITE),
        plot_title=element_text(
            color=WHITE, size=base_size * 1.5, weight="bold", ha="left"
        ),
        plot_subtitle=element_text(color=GOLD, ha="left"),
        plot_caption=element_text(color="#9bbf9f"),
        legend_background=element_rect(fill=CARD_BG, color=CARD_BG),
        legend_key=element_blank(),
        legend_text=element_text(color=WHITE),
        legend_title=element_text(color=GOLD, weight="bold"),
        strip_background=element_rect(fill=WHITE, color=WHITE),
        strip_text=element_text(color=CARD_BG, weight="bold"),
    )


# Colour scales that match the theme
def scale_fill_pitch():
    return scale_fill_manual(values=PALETTE)


def scale_color_pitch():
    return scale_color_manual(values=PALETTE)


def scale_fill_pitch_c():
    """Continuous fill: dark green -> gold."""
    return scale_fill_gradient(low="#2e7d32", high=GOLD)


def scale_color_pitch_c():
    return scale_color_gradient(low="#2e7d32", high=GOLD)


# ---------------------------------------------------------------
# UI CSS
# ---------------------------------------------------------------
FONT_LINK = (
    "https://fonts.googleapis.com/css2?"
    "family=Oswald:wght@400;600;700&display=swap"
)

_CSS = """
/* ---------- page: mowed-grass stripes ---------- */
body {
    font-family: 'Oswald', sans-serif;
    color: WHITE;
    background: repeating-linear-gradient(
        90deg, GRASS 0, GRASS 80px, GRASS_LIGHT 80px, GRASS_LIGHT 160px);
    background-attachment: fixed;
}
.bslib-page-title, .navbar {
    background: SIDEBAR_BG !important;
    color: WHITE !important;
    text-transform: uppercase;
    letter-spacing: 3px;
    border-bottom: 3px solid GOLD;
}

/* ---------- sidebar ---------- */
.bslib-sidebar-layout > .sidebar {
    background: SIDEBAR_BG !important;
    color: WHITE;
    border-right: 3px solid WHITE !important;
}
.sidebar-title { color: GOLD; text-transform: uppercase; letter-spacing: 2px; }
label, .control-label {
    text-transform: uppercase;
    letter-spacing: 1px;
    font-size: 0.85rem;
    color: WHITE;
}
.form-control, .form-select, .selectize-input, .selectize-dropdown {
    background: WHITE !important;
    color: CARD_BG !important;
    border-radius: 6px !important;
    font-family: 'Oswald', sans-serif;
}
.form-check-input:checked {
    background-color: GOLD !important;
    border-color: GOLD !important;
}

/* sliders */
.irs--shiny .irs-bar { background: GOLD; border-color: GOLD; }
.irs--shiny .irs-handle { background: WHITE; border: 2px solid GOLD; }
.irs--shiny .irs-from, .irs--shiny .irs-to, .irs--shiny .irs-single {
    background: GOLD; color: CARD_BG; font-weight: 700;
}
.irs--shiny .irs-line { background: #1d4d27; border-color: #1d4d27; }
.irs--shiny .irs-min, .irs--shiny .irs-max { color: WHITE; background: transparent; }

/* ---------- cards ---------- */
.card {
    background: CARD_BG !important;
    border: 2px solid WHITE !important;
    border-radius: 12px !important;
    color: WHITE;
}
.card-header {
    background: WHITE !important;
    color: CARD_BG !important;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* ---------- scoreboard value boxes ---------- */
.bslib-value-box {
    background: #111 !important;
    color: GOLD !important;
    border: 3px solid WHITE !important;
    border-radius: 10px !important;
    text-align: center;
}
.bslib-value-box .value-box-title {
    color: WHITE;
    text-transform: uppercase;
    letter-spacing: 2px;
}
.bslib-value-box .value-box-value { font-size: 2.2rem; font-weight: 700; }

/* ---------- tabs (pills) ---------- */
.nav-pills .nav-link {
    color: WHITE;
    text-transform: uppercase;
    letter-spacing: 1px;
    border: 2px solid WHITE;
    margin-right: 6px;
    border-radius: 999px;
}
.nav-pills .nav-link.active {
    background: GOLD !important;
    color: CARD_BG !important;
    border-color: GOLD;
    font-weight: 700;
}

/* ---------- data table ---------- */
.shiny-data-grid table { color: WHITE; }
.shiny-data-grid thead th { background: WHITE !important; color: CARD_BG !important; }
.shiny-data-grid tbody td { background: CARD_BG !important; color: WHITE !important; }
.shiny-data-grid tbody tr:nth-child(even) td { background: #0f3a1a !important; }
"""

_TOKENS = {
    "SIDEBAR_BG": SIDEBAR_BG,
    "CARD_BG": CARD_BG,
    "GRASS_LIGHT": GRASS_LIGHT,
    "GRASS": GRASS,
    "WHITE": WHITE,
    "GOLD": GOLD,
}
FOOTBALL_CSS = _CSS
for _name, _value in _TOKENS.items():
    FOOTBALL_CSS = FOOTBALL_CSS.replace(_name, _value)
