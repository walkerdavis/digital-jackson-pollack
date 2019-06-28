#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
functions for digital jackson pollacks

walker davis
"""

from PIL import Image, ImageDraw, ImageColor
import math
import numpy as np
import random as rand
from scipy import interpolate


def paint_line(canvas, x0, y0, x1, y1, color):
    """
    Draw a line on your canvas

    Args:
        canvas: A 2-D numpy array of integers
        x0,y0: Integers coordinates at which the line begins
        x1,y1: Integers coordinate at which the line ends
        color: Integer that represents of these colors in your pallete

    Returns:
        Nothing, but your canvas has a new line on it.
    """
    hypotenuse = int(pow((pow(x0-x1, 2) + pow(y0-y1, 2)), 1/2))

    #create the points at every pixel between each coordinate
    xs = np.linspace(x0, x1, hypotenuse+2)
    ys = np.linspace(y0, y1, hypotenuse+2)

    #do splatter
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

    x2 = np.linspace(x[0], x[-1], (x[-1] - x[0])*4)
    x2.sort()
    x2, indices = np.unique(x2, return_index=True)
    y2 = interpolate.pchip_interpolate(x, y, x2[indices])

    #do splatter
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
    while ((min(abs(np.ediff1d(x))) < x_neighbor_width) |
            (max(x) - min(x) <= ((splat_width + 1) * num_points)) |
            (x.shape[0] != np.unique(x).shape[0]) | 
            (x[1] - x[0] <= splat_width) |
            (x[-1] - x[-2] <= splat_width)):
        x = np.random.randint(0, canvas.shape[0], size=num_points)
    x.sort()
    y = np.random.randint(0, canvas.shape[1], size=num_points)

    v, w = x.copy(), y.copy()

    for i in range(num_points - 2):
        v_temp = v[i + 1] + rand.randint(-splat_width, splat_width)
        while v_temp in v:
            v_temp = v[i + 1] + rand.randint(-splat_width, splat_width)
        v[i + 1, ] = min(max(v_temp, 0), canvas.shape[0]-1)
        w[i + 1, ] += min(max(rand.randint(-splat_height,
                                             splat_height), 0), canvas.shape[1]-1)
    v.sort()

    line_res = 5
    x2 = np.linspace(x[0], x[-1], (x[-1] - x[0])*line_res)
    x2, indices = np.unique(x2, return_index=True)
    y2 = interpolate.pchip_interpolate(x, y, x2[indices])

    v2 = np.linspace(v[0], v[-1], (v[-1] - v[0])*line_res)
    v2, indices = np.unique(v2, return_index=True)
    w2 = interpolate.pchip_interpolate(v, w, v2[indices])

    #do splatter
    for i in range(len(x2)):
        if y2[i] < canvas.shape[1]:
            canvas[int(math.ceil(x2[i]))][int(math.ceil(y2[i]))] = color
        canvas[int(math.floor(x2[i]))][int(math.floor(y2[i]))] = color

        if (v2[i] >= 0) & (w2[i] >= 0) & (v2[i] < canvas.shape[0]) & (w2[i] < canvas.shape[1] - 1):
            canvas[int(math.ceil(v2[i]))][int(math.ceil(w2[i]))] = color
            canvas[int(math.floor(v2[i]))][int(math.floor(w2[i]))] = color

def get_random_colors(num_colors):
    """
    Generate RGB values of a specified amount of colors

    Args:
        num_colors: Integer of how many colors you would like

    Returns:
        palette: An array that contains arrays of 3 RGB values, integers between 0 and 255
    """
    palette = []
    for swatch in range(0, num_colors + 1):
        color = 'hsl('
        #hue
        color += str(rand.uniform(0, 360)) + ','
        #saturation
        color += str(rand.uniform(0, 100)) + '%,'
        #lightness
        color += str(rand.uniform(0, 100)) + '%)'
        palette.append(color)

    return palette


def get_similar_color(hsl_color_str):
    color_dif = .04
    h = float(hsl_color_str.split(',')[0][4:]) * \
        rand.uniform(1 - color_dif, 1 + color_dif)
    s = float(hsl_color_str.split(',')[1][:-1]) * \
        rand.uniform(1 - color_dif, 1 + color_dif)
    l = float(hsl_color_str.split(',')[2][:-2]) * \
        rand.uniform(1 - (color_dif/2), 1 + (color_dif/2))

    return 'hsl(' + str(h) + ',' + str(s) + '%,' + str(l) + '%)'




def jackson_pollack(width, height, num_colors, num_splatters):
    """
    Generate Jackson Pollack inspired digital canvas
    
    Args:
        width (int): Width of canvas; number of columns in numpy array
        height (int): Height of canvas; number of rows in numpy array
        num_colors (int): Number of unique colors you would like for your canvas
        num_splatters (int): Number of lines you would like on your canvas
        
    Returns:
        canvas (2-D numpy array): A numpy array of (width, height) dimensions
    """
    canvas = np.zeros((width, height), dtype=int)

    for i in range(0, num_splatters):
        x0 = rand.randint(0, width - 1)
        y0 = rand.randint(0, height - 1)
        x1 = rand.randint(0, width - 1)
        y1 = rand.randint(0, height - 1)

        color = rand.uniform(1, num_colors)
        paint_line(canvas, x0, y0, x1, y1, color)

    return canvas


def cy_twombly(width, height, num_colors, num_splatters):
    canvas = np.zeros((width, height), dtype=int)

    for x in range(0, num_splatters):
        color = rand.randint(1, num_colors)
        scribble(canvas, color)

    return canvas


def canvas_to_image(canvas=[[]], palette=[]):

    #if canvas palette are both NOT passed as arguments
    if (canvas == [[]]) & (palette == []):
        canvas = jackson_pollack(255, 255, 8, 5000)
        palette = get_random_colors(8)

    #if canvas is not passed but palette is
    elif (canvas == [[]]) & (palette != []):
        canvas = jackson_pollack(255, 255, len(palette), 5000)

    #if canvas is passed but palette is not
    elif (canvas != [[]]) & (palette == []):
        palette = get_random_colors(len(np.unique(canvas)))

    #create image
    image = Image.new('RGB', (canvas.shape))

    if len(np.unique(canvas)) + 1 > len(palette):
        print('WARNING: There are more colors on your canvas than in your palette.  This will increase the splatters of the first colors in your palette.')
    if len(np.unique(canvas)) + 1 < len(palette):
        print('WARNING: Your palette has more colors than your canvas.  Some of your colors will not be splattered on your canvas.')

    #write each pixel
    for (x, y), value in np.ndenumerate(canvas):
        if canvas[x][y] == 0:
            image.putpixel((x, y), ImageColor.getrgb(
                get_similar_color(palette[0])))
        else:
            pixel_coordinate = palette[(canvas[x][y] % len(palette))]
            image.putpixel((x, y), ImageColor.getrgb(pixel_coordinate))
            

    return image


def add_border_to_image(image, border_size=30, color=(255, 255, 255), inplace=True):

    width = image.size[0]
    height = image.size[1]

    if inplace:
        for h in range(0, border_size):
            for w in range(0, width):
                image.putpixel((w, h), (color[0], color[1], color[2]))
                image.putpixel((w, height-(h+1)),
                               (color[0], color[1], color[2]))

        for h in range(border_size, height-border_size):
            for w in range(0, border_size):
                image.putpixel((w, h), (color[0], color[1], color[2]))
                image.putpixel((width-(w+1), h),
                               (color[0], color[1], color[2]))

    else:
        full_width = (border_size*2+width)
        full_height = (border_size*2+height)

        old_array = np.array(image)
        image = image.resize((full_width, full_height), Image.ANTIALIAS)

        for h in range(0, border_size):
            for w in range(0, full_width):
                image.putpixel((w, h), (color[0], color[1], color[2]))
                image.putpixel((w, full_height-(h+1)),
                               (color[0], color[1], color[2]))

        for h in range(border_size, full_height-border_size):
            for w in range(0, border_size):
                image.putpixel((w, h), (color[0], color[1], color[2]))
                image.putpixel((full_width-(w+1), h),
                               (color[0], color[1], color[2]))

        for h in range(0, width):
            for w in range(0, height):
                image.putpixel((h+border_size, w+border_size),
                               (old_array[w][h][0], old_array[w][h][1], old_array[w][h][2]))
