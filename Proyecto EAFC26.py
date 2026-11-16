from functools import partial
from itertools import cycle
import pandas as pd
from plotnine import aes, element_text, geom_bar, geom_boxplot, ggplot, labs, theme
from shiny.express import input, render, ui
from shiny.ui import page_navbar
from theme import (
    FOOTBALL_CSS,
    FONT_LINK,
    GOLD,
    PALETTE,  # Make sure PALETTE exists in theme.py
    PITCH_DARK,
    POSITION_COLOURS,
    WHITE,
    scale_fill_pitch,
    theme_pitch,
)
from theme_ui import shiny_theme



# Load your data
datos = pd.read_csv("EAFC26.csv")
datos = datos.drop(columns= ["url","card","ID"])
mis_5_ligas = [
    "LALIGA EA SPORTS",
    "Premier League",
    "Serie A Enilive",
    "Bundesliga",
    "Ligue 1 McDonald's",
    "MLS",
    "Liga Portugal",
    "Trendyol Süper Lig",
    "Eredivisie",
    "LPF",
    "ROSHN Saudi League"
]

# Default selection: the 5 leagues with the most players
top_ligas = datos["League"].value_counts().head(5).index.tolist()
POSITION_GROUPS = {
    "GK": "GK",
    "CB": "DEF", "LB": "DEF", "RB": "DEF",
    "CDM": "MID", "CM": "MID", "CAM": "MID", "LM": "MID", "RM": "MID",
    "ST": "ATT", "LW": "ATT", "RW": "ATT",
}
datos["PosGroup"] = datos["Position"].map(POSITION_GROUPS)
colores = dict(zip(mis_5_ligas, cycle(PALETTE)))

ui.page_opts(
    title="EA FC 26",
    page_fn=partial(page_navbar, id="nav"),
    fillable=True,
    theme=shiny_theme(),
)

with ui.nav_panel("Tab 1"):
  with ui.layout_sidebar():
    with ui.sidebar():
        ui.input_checkbox_group(
            "Ligas",
            "Ligas",
            choices=mis_5_ligas,
            selected=["LALIGA EA SPORTS"],
        )

    @render.plot
    def grafico1():
      chosen = input.Ligas()
      filtered_df = datos[datos["League"].isin(chosen)]

      if filtered_df.empty:
        return ggplot() + labs(title="Please select at least one league")

      return (
          ggplot(filtered_df, aes(x="League", y="OVR", fill="League"))
          + geom_boxplot()
          + theme_pitch()
      )
with ui.nav_panel("Tab 2"):
    "Contenido de la 2"

with ui.nav_panel("Tab 3"):
    "Contenido de la pestaña 3"
