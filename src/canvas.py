import random as rand

import numpy as np

from src.lines import paint_line, scribble


def jackson_pollack(width, height, num_colors, num_splatters, num_layers=1):
    perimeter = 2
    width += perimeter * 2
    height += perimeter * 2
    canvas = np.zeros((width, height), dtype=int)
    layer_canvas = np.zeros((width, height), dtype=int)

    splats_per_layer = num_splatters // num_layers
    remainder = num_splatters % num_layers

    def get_point_on_perimeter(w, h, zone):
        if zone == "top":
            return rand.randint(0, w - 1), 0
        elif zone == "bottom":
            return rand.randint(0, w - 1), h - 1
        elif zone == "left":
            return 0, rand.randint(0, h - 1)
        elif zone == "right":
            return w - 1, rand.randint(0, h - 1)
        raise ValueError(f"Invalid zone: {zone}")

    for layer in range(num_layers):
        layer_splats = splats_per_layer + (
            remainder if layer == num_layers - 1 else 0
        )

        for _ in range(layer_splats):
            zones = ["top", "bottom", "left", "right"]
            zone0 = zones.pop(rand.randint(0, len(zones) - 1))
            zone1 = zones.pop(rand.randint(0, len(zones) - 1))

            x0, y0 = get_point_on_perimeter(width, height, zone0)
            x1, y1 = get_point_on_perimeter(width, height, zone1)

            color = rand.uniform(1, num_colors)
            paint_line(canvas, x0, y0, x1, y1, color)
            paint_line(layer_canvas, x0, y0, x1, y1, layer)

    canvas = canvas[perimeter : width - perimeter, perimeter : height - perimeter]
    layer_canvas = layer_canvas[
        perimeter : width - perimeter, perimeter : height - perimeter
    ]

    return canvas, layer_canvas


def cy_twombly(width, height, num_colors, num_splatters):
    canvas = np.zeros((width, height), dtype=int)
    for _ in range(num_splatters):
        color = rand.randint(1, num_colors)
        scribble(canvas, color)
    return canvas
