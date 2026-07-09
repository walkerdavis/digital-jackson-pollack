import numpy as np
from PIL import Image, ImageColor

from src.colors import get_color_str, get_random_colors, get_similar_color


def canvas_to_image(canvas, palette=None, alpha=255, layer_canvas=None):
    if palette is None:
        palette = get_random_colors(len(np.unique(canvas)))

    mode = "RGBA" if (alpha < 255 or layer_canvas is not None) else "RGB"
    image = Image.new(mode, (canvas.shape[0], canvas.shape[1]))

    for (x, y), _value in np.ndenumerate(canvas):
        if canvas[x][y] == 0:
            rgb = ImageColor.getrgb(get_color_str(get_similar_color(palette[0])))
        else:
            pixel_str = get_color_str(palette[canvas[x][y] % len(palette)])
            rgb = ImageColor.getrgb(pixel_str)

        if mode == "RGBA":
            if layer_canvas is not None:
                pixel_layer = int(layer_canvas[x][y])
                pixel_alpha = 255 if pixel_layer == 0 else alpha
            else:
                pixel_alpha = alpha
            image.putpixel((x, y), rgb + (pixel_alpha,))
        else:
            image.putpixel((x, y), rgb)

    return image


def add_border_to_image(image, border_size=30, color=(255, 255, 255)):
    width = image.size[0]
    height = image.size[1]

    for h in range(0, border_size):
        for w in range(0, width):
            image.putpixel((w, h), (color[0], color[1], color[2]))
            image.putpixel((w, height - (h + 1)), (color[0], color[1], color[2]))

    for h in range(border_size, height - border_size):
        for w in range(0, border_size):
            image.putpixel((w, h), (color[0], color[1], color[2]))
            image.putpixel((width - (w + 1), h), (color[0], color[1], color[2]))
