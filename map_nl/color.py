import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np


def get_color_function(data: np.array):
    min_value = np.min(data)
    max_value = np.max(data)
    cmap_name = "YlOrRd"

    def get_color(d):
        if not d:
            return None
        cmap = plt.get_cmap(cmap_name)
        norm = mcolors.Normalize(vmin=min_value, vmax=max_value)
        rgba_color = cmap(norm(float(d)))
        hex_color = mcolors.to_hex(rgba_color)
        return hex_color

    return get_color
