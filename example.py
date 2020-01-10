import matplotlib.pyplot as plt
from maptiles import MapboxMap
import numpy as np


# Specify valid mapbox api key
access_token = "pk..."


# Initialize plot
fig, ax = plt.subplots()

# Initialize Map
map = MapboxMap(ax, access_token)

# Plot area
map.plot_area(area=[[55, -10], [30, 50]], zoom=4)

# Plot some points on the map
cities = [
    (52.51695, 13.38943), # Berlin
    (41.8988, 12.5451), # Rome
    (41.0098, 28.9652), # Istanbul
]

points = [map.project(city) for city in cities]
ax.plot(*zip(*points), "ro")

# Show interactive plot window
plt.show()
