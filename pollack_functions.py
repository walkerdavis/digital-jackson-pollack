#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
functions for digital jackson pollack's

walker davis
"""

import numpy as np
import math
import random



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
    xs=np.linspace(x0,x1,hypotenuse+2)
    ys=np.linspace(y0,y1,hypotenuse+2)

    #do splatter
    for i in range(len(xs)):
        canvas[int(math.ceil(xs[i]))][int(math.ceil(ys[i]))] = color
        canvas[int(math.floor(xs[i]))][int(math.floor(ys[i]))] = color




def get_random_colors(num_colors):
    """
    Generate RGB values of a specified amount of colors

    Args:
        num_colors: Integer of how many colors you would like

    Returns:
        palette: An array that contains arrays of 3 RGB values, integers between 0 and 255
    """
    palette = []
    for swatch in range(0, num_colors):
        color = []
        color.append(random.randint(0,255))
        color.append(random.randint(0,255))
        color.append(random.randint(0,255))
        palette.append(color)

    return palette





def jackson_pollack(width, height, num_colors, num_splatters):

    canvas = np.zeros((width,height),dtype=int)

    for x in range(0,num_splatters):
        x0 = random.randint(0,width-1)
        y0 = random.randint(0,height-1)
        x1 = random.randint(0,width-1)
        y1 = random.randint(0,height-1)
        color = random.randint(0,num_colors - 1)
        paint_line(canvas,x0,y0,x1,y1,color)

    return canvas




def writeToRuntFile(filename, canvas=[[]], palette=[]):
    with open(filename, 'w') as text_file:
        text_file.write("# generated image using jackson pollack jupyter notebook")
        text_file.write('\n')

        #set up palette
        if not palette:
            #use colors of your choice
            for i in range(0, len(palette)):
                color_inst = str(i) + ' ' + str(palette[i]) + ' pxclr'
                text_file.write(color_inst)
                text_file.write('\n')
        else:
            #use randomly generated colors
            for i in range(0, len(palette)):
                color_inst = str(i) + ' ' + str(palette[i]) + ' pxclr'
                text_file.write(color_inst)
                text_file.write('\n')

        #write each pxpt to file
        for (x,y), value in np.ndenumerate(canvas):
            pixel_str = str(x) + ' ' + str(y) + ' ' + str(canvas[x][y]) + ' pxpt'
            text_file.write(pixel_str)
            text_file.write('\n')


        footer_str = '\"' + filename.split(".")[0] + '.png\" pxsave'
        text_file.write(footer_str)
        text_file.write('\n')
