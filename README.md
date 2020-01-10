# Plot Map Tiles in Pyplot

I wrote this map tile plotter to create basic geo-spatial data visualizations for [powerplace.io](//powerplace.io).

## Usage

Use class `TileMap` for plotting a map. Specify a map tile provider for download of map tile images.

`MapboxMap` wraps `TileMap` for usage with [Mapbox](//www.mapbox.com) maps (see `examples.py`).


## Example

![Example Plot](./example.png)

## HTTPError 401

If a request returns an http status code 401 (`urllib.error.HTTPError: HTTP Error 401: Unauthorized`) and you are using mapbox as an tile provider, it means that the api key you provided is invalid.
