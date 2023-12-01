<p align="center" style="margin: 30px 30px 40px 30px;">
  <img alt="map nl" height="150" src="https://github.com/fpgmaas/map-nl/blob/main/docs/static/nl.png?raw=true">
</p>

# map-nl

[![Release](https://img.shields.io/github/v/release/fpgmaas/map-nl)](https://img.shields.io/github/v/release/fpgmaas/map-nl)
[![Build status](https://img.shields.io/github/actions/workflow/status/fpgmaas/map-nl/main.yml?branch=main)](https://github.com/fpgmaas/map-nl/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/fpgmaas/map-nl/branch/main/graph/badge.svg)](https://codecov.io/gh/fpgmaas/map-nl)
[![Commit activity](https://img.shields.io/github/commit-activity/m/fpgmaas/map-nl)](https://img.shields.io/github/commit-activity/m/fpgmaas/map-nl)
[![License](https://img.shields.io/github/license/fpgmaas/map-nl)](https://img.shields.io/github/license/fpgmaas/map-nl)

_map-nl_ is a Python package to help you quickly create PC4 maps of the Netherlands, i.e. maps at the postal code 4 level. While that is already possible without _map-nl_, this package aims to make the process as simple as possible. It automatically downloads the geojson files, so all you need to provide is a dataset wtih two columns: PC4 codes and a related value to plot on the map. The package uses [folium](https://github.com/python-visualization/folium) to create the map.

---

<p align="center">
  <a href="https://fpgmaas.github.io/map-nl">Documentation</a> - <a href="https://fpgmaas.github.io/map-nl/contributing/">Contributing</a>
</p>

---

## Quickstart

### Installation

To add _map-nl_ to your project, run one of the following commands:

```shell
# Install with poetry
poetry add map-nl

# Install with pip
pip install map-nl
```

### Usage

To create a choropleth map of the average WOZ-value in the Netherlands, you could run the following:

```py
import pandas as pd
from map_nl import ChoroplethMapNL

df = pd.read_csv("https://raw.githubusercontent.com/fpgmaas/map-nl/main/data/woz-pc4.csv")

m = ChoroplethMapNL(geojson_simplify_tolerance=0.001).plot(
    df, pc4_column_name="pc4", value_column_name="WOZ", legend_name="Average WOZ Value"
)
m.save("map.html")
```

This will download the geojson file to the `.map_nl` directory, simplify the geojson file to reduce the disk size of the plot, plot the map and save it to disk.

For more details, see [the documentation](https://fpgmaas.github.io/map-nl).

---

Repository initiated with [fpgmaas/cookiecutter-poetry](https://github.com/fpgmaas/cookiecutter-poetry).
