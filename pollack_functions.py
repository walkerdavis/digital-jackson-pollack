#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
functions for digital jackson pollack's

walker davis
"""

import numpy as np
import math
import random


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
    canvas = np.zeros((width,height),dtype=int)

    for x in range(0,num_splatters):
        x0 = random.randint(0,width-1)
        y0 = random.randint(0,height-1)
        x1 = random.randint(0,width-1)
        y1 = random.randint(0,height-1)
        color = random.randint(0,num_colors - 1)
        paint_line(canvas,x0,y0,x1,y1,color)

    return canvas



def paint_line(canvas, x0, y0, x1, y1, color):
    """
    Draw a line on your canvas

    Args:
        canvas (2-D numpy array): A 2-D numpy array of integers
        x0,y0 (int): Coordinates at which the line begins
        x1,y1 (int): Coordinate at which the line ends
        color (int): Index of color in your palette array

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
        num_colors (int): How many colors you would like

    Returns:
        palette (an array of arrays): A canvas of 3 RGB values, integers between 0 and 255
    """
    palette = []
    for swatch in range(0, num_colors):
        color = []
        color.append(random.randint(0,255))
        color.append(random.randint(0,255))
        color.append(random.randint(0,255))
        palette.append(color)

    return palette





def writeToRuntFile(filename, canvas=np.array([[]]), palette=[]):
    """
    Write your canvas to a .rnt file
    
    Args:
        filename (str): path and filename you would like your canvas too
        canvas (2-D numpy array) (optional): Canvas of specified width, heights, and number of colors
        palette (array of arrays) (optional): An array of RGB values
        -if canvas or palette are not specified, canvas will be 256 x 256 pixels and will contain 8 colors
    
    Returns: Writes digital Jackson Pollack to .rnt file
    """
    
    with open(filename, 'w') as text_file:
        #write intro text for RUNT interpretation
        text_file.write("# generated image using jackson pollack jupyter notebook")
        text_file.write('\n')
        
        #set up canvas
        if canvas.size == 0:
            canvas = jackson_pollack(255, 255, 8, 5000)

        #set up palette
        if not palette:
            #use randomly generated colors
            palette = get_random_colors(8)
            
        #write RGB color values to be interpretted by RUNT
        for i in range(0, len(palette)):
            color_inst = str(i) + ' ' 
            for j in range(0,3):
                color_inst += str(palette[i][j]) + ' ' 
            color_inst += ' pxclr'
            text_file.write(color_inst)
            text_file.write('\n')

        #write each pxpt to file
        for (x,y), value in np.ndenumerate(canvas):
            pixel_str = str(x) + ' ' + str(y) + ' ' + str(canvas[x][y]) + ' pxpt'
            text_file.write(pixel_str)
            text_file.write('\n')

        #write outro text for RUNT interpretation
        footer_str = '\"' + filename.split(".")[0] + '.png\" pxsave'
        text_file.write(footer_str)
        text_file.write('\n')