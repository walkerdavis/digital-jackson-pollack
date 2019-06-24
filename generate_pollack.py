import pollack_functions

from PIL import Image, ImageDraw
import math
from random import randint as rint
from pollack_functions import *

num_splatters = 5000

# painting = jackson_pollack(width, height, len(palette), num_splatters)

# picture = create_pollack_image(canvas=painting,palette=palette)

canvas = jackson_pollack(300, 300, 8, 5000)

picture_random_colors = create_pollack_image(canvas=canvas)

picture_random_colors

picture_random_colors.save('/Users/walkerrdavis/Desktop/random_colors_0.png', "PNG")
