import random as rand


def get_random_colors(num_colors):
    palette = []
    for _ in range(num_colors + 1):
        color = [
            rand.uniform(0, 360),
            rand.uniform(0, 100),
            rand.uniform(0, 100),
        ]
        palette.append(color)
    return palette


def get_color_str(color_list):
    return f"hsl({color_list[0]},{color_list[1]}%,{color_list[2]}%)"


def get_similar_color(hsl_color):
    color_dif = 0.04
    return [
        hsl_color[0] * rand.uniform(1 - color_dif, 1 + color_dif),
        hsl_color[1] * rand.uniform(1 - color_dif, 1 + color_dif),
        hsl_color[2] * rand.uniform(1 - (color_dif / 2), 1 + (color_dif / 2)),
    ]
