# Usage

_map-nl_ currently has two classes to help you create a PC4 map of the Netherlands: `MapNL` and `ChoroplethMapNL`.
`ChoroplethMapNL` a wrapper around [`folium.Choropleth`](https://python-visualization.github.io/folium/latest/reference.html#folium.features.Choropleth),
and `MapNL` is a wrapper around [`folium.GeoJson`](https://python-visualization.github.io/folium/latest/reference.html#folium.features.GeoJson). Both require
a pandas DataFrame with at least two columns; one containing the PC4 codes, and one containing a value to plot. For example:

| pc4  | WOZ |
| ---- | --- |
| 2343 | 200 |
| 3544 | 250 |
| ...  | ... |

## ChoroplethMapNL

`ChoroplethMapNL` allows you to create a PC4 choropleth map of the Netherlands.

An example is shown below.

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

Any other keyword-arguments passed to `plot()` are passed on to [`folium.Choropleth`](https://python-visualization.github.io/folium/latest/reference.html#folium.features.Choropleth). For example,
in order to change the colorscale that is used to fill the polygons, you could do:

```py
m = ChoroplethMapNL(geojson_simplify_tolerance=0.0001).plot(
    df,
    pc4_column_name="pc4",
    value_column_name="WOZ",
    legend_name="Average WOZ Value",
    fill_color = "OrRd"
)
```

For more customization options, see the documentation of [`folium.Choropleth`](https://python-visualization.github.io/folium/latest/reference.html#folium.features.Choropleth).

## MapNL

`MapNL` allows you to create a custom PC4 map of the Netherlands.

An example is shown below.

```py

import pandas as pd
from map_nl import MapNL

def get_color(value):
    if not value:
        return "grey"
    if value > 500:
        return "green"
    else:
        return "blue"

def style(feature):
    return {"fillColor": get_color(feature.get("properties").get("WOZ"))}

df = pd.read_csv("data/woz-pc4.csv")
m = MapNL(geojson_simplify_tolerance=0.0001).plot(
    df, pc4_column_name="pc4", value_column_name="WOZ", style_function=style, name="WOZ value"
)
m.save("map.html")
```

The above example will color any PC4-areas with a average WOZ above 500 green, blue if it is below 500, and grey if no average WOZ was found.

Any other keyword-arguments passed to `plot()` are passed on to [`folium.GeoJson`](https://python-visualization.github.io/folium/latest/reference.html#folium.features.GeoJson). For example,
in order to modify the default tooltip, you can define your own and provide that to the `plot()` method:

```py
tooltip = folium.GeoJsonTooltip(
    fields=["pc4_code", "gem_name", "WOZ"],
    aliases=["PC4:", "Gemeente:", "WOZ:"],
    localize=True,
    sticky=False,
    labels=True,
    style="""
        background-color: #F0EFEF;
        border: 3px solid black;
        border-radius: 10px;
        box-shadow: 10px;
    """,
    max_width=800,
)

m = MapNL(geojson_simplify_tolerance=0.0001).plot(
    df,
    pc4_column_name="pc4",
    value_column_name="WOZ",
    style_function=style,
    name="WOZ value",
    tooltip=tooltip
)
```

For more customization options, see the documentation of [`folium.GeoJson`](https://python-visualization.github.io/folium/latest/reference.html#folium.features.GeoJson).

## Customizing the map

Keyword arguments passed to the constructors of `MapNL` and `ChoroplethMapNL` are passed on to [`folium.Map`](https://python-visualization.github.io/folium/latest/reference.html#module-folium.folium). So for example,
in order to change the starting zoom level of the map, one could do:

```py
m = ChoroplethMapNL(geojson_simplify_tolerance=0.0001, zoom_start=7)
```

For more customization options, see the documentation of [`folium.Map`](https://python-visualization.github.io/folium/latest/reference.html#module-folium.folium).
