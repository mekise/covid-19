import sys, os
import numpy as np
import pandas as pd
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import cv2
import glob

# dimension figure
my_dpi=96
fig = plt.figure(figsize=(1920/my_dpi, 1080/my_dpi), dpi=my_dpi)

# read the data (online - John Hopkins University)
confirmed = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv', sep=",")
recovered = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv', sep=",")
deaths = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv', sep=",")

# basemap
bmap = Basemap(projection='cyl')
# bmap.drawmapboundary(fill_color='#93aac4', linewidth=0) # light theme
# bmap.fillcontinents(color='#6a7380', alpha=0.5) # light theme
bmap.drawmapboundary(fill_color='#0e3745', linewidth=0) # dark theme
bmap.fillcontinents(color='#6f8781', alpha=0.4) # dark theme
bmap.drawcoastlines(linewidth=0.1, color="white")

col = 'sandybrown' # color scatter if uniform
leg = [Line2D([0], [0], marker='o', color='w', label='200 infections', markerfacecolor=col, markersize=15, alpha=0.8)]

plt.legend(handles=leg, loc='center', bbox_to_anchor=(0.07, 0.25))
plt.text(0, -45,'COVID-19 - population infected', ha='center', va='center', size=27, color='#999999' ) # dark theme
# plt.text(0, -45,'COVID-19 - population infected', ha='center', va='center', size=27, color='#111111' ) # light theme

# color for each point depending on the country.
confirmed['labels_enc'] = pd.factorize(confirmed['Country/Region'])[0]
confirmed['labels_enc'] = confirmed['labels_enc']/max(confirmed['labels_enc'])*256

def show_plot(i,j):
	index = str(j)+'/'+str(i+1)+'/20'
	bubbles = bmap.scatter(confirmed['Long'], confirmed['Lat'], s=(confirmed[index]-recovered[index]), alpha=0.7, c=col) #confirmed['labels_enc'], cmap="Pastel1")
	date = plt.text(0, -60,'date: '+str(i+1)+'/'+str(j)+'/2020', ha='center', va='center', size=26, color='#999999') # dark theme
	# date = plt.text(0, -60,'date: '+str(i+1)+'/'+str(j)+'/2020', ha='center', va='center', size=25, color='#111111') # light theme
	if i+1 < 10:
		fig.savefig('./fig/map'+str(j)+'0'+str(i+1), bbox_inches='tight')
	else:
		fig.savefig('./fig/map'+str(j)+str(i+1), bbox_inches='tight')
	bubbles.remove()
	date.remove()
	return()

for j in range(1,5):
	if j==1:
		days = range(21,31) # January
	elif j==2:
		days = range(29) # February
	elif j==3:
		days = range(31) # March
	elif j==4:
		days = range(14) # April
	for i in days:
		show_plot(i,j)

# video creation
img_array = []
for filename in sorted(glob.glob('./fig/*.png')):
	img = cv2.imread(filename)
	height, width, layers = img.shape
	size = (width,height)
	img_array.append(img)

FPS = 4
out = cv2.VideoWriter('covid_animation.mkv',cv2.VideoWriter_fourcc(*'XVID'), FPS, size) # use MPEG for better quality

for i in range(len(img_array)):
	out.write(img_array[i])
[out.write(img_array[-1]) for _ in range(10)] # write last plot for n frames

out.release() # close video and save