# digital-jackson-pollack
## Generate digital pixel splatters with Python and [Pillow](https://github.com/python-pillow/Pillow)(Python Image Library)

## ![alt text](/masterpieces/convergence.png)

### Using Pillow, you can generate digital images inspired by Jackson Pollack.  I chose to imitate Jackon Pollack's 1952 *Convergence* because I like the colors, seemed like a good place to start.  

### This jupyter notebook will show you how to create a painting(really a [NumPy](http://www.numpy.org) array), specify your colors, add a border to the image if you'd like, and then save to a .png format.

### Recently added: Generate Cy Twombly inspired pieces.
### ![alt text](/masterpieces/TWOMBLY_6_27_23_6_25_149273_.png) 

### You can also generate canvases with random color combinations.

### ![alt text](/masterpieces/random_colors_0.png)      ![alt text](/masterpieces/random_colors_2.png)
### ![alt text](/masterpieces/random_colors_4.png)      ![alt text](/masterpieces/random_colors_5.png)

### And make gif's using my other [repo](https://github.com/walkerdavis/producerpy)'s [giffer.py](https://github.com/walkerdavis/producerpy/blob/master/giffer.py) script.

### ![alt text](/masterpieces/POLLACK_gif.gif)

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/walkerdavis/digital-jackson-pollack.git
cd digital-jackson-pollack
```

### 2. Create and activate virtual environment using uv
```bash
uv venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
uv pip install -r requirements.txt
```

## Make some art!

### Generate Jackson Pollack-style masterpieces

Basic usage:
```bash
python generate_pollack.py ./masterpieces
```

With custom options:
```bash
# Custom width, height, and number of colors
python generate_pollack.py ./masterpieces --width 1200 --height 800 --colors 10

# More splats for denser art
python generate_pollack.py ./masterpieces --splats 3000

# Apply splats in multiple layers for more depth (automatically enables transparency)
python generate_pollack.py ./masterpieces --layers 5

# Create semi-transparent art with custom alpha channel
python generate_pollack.py ./masterpieces --alpha 180

# Combine layers with custom transparency
python generate_pollack.py ./masterpieces --layers 3 --alpha 150

# Generate multiple works at once
python generate_pollack.py ./masterpieces --works 5

# Add a border
python generate_pollack.py ./masterpieces --border yes
```

### Generate Cy Twombly-style pieces

Basic usage:
```bash
python generate_twombly.py ./masterpieces
```

With custom options:
```bash
# Custom dimensions and colors
python generate_twombly.py ./masterpieces --width 1000 --height 600 --colors 5

# More lines for denser art  
python generate_twombly.py ./masterpieces --lines 150

# Generate multiple works
python generate_twombly.py ./masterpieces --works 3
```

### Generate tvOS App Icon Assets

Generate Pollack art that conforms to Apple's tvOS icon requirements with automatic validation:

```bash
# App Icon 2x (1200x720) - default
python generate_pollack_tvos.py ./masterpieces

# App Icon 1x (400x240)
python generate_pollack_tvos.py ./masterpieces --preset app_icon_1x

# Top Shelf Wide (1920x720)
python generate_pollack_tvos.py ./masterpieces --preset top_shelf_wide

# Top Shelf Standard (1920x440)
python generate_pollack_tvos.py ./masterpieces --preset top_shelf_std
```

With custom options:
```bash
# Multiple layered images with transparency
python generate_pollack_tvos.py ./masterpieces --preset app_icon_2x --layers 4 --works 5

# Custom colors and splats
python generate_pollack_tvos.py ./masterpieces --preset top_shelf_wide --colors 12 --splats 3000
```

**tvOS Presets:**
- `app_icon_2x` - App Icon (2x scale): 1200x720px
- `app_icon_1x` - App Icon (1x scale): 400x240px
- `top_shelf_wide` - Top Shelf Image (wide): 1920x720px
- `top_shelf_std` - Top Shelf Image (standard): 1920x440px

Each image is automatically validated after creation to ensure it meets all tvOS requirements.

### Available Options

**generate_pollack.py:**
- `export_loc` - Directory to save images (required)
- `--width` - Width of image in pixels (default: 300)
- `--height` - Height of image in pixels (default: 300)
- `--colors` - Number of paint colors (default: 8)
- `--splats` - Number of paint splats (default: 2000)
- `--layers` - Number of layers/passes to apply splats in; automatically enables transparency (default: 1)
- `--alpha` - Alpha transparency value, 0=fully transparent, 255=opaque (default: 255, or 200 when layers > 1)
- `--works` - Number of images to generate (default: 1)
- `--border` - Add border to image (default: '')

**generate_twombly.py:**
- `export_loc` - Directory to save images (required)
- `--width` - Width of image in pixels (default: 800)
- `--height` - Height of image in pixels (default: 482)
- `--colors` - Number of paint colors (default: 8)
- `--lines` - Number of lines to draw (default: 100)
- `--works` - Number of images to generate (default: 1)

**generate_pollack_tvos.py:**
- `export_loc` - Directory to save images (required)
- `--preset` - tvOS icon preset to use (default: app_icon_2x)
  - `app_icon_2x` - App Icon 2x scale (1200x720)
  - `app_icon_1x` - App Icon 1x scale (400x240)
  - `top_shelf_wide` - Top Shelf Wide (1920x720)
  - `top_shelf_std` - Top Shelf Standard (1920x440)
- `--colors` - Number of paint colors (default: 8)
- `--splats` - Number of paint splats (default: 2000)
- `--layers` - Number of layers/passes to apply splats in (default: 1)
- `--alpha` - Alpha transparency value, 0=fully transparent, 255=opaque (default: 255, or 200 when layers > 1)
- `--works` - Number of images to generate (default: 1)
- `--border` - Add border to image (default: '')

Images are automatically validated to ensure conformance to Apple tvOS requirements.

### Lots of future ideas brewing, stayed tuned.


### The pollack_RUNT directory contains the original project I made this for, using the [RUNT](https://github.com/MuvikLabs/runt) and [Pixku](https://github.com/MuvikLabs/Pixku) languages by my friends at [Muvik Labs](https://muviklabs.github.io).  To run anything in this directory, you will need to install and run RUNT by following the instructions on that repo's README.

### Enjoy.