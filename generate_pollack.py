from a_art_functions import *
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
    default=2000)

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

parser.add_argument(
    '--gif',
    help='Export images of individual splats to gif-ify',
    type=str,
    default='')


args = parser.parse_args()

EXPORT_DIR = args.export_loc
W = args.width
H = args.height
COLORS =args.colors
SPLATS = args.splats
WORKS = args.works
BORDER = (args.border != '')
GIF = (args.gif != '')

if GIF:
    WORKS = 1

def make_dir(dir_str):
    if not os.path.exists(dir_str):
        os.mkdir(dir_str)

def get_date_time_str():
    a = datetime.datetime.now()
    return str(a.month) + '_' + str(a.day) + '_' + str(a.hour) + '_' + str(
        a.minute) + '_' + str(a.second) + '_' + str(a.microsecond) + '_'

POLLACK_DIR = os.path.join(EXPORT_DIR, 'POLLACK/')
make_dir(POLLACK_DIR)


if not GIF:
    for i in range(WORKS):
        canvas = jackson_pollack(W, H, COLORS, SPLATS)
        picture_random_colors = canvas_to_image(canvas=canvas)

        if BORDER:
            add_border_to_image(picture_random_colors, inplace=True)

        picture_random_colors.save(
            POLLACK_DIR + 'POLLACK_' + get_date_time_str() + '.png', 'PNG')

else:
    CANVAS = np.zeros((W, H),dtype=int)
    PALETTE = get_random_colors(COLORS)

    for i in range(SPLATS):

        num_str = '00000'
        i_len = len(str(i))
        num_str = num_str[:-i_len]
        num_str += str(i)

        x0 = rand.randint(0, W - 1)
        y0 = rand.randint(0, H - 1)
        x1 = rand.randint(0, W - 1)
        y1 = rand.randint(0, H - 1)

        color = rand.uniform(1, COLORS)
        paint_line(CANVAS, x0, y0, x1, y1, color)
        temp_canvas = canvas_to_image(CANVAS,PALETTE)
        temp_canvas.save(POLLACK_DIR + 'POLLACK_' +
                         num_str + '.png', 'PNG')
