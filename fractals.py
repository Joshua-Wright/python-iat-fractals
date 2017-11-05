#!/usr/bin/env python3
import numpy as np
# import multiprocessing as mp
import pathos.multiprocessing as mp
from functools import reduce
from PIL import Image
from math import sin, cos
import shutil
import numba


def translate(x, y):
    return np.array([
        [1, 0, x],
        [0, 1, y],
        [0, 0, 1],
    ])


def scale(x, y, a):
    return np.array([
        [a, 0, (1 - a) * x],
        [0, a, (1 - a) * y],
        [0, 0, 1],
    ])


def rotate(x, y, theta):
    return np.array([
        [cos(theta), -sin(theta), x + y * sin(theta) - x * cos(theta)],
        [sin(theta),
         cos(theta), y - y * cos(theta) - x * sin(theta)],
        [0, 0, 1],
    ])


def compose(mats):
    # reverse because matrix multiplication goes the wrong way
    return reduce(np.matmul, mats[::-1])


def transform_points(x, y, mats, depth):
    while True:
        # TODO preallocate array
        # newx = np.zeros(len(mats) * len(x))
        # newy = np.zeros(len(mats) * len(y))
        newx = np.zeros(0)
        newy = np.zeros(0)
        for mat in mats:
            newx = np.append(newx, x * mat[0][0] + y * mat[0][1] + mat[0][2])
            newy = np.append(newy, x * mat[1][0] + y * mat[1][1] + mat[1][2])
        if depth == 0:
            return newx, newy
        else:
            depth -= 1
            x = newx
            y = newy


def rasterize_points(x, y, wd, bounds=(-1, 1, -1, 1)):
    # bounds is xmin, xmax, ymin, ymax
    xmin, xmax, ymin, ymax = bounds
    buf = np.zeros((wd, wd, 3)).astype(np.uint8)
    inside = np.logical_and(
        np.logical_and(x >= xmin, x <= xmax),
        #
        np.logical_and(y >= ymin, y <= ymax))
    x = x[inside]
    y = y[inside]
    xi = np.round((x - xmin) / (xmax - xmin) * (wd - 1)).astype(int)
    yi = np.round(wd - 1 - (y - ymin) / (ymax - ymin) * (wd - 1)).astype(int)
    buf[yi, xi, 0] = 255
    buf[yi, xi, 1] = 255
    buf[yi, xi, 2] = 255
    return buf


def render_fractal_np(mats, depth=10, width=800, bounds=(-1, 1, -1, 1)):
    x, y = transform_points(np.array([0]), np.array([0]), mats, depth)
    return rasterize_points(x, y, width, bounds=bounds)


def render_fractal(mats, filename, bounds=(-1, 1, -1, 1), depth=10, width=800):
    x, y = transform_points(np.array([0]), np.array([0]), mats, depth)
    img = Image.fromarray(rasterize_points(x, y, width, bounds=bounds))
    img.save(filename)
    return img


class Animation(object):
    def __init__(self, func):
        self.func = func

    def run(self, filename, n_frames, xmin, xmax, parallel=True, loop=False):
        def frame(i):
            x = xmin + (xmax - xmin) * i / n_frames
            img = self.func(x)
            img.save(filename % i)
            print("rendered frame %i" % i)

        if parallel:
            p = mp.Pool()
            p.map(frame, range(n_frames + 1))
        else:
            map(frame, range(n_frames + 1))
        if loop:
            frame(n_frames)
            for i in range(1, n_frames + 1):
                i0 = n_frames - i
                i1 = n_frames + i
                shutil.copy(filename % i0, filename % i1)


@numba.jit(nopython=True, nogil=True, parallel=True)
def flood_fill(buf, x, y, to_replace, new_val):
    """
    buf: RGB numpy array
    to_replace, new_val: tuple of (r,g,b)
    """
    points = [(int(x), int(y))]
    while points:
        x, y = points.pop()
        for newpoint in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
            if x < 0 or y < 0 or x >= len(buf) or y >= len(buf):
                continue
            if buf[newpoint][0] == to_replace[0] and \
               buf[newpoint][1] == to_replace[1] and \
               buf[newpoint][2] == to_replace[2]:
                points.append(newpoint)
                buf[newpoint] = new_val


def invert_colors(array):
    # TODO handle Image in addition to array
    return 255 - array
