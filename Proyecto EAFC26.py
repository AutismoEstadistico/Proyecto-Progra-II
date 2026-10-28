import os
from plotnine import (ggplot, aes, geom_boxplot, geom_col, geom_histogram, geom_point)
import pandas as pd
import numpy as np
import matplotlib as mlt
import seaborn as sns
import plotly.express as px
from shiny.express import input, render, ui
from theme import (
    FOOTBALL_CSS, FONT_LINK, POSITION_COLOURS, GOLD, PITCH_DARK,
    theme_pitch,
)



# Load your data
datos = pd.read_csv("EAFC26.csv")
datos = datos.drop(columns= ["url","card","ID"])



#Grafico 1

#Grafico 2

#Grafico 3

#Grafico 4

#Grafico 5
