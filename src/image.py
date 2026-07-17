import numpy as np
from PIL import Image

from src.colors import get_random_colors


def _hsl_to_rgb_vectorized(h, s, light):
    """Vectorized HSL to RGB. h: 0-360, s: 0-100, l: 0-100. Returns (r, g, b) each 0-255."""
    h = h / 360.0
    s = s / 100.0
    ll = light / 100.0

    def hue_to_rgb(p, q, t):
        t = t % 1.0
        return np.where(
            t < 1/6, p + (q - p) * 6 * t,
            np.where(
                t < 1/2, q,
                np.where(
                    t < 2/3, p + (q - p) * (2/3 - t) * 6,
                    p
                )
            )
        )

    q = np.where(ll < 0.5, ll * (1 + s), ll + s - ll * s)
    p = 2 * ll - q

    is_gray = s == 0
    r = np.where(is_gray, ll, hue_to_rgb(p, q, h + 1/3))
    g = np.where(is_gray, ll, hue_to_rgb(p, q, h))
    b = np.where(is_gray, ll, hue_to_rgb(p, q, h - 1/3))

    return (np.clip(r * 255, 0, 255).astype(np.uint8),
            np.clip(g * 255, 0, 255).astype(np.uint8),
            np.clip(b * 255, 0, 255).astype(np.uint8))


def canvas_to_image(canvas, palette=None, alpha=255, layer_canvas=None):
    if palette is None:
        palette = get_random_colors(len(np.unique(canvas)))

    mode = "RGBA" if (alpha < 255 or layer_canvas is not None) else "RGB"
    w, h = canvas.shape[0], canvas.shape[1]

    import colorsys
    palette_rgb = []
    for c in palette:
        r, g, b = colorsys.hls_to_rgb(c[0] / 360.0, c[2] / 100.0, c[1] / 100.0)
        palette_rgb.append((int(r * 255), int(g * 255), int(b * 255)))
    palette_rgb = np.array(palette_rgb, dtype=np.uint8)

    color_dif = 0.04
    bg_hsl = np.array(palette[0], dtype=np.float64)
    bg_h = np.clip(bg_hsl[0] * np.random.uniform(1 - color_dif, 1 + color_dif, size=(w, h)), 0, 360)
    bg_s = np.clip(bg_hsl[1] * np.random.uniform(1 - color_dif, 1 + color_dif, size=(w, h)), 0, 100)
    bg_l = np.clip(bg_hsl[2] * np.random.uniform(1 - color_dif / 2, 1 + color_dif / 2, size=(w, h)), 0, 100)

    bg_r, bg_g, bg_b = _hsl_to_rgb_vectorized(bg_h, bg_s, bg_l)

    indices = canvas % len(palette)
    fg_rgb = palette_rgb[indices]

    is_bg = canvas == 0
    pixels = np.stack([
        np.where(is_bg, bg_r, fg_rgb[:, :, 0]),
        np.where(is_bg, bg_g, fg_rgb[:, :, 1]),
        np.where(is_bg, bg_b, fg_rgb[:, :, 2]),
    ], axis=-1).astype(np.uint8)

    if mode == "RGBA":
        if layer_canvas is not None:
            alpha_ch = np.where(layer_canvas == 0, 255, alpha).astype(np.uint8)
        else:
            alpha_ch = np.full((w, h), alpha, dtype=np.uint8)
        pixels = np.concatenate([pixels, alpha_ch[:, :, np.newaxis]], axis=-1)

    image = Image.fromarray(pixels.transpose(1, 0, 2), mode)

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
