from fractals import translate, rotate, scale, compose
from fractals import render_fractal
from math import sin, cos, pi

r = 0.381966011250105151795413165634361882279690820194237137864
mats = []

for i in range(5):
    theta = (i + 0.25) / 5 * 2 * pi
    x = cos(theta)
    y = sin(theta)
    mats.append(scale(x, y, r))
mats.append(
    compose([
        scale(0,0,r),
        rotate(0,0,pi)
        ])
    )

img = render_fractal(mats, "pentaflake.png", depth=6)
img.show()

