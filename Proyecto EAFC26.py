from functools import partial
import pandas as pd
from plotnine import ggplot, aes, geom_bar
from shiny.express import input, render, ui
from shiny.ui import page_navbar
from theme import (
    FOOTBALL_CSS, FONT_LINK, POSITION_COLOURS, GOLD, PITCH_DARK,
    theme_pitch,
)



# Load your data
datos = pd.read_csv("EAFC26.csv")
datos = datos.drop(columns= ["url","card","ID"])

POSITION_GROUPS = {
    "GK": "GK",
    "CB": "DEF", "LB": "DEF", "RB": "DEF",
    "CDM": "MID", "CM": "MID", "CAM": "MID", "LM": "MID", "RM": "MID",
    "ST": "ATT", "LW": "ATT", "RW": "ATT",
}
datos["PosGroup"] = datos["Position"].map(POSITION_GROUPS)

ui.page_opts(
    title="EA FC 26",
    page_fn=partial(page_navbar, id="page"),
)

with ui.nav_panel("Tab 1"):
    @render.plot
    def grafico1():
        return (
            ggplot(datos.dropna(subset=["PosGroup"]), aes(x="PosGroup"))
            + geom_bar()
            + theme_pitch()
        )

with ui.nav_panel("Tab 2"):
    @render.plot
    def grafico2():
        return (
            ggplot(datos, aes(x="Position"))
            + geom_bar()
            + theme_pitch()
        )

with ui.nav_panel("Tab 3"):
    "Contenido de la pestaña 3"
