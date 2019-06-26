from art_functions import *
from argparse import ArgumentParser
import os
import datetime

parser = ArgumentParser()

##### exports arguments
parser.add_argument(
    'export_loc',
    help='Directory to write new masterpieces to',
    type=str)

parser.add_argument(
    '--width',
    help='Width of masterpiece',
    type=int,
    default=800)

parser.add_argument(
    '--height',
    help='Height of masterpiece',
    type=int,
    default=482)

parser.add_argument(
    '--colors',
    help='Number of paint colors',
    type=int,
    default=8)

parser.add_argument(
    '--splats',
    help='Number of paint splats',
    type=int,
    default=20)

parser.add_argument(
    '--works',
    help='Number of paint splats',
    type=int,
    default=1)

parser.add_argument(
    '--border',
    help='Add a border?',
    type=str,
    default='')

args = parser.parse_args()

EXPORT_DIR = args.export_loc
W = args.width
H = args.height
COLORS = args.colors
SPLATS = args.splats
WORKS = args.works
BORDER = (args.border != '')


def make_dir(dir_str):
    if not os.path.exists(dir_str):
        os.mkdir(dir_str)


def get_date_time_str():
    a = datetime.datetime.now()
    return str(a.month) + '_' + str(a.day) + '_' + str(a.hour) + '_' + str(
        a.minute) + '_' + str(a.second) + '_' + str(a.microsecond) + '_'


TWOMBLY_DIR = os.path.join(EXPORT_DIR, 'TWOMBLY/')
make_dir(TWOMBLY_DIR)

for i in range(WORKS):
    canvas = cy_twombly(W, H, COLORS, SPLATS)
    picture_random_colors = canvas_to_image(canvas=canvas)

    if BORDER:
        add_border_to_image(picture_random_colors, inplace=True)

    picture_random_colors.save(
        TWOMBLY_DIR + 'TWOMBLY_' + get_date_time_str() + '.png', 'PNG')
