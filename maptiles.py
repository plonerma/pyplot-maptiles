"""https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Python"""

import numpy as np
from skimage import io

from pyproj import Proj

from collections import namedtuple
import matplotlib.pyplot as plt
from matplotlib import ticker

Tile = namedtuple('Tile', 'z x y')

WEBMERCATOR = Proj("+init=EPSG:3857")

class TileMap:
    def __init__(self, ax, url_fmt, lat_tick_step=10, lng_tick_step=10):
        self.tile_cache = dict()
        self.url_fmt = url_fmt
        self.ax = ax
        self.ax.set_aspect('equal')

        self.setup_ticks(lat_tick_step, lng_tick_step)

    def setup_ticks(self, lat_tick_step, lng_tick_step):
        self.ax.tick_params(axis='both', which='both',
                            bottom=True, top=True, labelbottom=True,
                            right=True, left=True, labelleft=True)


        lngs = np.arange(-180, 180, lng_tick_step)
        lng_ticks = [self.project((0, lng))[0] for lng in lngs]

        self.ax.set_xticks(lng_ticks)
        self.ax.set_xticklabels(["{}°".format(lng) for lng in lngs])
        self.ax.set_xlabel("Longitude")

        lats = np.arange(-90, 90, lat_tick_step)
        lat_ticks = [self.project((lat, 0))[1] for lat in lats]

        self.ax.set_yticks(lat_ticks)
        self.ax.set_yticklabels(["{}°".format(lat) for lat in lats])
        self.ax.set_ylabel("Latitude")

    def degree_from_index(self, tile):
        n = 2.0 ** tile.z
        lon_deg = tile.x / n * 360.0 - 180.0
        lat_rad = np.arctan(np.sinh(np.pi * (1 - 2 * tile.y / n)))
        lat_deg = np.degrees(lat_rad)
        return (lat_deg, lon_deg)

    def index_from_degree(self, lat_deg, lon_deg, zoom):
        lat_rad = np.radians(lat_deg)
        n = 2.0 ** zoom
        xtile = int((lon_deg + 180.0) / 360.0 * n)
        ytile = int((1.0 - np.log(np.tan(lat_rad) + (1 / np.cos(lat_rad))) / np.pi) / 2.0 * n)
        return Tile(zoom, xtile, ytile)

    def project(self, point, inverse=False):
        if inverse:
            return WEBMERCATOR(*point, inverse=True)[::-1]
        else:
            return WEBMERCATOR(*point[::-1], inverse=False)

    def fetch_tile(self, tile):
        url = self.url_fmt.format(z=tile.z, x=tile.x, y=tile.y)
        return io.imread(url)

    def get_tile(self, tile):
        if not tile in self.tile_cache:
            self.tile_cache[tile] = self.fetch_tile(tile)

        return self.tile_cache[tile]

    def plot_tile(self, tile):
        nw = tile
        se = Tile(nw.z, nw.x + 1, nw.y + 1)
        img = self.get_tile(tile)

        nw = self.project(self.degree_from_index(nw))
        se = self.project(self.degree_from_index(se))

        self.ax.imshow(img, extent=(nw[0], se[0], se[1], nw[1]), vmin=0, vmax=255)

    def plot_area(self, area, zoom=0):
        bounds = tuple(zip(*area))

        nw = max(bounds[0]), min(bounds[1])
        se = min(bounds[0]), max(bounds[1])

        start = self.index_from_degree(*nw, zoom)
        end = self.index_from_degree(*se, zoom)

        nw = self.project(nw)
        se = self.project(se)

        for x in range(start.x, end.x + 1):
            for y in range(start.y, end.y + 1):
                tile = Tile(zoom, x, y)
                self.plot_tile(tile)

        self.ax.set_xlim([nw[0], se[0]])
        self.ax.set_ylim([se[1], nw[1]])

        self.ax.plot([nw[0]], [nw[1]], marker='+', markersize=10, color='k', linewidth=0)
        self.ax.plot([se[0]], [se[1]], marker='+', markersize=10, color='k', linewidth=0)


class MapboxMap(TileMap):
    def __init__(self, ax, access_token, map_id="mapbox.streets", **kwargs):
        url_fmt = f"https://api.tiles.mapbox.com/v4/{map_id}/{{z}}/{{x}}/{{y}}@2x.png?access_token={access_token}"
        super().__init__(ax, url_fmt=url_fmt, **kwargs)
