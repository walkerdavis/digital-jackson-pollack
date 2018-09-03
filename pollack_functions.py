#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
functions for digital jackson pollacks

walker davis
"""

import numpy as np
import math
import random
from PIL import Image, ImageDraw


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
        #randint is inclusive, need to subtract one from num_colors
        color = random.randint(0,num_colors-1)
        paint_line(canvas,x0,y0,x1,y1,color)

    return canvas




def create_pollack_image(canvas=[[]], palette=[]):
      
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
    image = Image.new('RGB', (canvas.shape[0],canvas.shape[1])) 
        
    if len(np.unique(canvas)) > len(palette):
        print('WARNING: There are more colors on your canvas than in your palette.  This will increase the splatters of the first colors in your palette.')
    if len(np.unique(canvas)) < len(palette):
        print('WARNING: Your palette has more colors than your canvas.  Some of your colors will not be splattered on your canvas.')
        
    #write each pixel
    for (x,y), value in np.ndenumerate(canvas):
        pixel_coordinate = palette[(canvas[x][y] % len(palette))] 
        image.putpixel((x, y), (pixel_coordinate[0], pixel_coordinate[1], pixel_coordinate[2]))

    return image



def add_border_to_image(image, border_size=30, color=(255,255,255), inplace=True):

    width = image.size[0]
    height = image.size[1]
    
    if inplace:
        for h in range(0,border_size):
            for w in range(0,width):
                image.putpixel((w,h), (color[0],color[1],color[2]))
                image.putpixel((w,height-(h+1)), (color[0],color[1],color[2]))

        for h in range(border_size, height-border_size):
            for w in range(0,border_size):
                image.putpixel((w,h), (color[0],color[1],color[2]))
                image.putpixel((width-(w+1),h), (color[0],color[1],color[2]))   
    
    else:
        full_width = (border_size*2+width)
        full_height = (border_size*2+height)
        
        old_array = np.array(image)
        image = image.resize((full_width, full_height), Image.ANTIALIAS)
        
        for h in range(0,border_size):
            for w in range(0,full_width):
                image.putpixel((w,h), (color[0],color[1],color[2]))
                image.putpixel((w,full_height-(h+1)), (color[0],color[1],color[2]))
                
        for h in range(border_size, full_height-border_size):
            for w in range(0,border_size):
                image.putpixel((w,h), (color[0],color[1],color[2]))
                image.putpixel((full_width-(w+1),h), (color[0],color[1],color[2]))
                
        for h in range(0,width):
            for w in range(0,height):
                image.putpixel((h+border_size,w+border_size),(old_array[w][h][0], old_array[w][h][1], old_array[w][h][2]))