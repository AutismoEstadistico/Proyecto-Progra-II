# --- IMPORTACIONES DE LIBRERÍAS Y TEMAS PERSONALIZADOS ---
from matplotlib.pyplot import plot
from functools import partial
from itertools import cycle
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import theme_sns  # Tema personalizado para gráficos de Seaborn
from plotnine import aes, element_text, geom_bar, geom_boxplot, ggplot, labs, theme
from plotnine import aes, element_text, geom_bar, geom_boxplot, geom_line, geom_point, ggplot, labs, theme
from shiny.express import input, render, ui  # Componentes reactivos e interfaz de Shiny Express
from shiny.ui import page_navbar

# Importación de variables de estilo, colores y temas personalizados desde theme.py
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
    CARD_BG,
    GRID,
)
from theme_ui import shiny_theme  # Tema visual general para la app de Shiny

# --- CONFIGURACIÓN GLOBAL DE ESTILO PARA SEABORN / MATPLOTLIB ---
# Define fondos oscuros estilo cancha, textos blancos/dorados y oculta bordes innecesarios
sns.set_theme(
    style="darkgrid",
    rc={
        "figure.facecolor": CARD_BG,
        "axes.facecolor": PITCH_DARK,
        "axes.edgecolor": PITCH_DARK,
        "grid.color": GRID,
        "text.color": WHITE,
        "axes.labelcolor": GOLD,
        "axes.titlecolor": WHITE,
        "xtick.color": WHITE,
        "ytick.color": WHITE,
        "legend.facecolor": CARD_BG,
        "legend.edgecolor": CARD_BG,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.spines.left": False,
        "axes.spines.bottom": False,
    },
)

# --- CARGA Y LIMPIEZA DE DATOS ---
# Load your data
datos = pd.read_csv("EAFC26.csv")  # Lee el dataset principal de jugadores
datos = datos.drop(columns= ["url","card","ID"])  # Elimina columnas innecesarias para el análisis

# Lista de ligas principales disponibles para filtrar en los menús
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

# Diccionario para agrupar posiciones específicas en 4 roles generales (Portero, Defensa, Medio, Delantero)
POSITION_GROUPS = {
    "GK": "GK",
    "CB": "DEF", "LB": "DEF", "RB": "DEF",
    "CDM": "MID", "CM": "MID", "CAM": "MID", "LM": "MID", "RM": "MID",
    "ST": "ATT", "LW": "ATT", "RW": "ATT",
}
datos["PosGroup"] = datos["Position"].map(POSITION_GROUPS)  # Crea columna con la posición agrupada

# Cálculo de límites de edad del dataset y asignación cíclica de colores por liga
edad_min = int(datos["Age"].min())
edad_max = int(datos["Age"].max())
colores = dict(zip(mis_5_ligas, cycle(PALETTE)))

# --- Agrupación de posiciones para el gráfico de Tab 2 ---
# Orden fijo pedido para el eje X (se excluye GK a propósito)
POS_ORDER_TAB2 = ["CB", "LB/RB", "CDM", "CM", "CAM", "LM/RM", "RW/LW", "ST"]

# Diccionario que combina bandas (izquierda/derecha) para la pestaña "Stats por pos"
POSITION_GROUPS_TAB2 = {
    "CB": "CB",
    "LB": "LB/RB", "RB": "LB/RB",
    "CDM": "CDM",
    "CM": "CM",
    "CAM": "CAM",
    "LM": "LM/RM", "RM": "LM/RM",
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

# --- CONFIGURACIÓN DE LA INTERFAZ PRINCIPAL (SHINY) ---
# Define el título de la página, barra de navegación superior y tema visual
ui.page_opts(
    title="EA FC 26",
    page_fn=partial(page_navbar, id="nav"),
    fillable=True,
    theme=shiny_theme(),
)

# ==============================================================================
# PESTAÑA 1: BIENVENIDA E IMÁGENES
# ==============================================================================
with ui.nav_panel("Hola :D"):
     # Distribuye el contenido en una cuadrícula de 2 columnas (ancho 6 de 12 cada tarjeta)
     with ui.layout_columns(col_widths=(6, 6, 6,6)):
         with ui.card():
            ui.p("Este es nuestro proyecto de programación II, una app usando datos de EAFC26! ")
         with ui.card():
            ui.p("A continuacion, van a observar una coleccion de graficos hechos con las librerias plotnine y seaborne. Disfruten!")
         with ui.card(style="width: fit-content; margin: 0 auto; text-align: center;"):
            ui.p("Aupa Athletic")
            ui.img(src = "AthleticCopaCampeones.jpg",style="max-height: 400px; width: auto; display: block; margin: 0 auto;")
         with ui.card(style="width: fit-content; margin: 0 auto; text-align: center;"):
            ui.p("Visca Barca")
            ui.img(src = "fcbarcelonachampions.png",style="max-height: 400px; width: auto; display: block; margin: 0 auto;")

# ==============================================================================
# PESTAÑA 2: BOXPLOT DE MEDIA GENERAL (OVR) POR LIGA
# ==============================================================================
with ui.nav_panel("OVR Ligas"):
  with ui.layout_sidebar():
    # Panel lateral con checkboxes para elegir una o varias ligas
    with ui.sidebar():
        ui.input_checkbox_group(
            "Ligas",
            "Ligas",
            choices=mis_5_ligas,
            selected=[mis_5_ligas[0]] if mis_5_ligas else [],
        )

    # Renderiza gráfico de cajas (boxplot) con plotnine según las ligas seleccionadas
    @render.plot
    def grafico1():
      chosen = input.Ligas()
      filtered_df = datos[datos["League"].isin(chosen)]

      # Mensaje de aviso si el usuario desmarca todas las ligas
      if filtered_df.empty:
        return ggplot() + labs(title="Please select at least one league")

      return (
          ggplot(filtered_df, aes(x="League", y="OVR", fill="League"))
          + geom_boxplot(color="white", outlier_color="white") + labs(title = "Overall por liga")
          + theme_pitch() + theme(plot_title= element_text(color = GOLD))
      )

# ==============================================================================
# PESTAÑA 3: EVOLUCIÓN DE ESTADÍSTICAS PROMEDIO SEGÚN POSICIÓN EN EL CAMPO
# ==============================================================================
with ui.nav_panel("Stats por pos"):
  with ui.layout_sidebar():
    # Panel lateral con checkboxes para seleccionar las estadísticas a comparar
    with ui.sidebar():
        ui.input_checkbox_group(
            "Stats",
            "Estadísticas",
            choices=STATS_COLS,
            selected=[STATS_COLS[0]],
        )

    # Renderiza gráfico de líneas y puntos con plotnine
    @render.plot
    def grafico2():
      chosen = input.Stats()

      # Valida que exista al menos una estadística seleccionada
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

      # Calcula el promedio de cada estadística por posición
      resumen = (
          df_largo.groupby(["PosGroupTab2", "Estadistica"], observed=True)["Valor"]
          .mean()
          .reset_index()
      )

      # Fuerza el orden del eje X pedido (de defensa central a delantero centro)
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
          + labs(x="Posición", y="Promedio", title = "Estadisticas basadas en la posicion del jugador")
          + theme_pitch() + theme(plot_title= element_text(color = GOLD))
      )

# ==============================================================================
# PESTAÑA 4: GRÁFICO DE RADAR (SPIDER) COMPARANDO DOS RANGOS DE EDAD
# ==============================================================================
with ui.nav_panel("Spider"):
  with ui.layout_sidebar():
    # Panel lateral con dos deslizadores (sliders) para comparar dos grupos de edad
    with ui.sidebar():
      ui.input_slider(
          "RangoEdad1",
          "Rango de Edad 1",
          min=edad_min,
          max=edad_max,
          value=(17, 17),
      )
      ui.input_slider(
          "RangoEdad2",
          "Rango de Edad 2",
          min=edad_min,
          max=edad_max,
          value=(44, 44),
      )

    # Renderiza gráfico polar/radar personalizado usando Matplotlib
    @render.plot
    def grafico3():
      # Atributos principales de la carta y cálculo de ángulos en radianes (cerrando el círculo)
      stats = ["PAC", "SHO", "PAS", "DRI", "DEF", "PHY"]
      angulos = np.linspace(0, 2 * np.pi, len(stats), endpoint=False).tolist()
      angulos += angulos[:1]

      # Creación de la figura polar y ajuste de márgenes para dejar espacio a la leyenda
      fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
      fig.subplots_adjust(left=0.0, right=0.40, top=0.82, bottom=0.12)
      fig.patch.set_facecolor("#0a2912")
      ax.set_facecolor("none")

      # Dibuja un rectángulo de fondo oscuro detrás del gráfico polar
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

      # Extiende las líneas radiales desde el centro hasta los bordes del rectángulo de fondo
      for deg in [90, 30, -30, -90, -150, 150]:
        rad = np.deg2rad(deg)
        dx, dy = np.cos(rad), np.sin(rad)
        tx = ((x_der - 0.5) / dx) if dx > 1e-9 else (((x_izq - 0.5) / dx) if dx < -1e-9 else np.inf)
        ty = ((y_sup - 0.5) / dy) if dy > 1e-9 else (((y_inf - 0.5) / dy) if dy < -1e-9 else np.inf)
        t = min(tx, ty)

        ax.plot(
            [0.5, 0.5 + t * dx],
            [0.5, 0.5 + t * dy],
            transform=ax.transAxes,
            color="#2c6b36",
            linewidth=0.6,
            alpha=1,
            clip_on=False,
            zorder=1,
        )

      # Configura orientación (PAC arriba, sentido horario), etiquetas, escala 0-100 y rejilla
      ax.set_theta_offset(np.pi / 2)
      ax.set_theta_direction(-1)

      ax.set_xticks(angulos[:-1])
      ax.set_xticklabels(stats, color=GOLD, fontsize=12, fontweight="bold")
      ax.set_ylim(0, 100)
      ax.set_yticks([20, 40, 60, 80])
      ax.set_yticklabels(["20", "40", "60", "80"], color=WHITE, fontsize=8)
      ax.grid(color="#2c6b36", alpha=1)
      ax.spines["polar"].set_color("#2c6b36")
      ax.spines["polar"].set_alpha(1)

      # Asocia cada slider de edad con su color de trazo (cian y rojo)
      rangos = [
          (input.RangoEdad1(), "#00E5FF"),
          (input.RangoEdad2(), "#FF5252"),
      ]

      # Filtra datos, calcula promedios y traza los polígonos en el radar
      graficados = 0
      for (r_min, r_max), color in rangos:
        sub_df = datos[datos["Age"].between(r_min, r_max)]
        if sub_df.empty:
          continue

        promedios = sub_df[stats].mean().tolist()
        promedios += promedios[:1]  # Cierra el polígono uniendo el último punto con el primero

        etiqueta_edad = f"{r_min} años" if r_min == r_max else f"{r_min}-{r_max} años"
        ax.plot(
            angulos,
            promedios,
            linewidth=2.2,
            label=f"{etiqueta_edad} ({len(sub_df)})",
            color=color,
        )
        ax.fill(angulos, promedios, color=color, alpha=0.2)
        graficados += 1

      # Manejo visual si ninguno de los dos rangos seleccionados contiene jugadores
      if graficados == 0:
        ax.set_title("Sin jugadores en los rangos elegidos", color=GOLD, pad=25)
        ax.plot([], [], color="none", label="19-21 años (0000)")
        leyenda_vacia = ax.legend(
            loc="center left",
            bbox_to_anchor=(1.52, 0.5),
            frameon=False,
            title="Rangos de Edad",
            alignment="left",
        )
        leyenda_vacia.get_title().set_alpha(0)
        for texto in leyenda_vacia.get_texts():
          texto.set_alpha(0)
        return fig

      # Título y configuración de la leyenda lateral derecha
      ax.set_title("Estadisticas promedio por rango de edad", color=GOLD, fontsize=14, fontweight="bold", pad=25)

      leyenda = ax.legend(
          loc="center left",
          bbox_to_anchor=(1.52, 0.5),
          frameon=False,
          title="Rangos de Edad",
          alignment="left",
      )
      leyenda.get_title().set_color(GOLD)
      leyenda.get_title().set_fontweight("bold")
      leyenda.get_title().set_fontsize(12)
      for texto in leyenda.get_texts():
        texto.set_color(WHITE)

      return(fig)

# ==============================================================================
# PESTAÑA 5: TOP 10 JUGADORES CON MEJOR TIRO LEJANO (BARRAS HORIZONTALES)
# ==============================================================================
with ui.nav_panel("Tiros"):
  with ui.layout_sidebar():
    # Panel lateral para filtrar por ligas y grupos de posición (ATT, MID, DEF)
    with ui.sidebar():
      ui.input_checkbox_group(
          "liga_tab4", "LIGAS", choices=mis_5_ligas, selected=["LALIGA EA SPORTS"]
      )
      ui.input_checkbox_group(
          "pos_tab4",
          "Posición",
          choices=["ATT", "MID", "DEF"],
          selected=["ATT", "MID"],
      )

    # Renderiza gráfico de barras horizontales con Matplotlib
    @render.plot
    def grafico4():
      # Filtra jugadores por posición y liga seleccionadas
      df = datos[
    (datos["PosGroup"].isin(input.pos_tab4()))
    & (datos["League"].isin(input.liga_tab4()))]

      fig, ax = plt.subplots(figsize=(8, 5), facecolor=PITCH_DARK)
      ax.set_facecolor(PITCH_DARK)

      # Si el filtro queda vacío, muestra aviso centrado
      if df.empty:
        ax.text(0.5, 0.5, "Sin datos", color=WHITE, ha="center")
        ax.axis("off")
        return fig

      # Ordena de mayor a menor "Long Shots", quita nombres duplicados y toma los 10 mejores (invertidos para barh)
      top10 = (
          df.sort_values("Long Shots", ascending=False)
          .drop_duplicates("Name")
          .head(10)[::-1]
      )
      barras = ax.barh(
          top10["Name"], top10["Long Shots"], color=PALETTE[: len(top10)]
      )

      # Añade etiquetas numéricas al final de cada barra y ajusta ejes/estilo
      ax.bar_label(barras, padding=4, color=WHITE, fmt="%.0f")
      ax.set_xlim(top10["Long Shots"].min() - 4, top10["Long Shots"].max() + 3)
      ax.set_title("Top 10 tiros lejanos", color=GOLD)
      ax.tick_params(colors=WHITE)
      ax.spines[["top", "right"]].set_visible(False)
      ax.spines[["bottom", "left"]].set_color(WHITE)
      plt.tight_layout()
      return fig

# ==============================================================================
# PESTAÑA 6: DISTRIBUCIÓN DE PORTEROS (GK) POR MEDIA Y NACIONALIDAD
# ==============================================================================
with ui.nav_panel("GK"):
  with ui.layout_sidebar():
    # Panel lateral con slider para filtrar el rango de edad de los porteros
    with ui.sidebar():
        ui.input_slider(
            "gk",
            "Edad del portero",
            min=17,
            max=44,
            value=(17, 44), 
        )

    # Renderiza histograma apilado por país usando Seaborn
    @render.plot
    def grafico5():
        edad_min, edad_max = input.gk()
        paises = ["Spain",
                "Argentina",
                "France",
                "England",
                "Morocco"]
        COLORES_PAIS = dict(zip(paises, theme_sns.pitch_palette(len(paises))))
        
        # Filtra únicamente porteros dentro del rango de edad y de los 5 países definidos
        df = datos[
            (datos["PosGroup"] == "GK")
            & (datos["Age"].between(edad_min, edad_max))
            & (datos["Nation"].isin(paises))
        ]
        
        # Genera el histograma apilado de OVR en intervalos de 5 puntos
        return sns.histplot(
            data=df,
            x="OVR",
            hue="Nation",
            hue_order= paises,
            multiple = "stack",
            palette= COLORES_PAIS,
                binwidth=5,
                binrange=(47, 90)
        ).set_title("Cantidad de porteros con OVR X por edad").set_color(GOLD)