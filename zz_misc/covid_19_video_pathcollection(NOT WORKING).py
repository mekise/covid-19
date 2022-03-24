import numpy as np
import pandas as pd
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# setup writer for saving the movie file
Writer = animation.writers['ffmpeg']
writer = Writer(fps=15, metadata=dict(artist='Stefano Scali'), bitrate=1800)

# dimension figure
my_dpi=96
fig1 = plt.figure(figsize=(2600/my_dpi, 1800/my_dpi), dpi=my_dpi)

# read the data (online - John Hopkins Univeristy)
confirmed = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv', sep=",")
recovered = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv', sep=",")
deaths = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv', sep=",")
active = confirmed['3/1/20']-recovered['3/1/20']

# basemap
bmap = Basemap(projection='cyl')
bmap.drawmapboundary(fill_color='#060f36', linewidth=0)
bmap.fillcontinents(color='#3a4954', alpha=0.3)
bmap.drawcoastlines(linewidth=0.1, color="white")

# color for each point depending on the continent.
confirmed['labels_enc'] = pd.factorize(confirmed['Country/Region'])[0]

# NB: bmap.scatter is a 'pathcollection'. bmap.plot would have been a tuple
evol = bmap.scatter(confirmed['Long'], confirmed['Lat'], s=(confirmed['3/1/20']-recovered['3/1/20'])/4, alpha=0.5, c=confirmed['labels_enc'], cmap="Set1")

def update(i):
    evol.set_sizes((confirmed['3/'+str(i+1)+'/20']-recovered['3/'+str(i+1)+'/20'])/4)
    return evol

video = animation.FuncAnimation(fig1, update, frames=13, interval=200, blit=True)
video.save('COVID-19.mp4', writer=writer)

# plt.text( -170, -30,'COVID-19 diffusion over time', ha='left', va='bottom', size=24, color='#888888' )
# plt.tight_layout()