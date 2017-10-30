#!/usr/bin/env python3
from fractals import translate, rotate, scale, compose
from fractals import render_fractal, render_fractal_np
from fractals import Animation
from fractals import flood_fill
from PIL import Image
from math import sin, cos, pi
import math


def koch_curve(x1, y1, x2, y2, theta=pi / 3):
    mats = []
    denom = 2 + 2 * cos(theta)
    mats.append(scale(x1, y1, 1 / denom))
    mats.append(scale(x2, y2, 1 / denom))
    mats.append(
        compose([
            scale(x1, y1, 1 / denom),
            rotate(x1, y1, theta),
            translate((x2 - x1) / denom, (y2 - y1) / denom),
        ]))
    mats.append(
        compose([
            scale(x2, y2, 1 / denom),
            rotate(x2, y2, -theta),
            translate((x1 - x2) / denom, (y1 - y2) / denom),
        ]))
    return mats


# img = render_fractal(koch_curve(-1,-1,1,-1, 85*pi/180), "tmp.png", depth=7)
# img.show()

# sides pointing in
# sides = [
#     [1, -1, 1, 1],
#     [-1, -1, 1, -1],
#     [1, 1, -1, 1],
#     [-1, 1, -1, -1],
# ]

# sides = [
#     # inner diagonals pointing in
#     [0,-1,1,0],
#     [1,0,0,1],
#     [0,1,-1,0],
#     [-1,0,0,-1],
#     # inner diagonals pointing out
#     [1,0,0,-1,],
#     [0,1,1,0,],
#     [-1,0,0,1,],
#     [0,-1,-1,0,],
# ]

sides_pointing_in = [
    # inner diagonals pointing in
    [0, -1, 1, 0],
    [1, 0, 0, 1],
    [0, 1, -1, 0],
    [-1, 0, 0, -1],
]

sides_pointing_out = [
    [1, 0, 0, -1],
    [0, 1, 1, 0],
    [-1, 0, 0, 1],
    [0, -1, -1, 0],
]

curves = [koch_curve(*(x + [pi / 3])) for x in sides_pointing_in]


@Animation
def render_square(theta):
    curves = [koch_curve(*(x + [theta])) for x in sides_pointing_in]
    arr = sum([render_fractal_np(m, width=600) for m in curves])
    img = Image.fromarray(arr)
    return img


mats = koch_curve(-1, -1, 1, -1, 85 * pi / 180)
render_fractal(mats, "von_koch_curve.png", width=3840 * 2, depth=12)

# width = 600
# curves = [
#     koch_curve(*(x + [pi / 2 * 0.92]))
#     for x in (sides_pointing_out + sides_pointing_in)
# ]
# arr = sum([render_fractal_np(m, width=width) for m in curves])
# flood_points = [
#     # (int(width / 2), int(width / 2)),
#     (0, 0),
#     (0, width - 3),
#     (width - 3, 0),
#     (width - 3, width - 3),
# ]
# for x, y in flood_points:
#     flood_fill(arr, x, y, (0, 0, 0), (255, 255, 255))
# img = Image.fromarray(arr)
# img.save("koch_flake.png")

# render_square.run(
#     "koch_squares/koch_square_%06i.png", 100, -pi / 2, pi / 2, loop=True)

# expanding/contracting koch square animation
# if __name__ == '__main__':
#     n_frames = 20
#     for i in range(n_frames):
#         theta = (pi/2 - pi/3) * i/n_frames + pi/3
#         render_square(theta)
#         print(i, theta)

# render_fractal(koch_curve(-1,-1,1,-1), "koch_curve.png", depth=5)

# render a 16/9 aspect ratio koch curve (for a wallpaper)
# theta = 2 * (pi + math.atan(9 / 16))
# mats = koch_curve(-1, -1, 1, -1, theta)
# render_fractal(mats, "koch_curve_16x9.png", width=4 * 1920)
