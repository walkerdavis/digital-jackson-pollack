import math

import numpy as np
import random as rand
from scipy import interpolate


def paint_line(canvas, x0, y0, x1, y1, color):
    num_points = max(abs(x0 - x1), abs(y0 - y1))
    xs = np.linspace(x0, x1, num_points)
    ys = np.linspace(y0, y1, num_points)

    for i in range(len(xs) - 1):
        canvas[int(math.ceil(xs[i]))][int(math.ceil(ys[i]))] = color
        canvas[int(math.floor(xs[i]))][int(math.floor(ys[i]))] = color


def paint_line_curved(canvas, color):
    num_points = np.random.randint(3, 6)

    x = np.random.randint(0, canvas.shape[0], size=num_points)
    while x.shape[0] > np.unique(x).shape[0]:
        x = np.unique(x)
        x = np.concatenate([x, np.random.randint(0, canvas.shape[0], size=1)])
    x.sort()
    y = np.random.randint(0, canvas.shape[1], size=num_points)

    x2 = np.linspace(x[0], x[-1], (x[-1] - x[0]) * 4)
    x2.sort()
    x2, indices = np.unique(x2, return_index=True)
    y2 = interpolate.pchip_interpolate(x, y, x2[indices])

    for i in range(len(x2)):
        if y2[i] < canvas.shape[1]:
            canvas[int(math.ceil(x2[i]))][int(math.ceil(y2[i]))] = color
        canvas[int(math.floor(x2[i]))][int(math.floor(y2[i]))] = color


def scribble(canvas, color):
    num_points = np.random.randint(3, 6)
    splat_width = 4
    splat_height = 20
    x_neighbor_width = 80

    x = np.random.randint(0, canvas.shape[0], size=num_points)
    while (
        (min(abs(np.ediff1d(x))) < x_neighbor_width)
        | (max(x) - min(x) <= ((splat_width + 1) * num_points))
        | (x.shape[0] != np.unique(x).shape[0])
        | (x[1] - x[0] <= splat_width)
        | (x[-1] - x[-2] <= splat_width)
    ):
        x = np.random.randint(0, canvas.shape[0], size=num_points)
    x.sort()
    y = np.random.randint(0, canvas.shape[1], size=num_points)

    v, w = x.copy(), y.copy()

    for i in range(num_points - 2):
        v_temp = v[i + 1] + rand.randint(-splat_width, splat_width)
        while v_temp in v:
            v_temp = v[i + 1] + rand.randint(-splat_width, splat_width)
        v[i + 1] = min(max(v_temp, 0), canvas.shape[0] - 1)
        w[i + 1] += min(
            max(rand.randint(-splat_height, splat_height), 0), canvas.shape[1] - 1
        )
    v.sort()

    line_res = 5
    x2 = np.linspace(x[0], x[-1], (x[-1] - x[0]) * line_res)
    x2, indices = np.unique(x2, return_index=True)
    y2 = interpolate.pchip_interpolate(x, y, x2[indices])

    v2 = np.linspace(v[0], v[-1], (v[-1] - v[0]) * line_res)
    v2, indices = np.unique(v2, return_index=True)
    w2 = interpolate.pchip_interpolate(v, w, v2[indices])

    for i in range(len(x2)):
        if y2[i] < canvas.shape[1]:
            canvas[int(math.ceil(x2[i]))][int(math.ceil(y2[i]))] = color
        canvas[int(math.floor(x2[i]))][int(math.floor(y2[i]))] = color

        if (
            (v2[i] >= 0)
            & (w2[i] >= 0)
            & (v2[i] < canvas.shape[0])
            & (w2[i] < canvas.shape[1] - 1)
        ):
            canvas[int(math.ceil(v2[i]))][int(math.ceil(w2[i]))] = color
            canvas[int(math.floor(v2[i]))][int(math.floor(w2[i]))] = color
