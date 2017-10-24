from fractals import translate, rotate, scale
from fractals import render_fractal

sierpinski = [
    scale(-1,-1,0.5),
    scale(0,1,0.5),
    scale(1,-1,0.5),
]


img = render_fractal(sierpinski, "sierpinski.png")
img.show()

