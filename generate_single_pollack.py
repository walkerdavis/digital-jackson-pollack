#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Self-contained script to generate a single Jackson Pollack inspired image
All functionality in one file - no external dependencies beyond standard libraries and PIL/numpy/scipy
"""

from PIL import Image, ImageColor
import math
import numpy as np
import random as rand
from scipy import interpolate
import os
from datetime import datetime


# ============================================================================
# LINE AND SHAPE FUNCTIONS
# ============================================================================

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
    num_points = max(abs(x0-x1), abs(y0-y1))
    #create the points at every pixel between each coordinate
    xs = np.linspace(x0, x1, num_points)
    ys = np.linspace(y0, y1, num_points)

    #do splatter
    for i in range(len(xs) - 1):
        canvas[int(math.ceil(xs[i]))][int(math.ceil(ys[i]))] = color
        canvas[int(math.floor(xs[i]))][int(math.floor(ys[i]))] = color


# ============================================================================
# COLOR FUNCTIONS
# ============================================================================

def get_random_colors(num_colors):
    """
    Generate HSL values of a specified amount of colors

    Args:
        num_colors: Integer of how many colors you would like

    Returns:
        palette: An array that contains arrays of 3 HSL values
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
    """Convert HSL color list to HSL string format"""
    color_str = 'hsl('
    color_str += str(color_list[0]) + ','
    color_str += str(color_list[1]) + '%,'
    color_str += str(color_list[2]) + '%)'
    return color_str


def get_similar_color(hsl_color):
    """Generate a similar color with slight variations"""
    color_dif = .04
    new_color = []
    new_color.append(hsl_color[0] * rand.uniform(1 - color_dif, 1 + color_dif))
    new_color.append(hsl_color[1] * rand.uniform(1 - color_dif, 1 + color_dif))
    new_color.append(hsl_color[2] * rand.uniform(1 - (color_dif/2), 1 + (color_dif/2)))
    return new_color


# ============================================================================
# CANVAS GENERATION FUNCTIONS
# ============================================================================

def jackson_pollack2(width, height, num_colors, num_splatters, num_layers=1):
    """
    Generate Jackson Pollack inspired digital canvas with layering support
    
    Args:
        width (int): Width of canvas
        height (int): Height of canvas
        num_colors (int): Number of unique colors
        num_splatters (int): Number of lines to paint
        num_layers (int): Number of layers/passes to apply splats in
        
    Returns:
        canvas (2-D numpy array): The artwork
        layer_canvas (2-D numpy array): Tracking which layer each pixel belongs to
    """
    perimeter = 2
    width += perimeter * 2
    height += perimeter * 2
    canvas = np.zeros((width, height), dtype=int)
    layer_canvas = np.zeros((width, height), dtype=int)
    
    # Divide splats across layers
    splats_per_layer = num_splatters // num_layers
    remainder = num_splatters % num_layers

    def get_point_on_perimeter(width, height, zone):
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
            raise ValueError("Invalid zone")

        return x, y

    # Apply splats in layers
    for layer in range(num_layers):
        # Add remainder splats to last layer
        layer_splats = splats_per_layer + (remainder if layer == num_layers - 1 else 0)
        
        for i in range(layer_splats):
            zones = ["top", "bottom", "left", "right"]
            zone0 = zones.pop(rand.randint(0, len(zones) - 1))
            zone1 = zones.pop(rand.randint(0, len(zones) - 1))

            x0, y0 = get_point_on_perimeter(width, height, zone0)
            x1, y1 = get_point_on_perimeter(width, height, zone1)

            color = rand.uniform(1, num_colors)
            paint_line(canvas, x0, y0, x1, y1, color)
            paint_line(layer_canvas, x0, y0, x1, y1, layer)

    canvas = canvas[perimeter:width - perimeter, perimeter:height - perimeter]
    layer_canvas = layer_canvas[perimeter:width - perimeter, perimeter:height - perimeter]
    
    return canvas, layer_canvas


# ============================================================================
# IMAGE GENERATION FUNCTIONS
# ============================================================================

def canvas_to_image(canvas=None, palette=None, alpha=255, layer_canvas=None):
    """
    Convert canvas to PIL image with colors from palette
    
    Args:
        canvas: 2-D numpy array of color indices
        palette: List of HSL color tuples
        alpha: Alpha transparency value (0-255)
        layer_canvas: Optional layer tracking array
        
    Returns:
        PIL Image object
    """
    if canvas is None and palette is None:
        canvas = np.zeros((300, 300), dtype=int)
        palette = get_random_colors(8)

    elif canvas is None and palette is not None:
        canvas = np.zeros((300, 300), dtype=int)

    elif canvas is not None and palette is None:
        palette = get_random_colors(len(np.unique(canvas)))

    # Create image with alpha channel if needed
    mode = 'RGBA' if (alpha < 255 or layer_canvas is not None) else 'RGB'
    image = Image.new(mode, (canvas.shape[0], canvas.shape[1]))

    if len(np.unique(canvas)) > len(palette) + 1:
        print('WARNING: More colors on canvas than in palette.')
    if len(np.unique(canvas)) < len(palette) + 1:
        print('WARNING: Palette has more colors than canvas.')

    # Write each pixel
    for (x, y), value in np.ndenumerate(canvas):
        if canvas[x][y] == 0:
            rgb = ImageColor.getrgb(get_color_str(get_similar_color(palette[0])))
        else:
            pixel_str = get_color_str(palette[(canvas[x][y] % len(palette))])
            rgb = ImageColor.getrgb(pixel_str)
        
        # Determine alpha value for this pixel
        if mode == 'RGBA':
            if layer_canvas is not None:
                # Bottom layer is fully opaque
                pixel_layer = int(layer_canvas[x][y])
                pixel_alpha = 255 if pixel_layer == 0 else alpha
            else:
                pixel_alpha = alpha
            image.putpixel((x, y), rgb + (pixel_alpha,))
        else:
            image.putpixel((x, y), rgb)

    return image


def add_border_to_image(image, border_size=30, color=(255, 255, 255)):
    """
    Add a white border to an image (modifies in place)
    
    Args:
        image: PIL Image object
        border_size: Size of border in pixels
        color: RGB tuple for border color
    """
    width = image.size[0]
    height = image.size[1]

    # Top and bottom borders
    for h in range(0, border_size):
        for w in range(0, width):
            image.putpixel((w, h), (color[0], color[1], color[2]))
            image.putpixel((w, height-(h+1)), (color[0], color[1], color[2]))

    # Left and right borders
    for h in range(border_size, height-border_size):
        for w in range(0, border_size):
            image.putpixel((w, h), (color[0], color[1], color[2]))
            image.putpixel((width-(w+1), h), (color[0], color[1], color[2]))


# ============================================================================
# MAIN GENERATION FUNCTION
# ============================================================================

def generate_single_pollack(
    width=300,
    height=300,
    num_colors=8,
    num_splats=2000,
    num_layers=1,
    alpha=255,
    add_border=False,
    output_path=None
):
    """
    Generate a single Jackson Pollack inspired image
    
    Args:
        width: Image width in pixels
        height: Image height in pixels
        num_colors: Number of colors in palette
        num_splats: Number of paint strokes
        num_layers: Number of rendering layers (creates layered effect)
        alpha: Alpha transparency (255=opaque, lower=more transparent)
        add_border: Whether to add a white border
        output_path: File path to save image (if None, returns image object)
        
    Returns:
        PIL Image object (or saves to file if output_path provided)
    """
    
    # Automatically enable transparency for layered effect
    if num_layers > 1 and alpha == 255:
        alpha = 200
    
    # Generate the canvas
    canvas, layer_canvas = jackson_pollack2(width, height, num_colors, num_splats, num_layers)
    
    # Convert canvas to image
    image = canvas_to_image(
        canvas=canvas,
        alpha=alpha,
        layer_canvas=layer_canvas if num_layers > 1 else None
    )
    
    # Optionally add border
    if add_border:
        add_border_to_image(image, inplace=True)
    
    # Save or return
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        image.save(output_path, 'PNG')
        print(f"Image saved to {output_path}")
    
    return image


# ============================================================================
# COMMAND LINE INTERFACE
# ============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate a single Jackson Pollack inspired artwork"
    )
    
    parser.add_argument(
        '--width',
        type=int,
        default=300,
        help='Width of image in pixels (default: 300)'
    )
    parser.add_argument(
        '--height',
        type=int,
        default=300,
        help='Height of image in pixels (default: 300)'
    )
    parser.add_argument(
        '--colors',
        type=int,
        default=8,
        help='Number of colors in palette (default: 8)'
    )
    parser.add_argument(
        '--splats',
        type=int,
        default=2000,
        help='Number of paint strokes (default: 2000)'
    )
    parser.add_argument(
        '--layers',
        type=int,
        default=1,
        help='Number of rendering layers (default: 1)'
    )
    parser.add_argument(
        '--alpha',
        type=int,
        default=255,
        help='Alpha transparency (0-255, default: 255=opaque)'
    )
    parser.add_argument(
        '--border',
        action='store_true',
        help='Add a white border to the image'
    )
    parser.add_argument(
        '--output',
        '-o',
        type=str,
        help='Output file path (default: pollack_<timestamp>.png in current directory)'
    )
    
    args = parser.parse_args()
    
    # Generate output path if not provided
    if not args.output:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.output = f"pollack_{timestamp}.png"
    
    # Generate the image
    generate_single_pollack(
        width=args.width,
        height=args.height,
        num_colors=args.colors,
        num_splats=args.splats,
        num_layers=args.layers,
        alpha=args.alpha,
        add_border=args.border,
        output_path=args.output
    )
