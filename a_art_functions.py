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

from a_lines_and_shapes_functions import *


def get_random_colors(num_colors):
    """
    Generate HSL values of a specified amount of colors

    Args:
        num_colors: Integer of how many colors you would like

    Returns:
        palette: An array that contains arrays of 3 RGB values, integers between 0 and 255
    """
    palette = []
    for swatch in range(0, num_colors + 1):
        color = []
        #hue
        color.append(rand.uniform(0, 360))
        #saturation
        color.append(rand.uniform(0, 100))
        #lightness
        color.append(rand.uniform(0, 100))
        palette.append(color)

    return palette


def get_color_str(color_list):
    # print(len(color_list))

    color_str = 'hsl('
    color_str += str(color_list[0]) + ','
    color_str += str(color_list[1]) + '%,'
    color_str += str(color_list[2]) + '%)'

    return color_str


def get_similar_color(hsl_color):
    color_dif = .04
    new_color = []
    new_color.append(hsl_color[0] * rand.uniform(1 - color_dif, 1 + color_dif))
    new_color.append(hsl_color[1] * rand.uniform(1 - color_dif, 1 + color_dif))
    new_color.append(hsl_color[2] * rand.uniform(1 - (color_dif/2), 1 + (color_dif/2)))

    return new_color




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


def jackson_pollack2(width, height, num_colors, num_splatters, num_layers=1):
    """
    Generate Jackson Pollack inspired digital canvas
    
    Args:
        width (int): Width of canvas; number of columns in numpy array
        height (int): Height of canvas; number of rows in numpy array
        num_colors (int): Number of unique colors you would like for your canvas
        num_splatters (int): Number of lines you would like on your canvas
        num_layers (int): Number of layers/passes to apply splats in
        
    Returns:
        canvas (2-D numpy array): A numpy array of (width, height) dimensions
        layer_canvas (2-D numpy array): A numpy array tracking which layer each pixel belongs to
    """
    perimeter = 2
    width += perimeter * 2
    height += perimeter * 2
    canvas = np.zeros((width, height), dtype=int)
    layer_canvas = np.zeros((width, height), dtype=int)  # Track which layer each pixel belongs to
    
    # Divide splats across layers
    splats_per_layer = num_splatters // num_layers
    remainder = num_splatters % num_layers

    def get_point_on_perimter(width, height, zone):
        if zone == "top":
            x = rand.randint(0, width - 1)
            y = 0
        elif zone == "bottom":
            x = rand.randint(0, width - 1)
            y = height - 1
        elif zone == "left":
            x = 0
            y = rand.randint(0, height - 1)
        elif zone == "right":
            x = width - 1
            y = rand.randint(0, height - 1)
        else:
            raise

        return x, y

    # Apply splats in layers
    for layer in range(num_layers):
        # Add remainder splats to last layer
        layer_splats = splats_per_layer + (remainder if layer == num_layers - 1 else 0)
        
        for i in range(layer_splats):
            zones = ["top", "bottom", "left", "right"]
            zone0 = zones.pop(rand.randint(0, len(zones) - 1))
            zone1 = zones.pop(rand.randint(0, len(zones) - 1))

            x0, y0 = get_point_on_perimter(width, height, zone0)
            x1, y1 = get_point_on_perimter(width, height, zone1)

            color = rand.uniform(1, num_colors)
            paint_line(canvas, x0, y0, x1, y1, color)
            # Track which layer this pixel belongs to (update layer_canvas for painted pixels)
            paint_line(layer_canvas, x0, y0, x1, y1, layer)

    canvas = canvas[perimeter:width - perimeter, perimeter:height - perimeter]
    layer_canvas = layer_canvas[perimeter:width - perimeter, perimeter:height - perimeter]
    
    return canvas, layer_canvas


def cy_twombly(width, height, num_colors, num_splatters):
    canvas = np.zeros((width, height), dtype=int)

    for x in range(0, num_splatters):
        color = rand.randint(1, num_colors)
        scribble(canvas, color)

    return canvas


def canvas_to_image(canvas=None, palette=None, alpha=255, layer_canvas=None):

    #if canvas palette are both NOT passed as arguments
    if canvas is None and palette is None:
        canvas = jackson_pollack(255, 255, 8, 5000)
        palette = get_random_colors(8)

    #if canvas is not passed but palette is
    elif canvas is None and palette is not None:
        canvas = jackson_pollack(255, 255, len(palette), 5000)

    #if canvas is passed but palette is not
    elif canvas is not None and palette is None:
        palette = get_random_colors(len(np.unique(canvas)))

    #create image with alpha channel if alpha < 255 or layer_canvas provided
    mode = 'RGBA' if (alpha < 255 or layer_canvas is not None) else 'RGB'
    image = Image.new(mode, (canvas.shape))

    if len(np.unique(canvas)) > len(palette) + 1:
        print('WARNING: There are more colors on your canvas than in your palette.  This will increase the splatters of the first colors in your palette.')
    if len(np.unique(canvas)) < len(palette) + 1:
        print('WARNING: Your palette has more colors than your canvas.  Some of your colors will not be splattered on your canvas.')

    #write each pixel
    for (x, y), value in np.ndenumerate(canvas):
        if canvas[x][y] == 0:
            rgb = ImageColor.getrgb(get_color_str(get_similar_color(palette[0])))
        else:
            pixel_str = get_color_str(palette[(canvas[x][y] % len(palette))])
            rgb = ImageColor.getrgb(pixel_str)
        
        # Determine alpha value for this pixel
        if mode == 'RGBA':
            if layer_canvas is not None:
                # Bottom layer (0) is fully opaque, upper layers use the specified alpha
                pixel_layer = int(layer_canvas[x][y])
                pixel_alpha = 255 if pixel_layer == 0 else alpha
            else:
                pixel_alpha = alpha
            image.putpixel((x, y), rgb + (pixel_alpha,))
        else:
            image.putpixel((x, y), rgb)
            

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
