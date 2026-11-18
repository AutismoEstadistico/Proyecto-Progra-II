from functools import partial
from itertools import cycle
import pandas as pd
from plotnine import aes, element_text, geom_bar, geom_boxplot, geom_line, geom_point, ggplot, labs, theme
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

# --- Agrupación de posiciones para el gráfico de Tab 2 ---
# Orden fijo pedido para el eje X (se excluye GK a propósito)
POS_ORDER_TAB2 = ["CB", "LB/RB", "CDM", "CM", "LM/RM", "CAM", "RW/LW", "ST"]

POSITION_GROUPS_TAB2 = {
    "CB": "CB",
    "LB": "LB/RB", "RB": "LB/RB",
    "CDM": "CDM",
    "CM": "CM",
    "LM": "LM/RM", "RM": "LM/RM",
    "CAM": "CAM",
    "LW": "RW/LW", "RW": "RW/LW",
    "ST": "ST",
    # GK no está en el diccionario -> queda como NaN y se filtra después
}
datos["PosGroupTab2"] = datos["Position"].map(POSITION_GROUPS_TAB2)

# Estadísticas disponibles para elegir en el sidebar (de Acceleration a Aggression)
STATS_COLS = [
    "Acceleration", "Sprint Speed", "Positioning", "Finishing", "Shot Power",
    "Long Shots", "Volleys", "Penalties", "Vision", "Crossing",
    "Free Kick Accuracy", "Short Passing", "Long Passing", "Curve",
    "Dribbling", "Agility", "Balance", "Reactions", "Ball Control",
    "Composure", "Interceptions", "Heading Accuracy", "Def Awareness",
    "Standing Tackle", "Sliding Tackle", "Jumping", "Stamina", "Strength",
    "Aggression",
]

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
  with ui.layout_sidebar():
    with ui.sidebar():
        ui.input_checkbox_group(
            "Stats",
            "Estadísticas",
            choices=STATS_COLS,
            selected=[STATS_COLS[0]],
        )

    @render.plot
    def grafico2():
      chosen = input.Stats()

      if not chosen:
        return ggplot() + labs(title="Selecciona al menos una estadística")

      # Excluye GK (PosGroupTab2 queda NaN para esos jugadores)
      df = datos[datos["PosGroupTab2"].notna()].copy()

      # Pasa de formato ancho a largo para poder graficar varias estadísticas a la vez
      df_largo = df.melt(
          id_vars=["PosGroupTab2"],
          value_vars=list(chosen),
          var_name="Estadistica",
          value_name="Valor",
      )

      resumen = (
          df_largo.groupby(["PosGroupTab2", "Estadistica"], observed=True)["Valor"]
          .mean()
          .reset_index()
      )

      # Fuerza el orden del eje X pedido
      resumen["PosGroupTab2"] = pd.Categorical(
          resumen["PosGroupTab2"], categories=POS_ORDER_TAB2, ordered=True
      )
      resumen = resumen.sort_values("PosGroupTab2")

      return (
          ggplot(
              resumen,
              aes(x="PosGroupTab2", y="Valor", color="Estadistica", group="Estadistica"),
          )
          + geom_line()
          + geom_point()
          + labs(x="Posición", y="Promedio")
          + theme_pitch()
      )

with ui.nav_panel("Tab 3"):
    "Contenido de la pestaña 3"