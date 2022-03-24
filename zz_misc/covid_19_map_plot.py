import numpy as np
import pandas as pd
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# dimension figure
my_dpi=96
plt.figure(figsize=(2600/my_dpi, 1800/my_dpi), dpi=my_dpi)

# read the data (online - John Hopkins Univeristy)
confirmed = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv', sep=",")
recovered = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv', sep=",")
deaths = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv', sep=",")

# basemap
m = Basemap(projection='cyl')
m.drawmapboundary(fill_color='#060f36', linewidth=0)
m.fillcontinents(color='#3a4954', alpha=0.3)
m.drawcoastlines(linewidth=0.1, color="white")

# color for each point depending on the continent.
confirmed['labels_enc'] = pd.factorize(confirmed['Country/Region'])[0]

m.scatter(confirmed['Long'], confirmed['Lat'], s=(confirmed['3/13/20']-recovered['3/13/20'])/4, alpha=0.5, c=confirmed['labels_enc'], cmap="Set1")

plt.text(0, -40,'COVID-19 diffusion over time', ha='center', va='center', size=24, color='#999999' )
plt.tight_layout()
plt.show()