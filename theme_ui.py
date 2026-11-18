"""
Tema de la UI de Shiny (no del ggplot).
Reutiliza los colores de theme.py para mantener todo consistente.
"""
from shiny import ui

from theme import (
    PITCH_DARK, CARD_BG, SIDEBAR_BG, GRASS, GRASS_LIGHT, WHITE, GOLD,
)

# ---------------------------------------------------------------
# 1) DEFAULTS: variables de Bootstrap (cambian TODOS los componentes)
# ---------------------------------------------------------------
_DEFAULTS = f"""
// Paleta propia (prefijo fc- para no chocar con variables de Bootstrap)
$fc-pitch:       {PITCH_DARK}  !default;
$fc-card:        {CARD_BG}     !default;
$fc-sidebar:     {SIDEBAR_BG}  !default;
$fc-grass:       {GRASS}       !default;
$fc-grass-light: {GRASS_LIGHT} !default;
$fc-white:       {WHITE}       !default;
$fc-gold:        {GOLD}        !default;

// Variables de Bootstrap
$body-bg:               $fc-grass !default;
$body-color:            $fc-white !default;
$primary:               $fc-gold  !default;
$link-color:            $fc-gold  !default;
$headings-color:        $fc-white !default;
$font-family-base:      'Oswald', sans-serif !default;
$border-radius:         0.4rem    !default;

$card-bg:               $fc-card  !default;
$card-color:            $fc-white !default;
$card-border-color:     $fc-white !default;
$card-border-width:     2px       !default;
$card-border-radius:    12px      !default;
$card-cap-bg:           $fc-white !default;
$card-cap-color:        $fc-card  !default;

$input-bg:              $fc-white !default;
$input-color:           $fc-card  !default;

$nav-pills-link-active-bg:    $fc-gold !default;
$nav-pills-link-active-color: $fc-card !default;
"""

# ---------------------------------------------------------------
# 2) RULES: CSS extra que Bootstrap no resuelve solo con variables
# ---------------------------------------------------------------
_RULES = """
/* césped a rayas */
body {
    background: repeating-linear-gradient(
        90deg, $fc-grass 0, $fc-grass 80px,
        $fc-grass-light 80px, $fc-grass-light 160px);
    background-attachment: fixed;
}

/* barra de navegación */
.navbar {
    background: $fc-sidebar !important;
    border-bottom: 3px solid $fc-gold;
    text-transform: uppercase;
    letter-spacing: 3px;
}
.navbar .navbar-brand, .navbar .nav-link { color: $fc-white !important; }
.navbar .nav-link.active { color: $fc-gold !important; }

/* sidebar */
.bslib-sidebar-layout > .sidebar {
    background: $fc-sidebar !important;
    color: $fc-white;
    border-right: 3px solid $fc-white !important;
}
.sidebar-title { color: $fc-gold; text-transform: uppercase; letter-spacing: 2px; }
label, .control-label {
    text-transform: uppercase;
    letter-spacing: 1px;
    font-size: 0.85rem;
    color: $fc-white;
}
.selectize-input, .selectize-dropdown {
    background: $fc-white !important;
    color: $fc-card !important;
}
.form-check-input:checked {
    background-color: $fc-gold !important;
    border-color: $fc-gold !important;
}

/* sliders */
.irs--shiny .irs-bar { background: $fc-gold; border-color: $fc-gold; }
.irs--shiny .irs-handle { background: $fc-white; border: 2px solid $fc-gold; }
.irs--shiny .irs-from, .irs--shiny .irs-to, .irs--shiny .irs-single {
    background: $fc-gold; color: $fc-card; font-weight: 700;
}
.irs--shiny .irs-line { background: #1d4d27; border-color: #1d4d27; }
.irs--shiny .irs-min, .irs--shiny .irs-max { color: $fc-white; background: transparent; }

/* tarjetas */
.card-header {
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* marcador (value boxes) */
.bslib-value-box {
    background: #111 !important;
    color: $fc-gold !important;
    border: 3px solid $fc-white !important;
    border-radius: 10px !important;
    text-align: center;
}
.bslib-value-box .value-box-title {
    color: $fc-white;
    text-transform: uppercase;
    letter-spacing: 2px;
}
.bslib-value-box .value-box-value { font-size: 2.2rem; font-weight: 700; }

/* pestañas tipo pill */
.nav-pills .nav-link {
    color: $fc-white;
    text-transform: uppercase;
    letter-spacing: 1px;
    border: 2px solid $fc-white;
    margin-right: 6px;
    border-radius: 999px;
}
.nav-pills .nav-link.active { font-weight: 700; border-color: $fc-gold; }

/* tablas */
.shiny-data-grid table { color: $fc-white; }
.shiny-data-grid thead th { background: $fc-white !important; color: $fc-card !important; }
.shiny-data-grid tbody td { background: $fc-card !important; color: $fc-white !important; }
.shiny-data-grid tbody tr:nth-child(even) td { background: #0f3a1a !important; }
"""


def shiny_theme() -> ui.Theme:
    """Tema de Shiny: uso -> ui.page_opts(theme=shiny_theme())"""
    return ui.Theme().add_defaults(_DEFAULTS).add_rules(_RULES)