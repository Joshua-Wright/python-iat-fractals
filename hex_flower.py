from fractals import translate, rotate, scale, compose
from fractals import render_fractal
from math import sin, cos, pi

r = 1/3
mats = []

for i in range(6):
    theta = i / 6 * 2 * pi
    x = cos(theta)
    y = sin(theta)
    mats.append(scale(x, y, 1/3))
mats.append(scale(0,0,r))

img = render_fractal(mats, "hex_flower.png", depth=6, width=1000)
img.show()

