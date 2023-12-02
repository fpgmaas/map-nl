<p align="center" style="margin: 30px 30px 40px 30px;">
  <img alt="map nl" height="150px" width="150px" src="https://github.com/fpgmaas/map-nl/blob/main/docs/static/nl.png?raw=true">
</p>

# map-nl

[![Release](https://img.shields.io/github/v/release/fpgmaas/map-nl)](https://img.shields.io/github/v/release/fpgmaas/map-nl)
[![Build status](https://img.shields.io/github/actions/workflow/status/fpgmaas/map-nl/main.yml?branch=main)](https://github.com/fpgmaas/map-nl/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/fpgmaas/map-nl/branch/main/graph/badge.svg)](https://codecov.io/gh/fpgmaas/map-nl)
[![Commit activity](https://img.shields.io/github/commit-activity/m/fpgmaas/map-nl)](https://img.shields.io/github/commit-activity/m/fpgmaas/map-nl)
[![License](https://img.shields.io/github/license/fpgmaas/map-nl)](https://img.shields.io/github/license/fpgmaas/map-nl)

_map-nl_ is a Python package to help you quickly create [PC4](https://www.cbs.nl/nl-nl/dossier/nederland-regionaal/geografische-data/gegevens-per-postcode) maps of the Netherlands, i.e. maps based on the numerical part of Dutch postal codes. While that is already possible without _map-nl_, this package aims to make the process a lot easier. It automatically downloads the geojson files, so all you need to provide is a dataset with two columns: One containing PC4 codes and one with a related value to plot on the map. _map-nl_ then uses [folium](https://github.com/python-visualization/folium) to plot the map.

For an example map created with _map-nl_, see [here](https://fpgmaas.github.io/map-nl/static/choropleth.html).

## Quickstart

### Installation

To install _map-nl_, simply run:

```shell
pip install map-nl
```

or a similar command for your dependency manager.

### Usage

To create a choropleth map of the average WOZ-value in the Netherlands, you could run the following:

```py
import pandas as pd
from map_nl import ChoroplethMapNL

df = pd.read_csv("https://raw.githubusercontent.com/fpgmaas/map-nl/main/data/woz-pc4.csv")

m = ChoroplethMapNL(geojson_simplify_tolerance=0.0001).plot(
    df,
    pc4_column_name="pc4",
    value_column_name="WOZ",
    legend_name="Average WOZ Value"
)
m.save("map.html")
```

This will download the geojson file to the `.map_nl` directory, simplify the geojson file to reduce the disk size of the plot, plot the map and save it to disk.
