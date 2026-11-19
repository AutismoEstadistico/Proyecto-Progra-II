from functools import partial
from itertools import cycle
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
from plotnine import aes, element_text, geom_bar, geom_boxplot, ggplot, labs, theme
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
datos["GrupoEdad"] = pd.cut(
    datos["Age"],
    bins=[0, 23, 29, 100],
    labels=["23 años o menos", "de 24 a 29 años", "30 años o más"],)
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

with ui.nav_panel("Hola :D"):
    with ui.layout_columns(col_widths=(6, 6, 12)):
        with ui.card():
            ui.p("Este es nuestro proyecto de programacion II, una app usando datos de EAFC26! ")

        with ui.card():
            ui.p("A continuacion veran una serie de graficos hechos con las librerias plotnine y seaborne. Para ver cada grafico, vayan a la tab correspondiente de cada uno")
        with ui.card(style="width: fit-content; margin: 0 auto; text-align: center;"):
            ui.p("Aupa Athletic")
            ui.img(src = "AthleticCopaCampeones.jpg",style="max-height: 400px; width: auto; display: block; margin: 0 auto;")

with ui.nav_panel("OVR Ligas"):
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
  with ui.layout_sidebar():
    with ui.sidebar():
      ui.input_checkbox_group(
          "GruposEdad",
          "Grupo de Edad",
          choices=["23 años o menos", "de 24 a 29 años", "30 años o más"],
          selected=["23 años o menos"],
      )

    @render.plot
    def grafico3():
      seleccion = input.GruposEdad()
      stats = ["PAC", "SHO", "PAS", "DRI", "DEF", "PHY"]
      angulos = np.linspace(0, 2 * np.pi, len(stats), endpoint=False).tolist()
      angulos += angulos[:1]

      fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
      fig.subplots_adjust(left=0.0, right=0.40, top=0.82, bottom=0.12)
      fig.patch.set_facecolor("#0a2912")
      ax.set_facecolor("none")

      fondo_cuadro = Rectangle(
          (-0.45, -0.18),
          1.90,
          1.40,
          transform=ax.transAxes,
          facecolor=PITCH_DARK,
          edgecolor="none",
          linewidth=1.2,
          clip_on=False,
          zorder=0,
      )
      ax.add_patch(fondo_cuadro)
      x_izq, y_inf = fondo_cuadro.get_xy()
      x_der = x_izq + fondo_cuadro.get_width()
      y_sup = y_inf + fondo_cuadro.get_height()

      ax.plot(
          [x_izq, x_der],
          [0.5, 0.5],
          transform=ax.transAxes,
          color=WHITE,
          linewidth=0.6,
          alpha=0.25,
          clip_on=False,
          zorder=1,
      )

      ax.plot(
          [0.5, 0.5],
          [y_inf, y_sup],
          transform=ax.transAxes,
          color=WHITE,
          linewidth=0.6,
          alpha=0.25,
          clip_on=False,
          zorder=1,
      )
      ax.set_theta_offset(np.pi / 2)
      ax.set_theta_direction(-1)

      ax.set_xticks(angulos[:-1])
      ax.set_xticklabels(stats, color=GOLD, fontsize=12, fontweight="bold")
      ax.set_ylim(0, 100)
      ax.set_yticks([20, 40, 60, 80])
      ax.set_yticklabels(["20", "40", "60", "80"], color=WHITE, fontsize=8)
      ax.grid(color=WHITE, alpha=0.25)
      ax.spines["polar"].set_color(WHITE)
      ax.spines["polar"].set_alpha(0.3)

      if not seleccion:
        ax.set_title("Selecciona al menos un grupo de edad", color=WHITE, pad=25)
        ax.plot([], [], color="none", label="23 años o menos (n=0000)")
        leyenda_vacia = ax.legend(
            loc="center left",
            bbox_to_anchor=(1.52, 0.5),
            frameon=False,
            title="Rango de Edad",
            alignment="left",
        )
        leyenda_vacia.get_title().set_alpha(0)
        for texto in leyenda_vacia.get_texts():
          texto.set_alpha(0)
        return fig

      colores_edad = {
          "23 años o menos": "#00E5FF",
          "de 24 a 29 años": GOLD,
          "30 años o más": "#FF5252",
      }

      for grupo in seleccion:
        sub_df = datos[datos["GrupoEdad"] == grupo]
        promedios = sub_df[stats].mean().tolist()
        promedios += promedios[:1]

        ax.plot(
            angulos,
            promedios,
            linewidth=2.2,
            label=f"{grupo} ({len(sub_df)})",
            color=colores_edad[grupo],
        )
        ax.fill(angulos, promedios, color=colores_edad[grupo], alpha=0.2)

      ax.set_title(
          "",
          color=GOLD,
          fontsize=14,
          fontweight="bold",
          pad=25,
      )

      leyenda = ax.legend(
          loc="center left",
          bbox_to_anchor=(1.52, 0.5),
          frameon=False,
          title="Rango de Edad",
          alignment="left",
      )
      leyenda.get_title().set_color(GOLD)
      leyenda.get_title().set_fontweight("bold")
      leyenda.get_title().set_fontsize(12)
      for texto in leyenda.get_texts():
        texto.set_color(WHITE)

      return fig