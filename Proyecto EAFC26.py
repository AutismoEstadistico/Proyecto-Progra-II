import os
from plotnine import (ggplot, aes, geom_boxplot, geom_col, geom_histogram, geom_point)
import pandas as pd
import numpy as np
import matplotlib as mlt
import seaborn as sns
import plotly.express as px
from shiny import App , render, ui
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

app_ui = ui.page_fluid(
    ui.h2("Datos de FC26"),
     ui.navset_card_tab(
        #Grafico 1
        ui.nav_panel(
            "Tab 1: Algo",
            ui.h4("Titulo grafico"),
            #Todo lo del grafico 1 va aca
        ),
        #Grafico 2
         ui.nav_panel(
            "Tab 2: Algo",
            ui.h4("Titulo grafico"),
            #Todo lo del grafico 2 va aca
        ),
        #Grafico 3
         ui.nav_panel(
            "Tab 1: Algo",
            ui.h4("Titulo grafico"),
            #Todo lo del grafico 3 va aca
        ),
         #Grafico 4
         ui.nav_panel(
            "Tab 1: Algo",
            ui.h4("Titulo grafico"),
            #Todo lo del grafico 4 va aca
        ),
        #Grafico 5
         ui.nav_panel(
            "Tab 1: Algo",
            ui.h4("Titulo grafico"),
            #Todo lo del grafico 5 va aca
        )
)

)

def server(input, output, session):
    #Tab 1
    @render.plot
    
    #Grafico aca
    #Tab 2
    @render.plot
    
    #Grafico aca

    #Tab 3
    @render.plot
    
    #Grafico aca
    #Tab 4
    @render.plot
    
    #Grafico aca

    #Tab 5
    @render.plot
    #Grafico aca

app = App(app_ui, server)
