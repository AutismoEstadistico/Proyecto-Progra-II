from plotnine import geom_point
from plotnine import ggplot
from plotnine import aes
from plotnine import geom_boxplot
import pandas as pd
import numpy as np
import matplotlib as mlt
import seaborn as sns
import plotly.express as px
import shiny


datos = pd.read_csv("EAFC26.csv")
datos = datos.drop(columns= ["url","card","ID"])
datos.head()

ggplot(datos, aes(x = "Preferred foot", y = "OVR", fill = "Position")) + geom_col() + facet_wrap("Position") + theme_bw()


ggplot(datos, aes (x = "DEF", y = "PHY", color = "GENDER")) + geom_point() + geom_smooth(method = "lm", color = "black") + theme_classic() + facet_wrap("GENDER")

#Grafico 1

#Grafico 2

#Grafico 3

#Grafico 4

#Grafico 5
