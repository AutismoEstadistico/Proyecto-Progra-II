import pandas as pd
import numpy as np
import matplotlib as mlt
import seaborn as sns
import plotly.express as px
import shiny
from plotnine import * 

datos = pd.read_csv("EAFC26.csv")
datos = datos.drop(columns= ["url","card","ID"])
datos.head()

ggplot(datos, aes(x = "Preferred foot", y = "OVR", fill = "Position")) + geom_col() + facet_wrap("Position") + theme_bw()
