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

    if len(np.unique(canvas)) > len(palette) + 1:
        print('WARNING: There are more colors on your canvas than in your palette.  This will increase the splatters of the first colors in your palette.')
    if len(np.unique(canvas)) < len(palette) + 1:
        print('WARNING: Your palette has more colors than your canvas.  Some of your colors will not be splattered on your canvas.')

    #write each pixel
    for (x, y), value in np.ndenumerate(canvas):
        if canvas[x][y] == 0:
            image.putpixel((x, y), ImageColor.getrgb(
                get_color_str(get_similar_color(palette[0]))))
        else:
            pixel_str= get_color_str(palette[(canvas[x][y] % len(palette))])
            image.putpixel((x, y), ImageColor.getrgb(pixel_str))
            

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
