import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.basemap import Basemap

fig=plt.figure()

#map of Puerto Rico
bmap=Basemap(projection='merc', llcrnrlat=17.5,urcrnrlat=19.,llcrnrlon=-67.5, urcrnrlon=-65, epsg=4139)
bmap.arcgisimage(service='World_Shaded_Relief', xpixels = 2000)
plt.title("Flight Path of sbet 0059")

#sample coordinates
##lon=[-63,-64,-65,-66]
##lon=[int(l) for l in lon]
##lat=[17., 17.5, 18., 18.5]
##lat=[int(l) for l in lat]
##time=[1, 3, 5, 7]
##time=[int(l) for l in time]

#generate the flight coordinates (just a straight line with 100 points)
N = 100
lon = np.linspace(-64, -68, N)
lat = np.linspace(17, 19.5, N)

#only convert the coordinates once    
x,y = bmap(lon, lat)

#generate the original line object with only one point
line, = bmap.plot(x[0], y[0], linewidth = 1, color = 'm')

def animate(i):
    #this is doing all the magic. Every time animate is called, the line
    #will become longer by one point:
    line.set_data(x[:i],y[:i])  
    return line

anim=animation.FuncAnimation(fig, animate, frames=N, interval=N)

plt.show()