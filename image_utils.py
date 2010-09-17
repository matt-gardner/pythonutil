#!/usr/bin/env python

from __future__ import division

import Image, ImageChops
import numpy as np
from evilplot import Plot, Histogram
from scipy import signal

def grad_magnitude(image):
    array = image_to_array(image)
    sobelx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    sobely = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    gradx = convolve_2d(array, sobelx, 8)
    grady = convolve_2d(array, sobely, 8)
    arraymag = (gradx**2 + grady**2)**.5
    arraymag = np.frompyfunc(crop, 3, 1)(arraymag, 0., 255.)
    arraymag = scale_array(arraymag, 0, 255)
    return array_to_image(arraymag.astype(np.uint8))


def grad_direction(image):
    array = image_to_array(image)
    sobelx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    sobely = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    gradx = convolve_2d(array, sobelx, 8)
    grady = convolve_2d(array, sobely, 8)
    array_direction = np.arctan2(grady, gradx)
    array_direction = scale_array(array_direction, 0, 255)
    return array_to_image(array_direction.astype(np.uint8))


def laplacian_image(image):
    array = image_to_array(image)
    laplace = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])
    laplacian = scale_array(convolve_2d(array, laplace, 8), 0, 255)
    return array_to_image(laplacian.astype(np.uint8))


def laplacian_array(image):
    array = image_to_array(image)
    laplace = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])
    return convolve_2d(array, laplace, 8)


def color_grad_magnitude(image):
    red, green, blue = image.split()
    red_grad_mag = grad_magnitude(red)
    green_grad_mag = grad_magnitude(green)
    blue_grad_mag = grad_magnitude(blue)
    tmp_image = ImageChops.lighter(red_grad_mag, green_grad_mag)
    return ImageChops.lighter(tmp_image, blue_grad_mag)


def threshold_image(image, value):
    return Image.eval(image, cutoff(value)).convert('1')


def crop(value, low, high):
    return max(low, min(value, high))


def cutoff(value):
    function = lambda x: x if x > value else 0
    return function


def convolve_2d(array, kernel, scale=1):
    result = signal.convolve2d(array, kernel, 'same')
    return result / scale


def scale_image(image, low, high):
    pixelmin, pixelmax = image.getextrema()
    offset = pixelmin-low
    scale = (high-low)/(pixelmax-pixelmin)
    return image.point(lambda i: (i - offset) * scale)


def scale_array(array, low, high):
    minval, maxval = np.min(array), np.max(array)
    offset = minval - low
    scale = (high - low) / (maxval - minval)
    return (array - offset) * scale


def flip_image_indices(i, j, width, height):
    if i < width/2:
        newi = i+width/2
    else:
        newi = i-width/2
    if j < height/2:
        newj = j+height/2
    else:
        newj = j-height/2
    return newi, newj


def bilinear_interpolate(image, x, y):
    width, height = image.size
    x1 = int(x)
    x2 = int(x)+1
    y1 = int(y)
    y2 = int(y)+1
    if x2 > width-1 and y2 > height-1:
        return image.getpixel((x1,y1))
    if y2 > height-1:
        f1 = image.getpixel((x1,y1))
        f2 = image.getpixel((x2,y1))
        return f1+(x-x1)*(f2-f1)/(x2-x1)
    if x2 > width-1:
        f1 = image.getpixel((x1,y1))
        f2 = image.getpixel((x1,y2))
        return f1+(y-y1)*(f2-f1)/(y2-y1)
    denom = (x2-x1)*(y2-y1)
    f11 = image.getpixel((x1,y1))
    f12 = image.getpixel((x1,y2))
    f21 = image.getpixel((x2,y1))
    f22 = image.getpixel((x2,y2))
    result = 0
    result += f11*(x2-x)*(y2-y)
    result += f12*(x2-x)*(y-y1)
    result += f21*(x-x1)*(y2-y)
    result += f11*(x-x1)*(y-y1)
    return result/denom


def create_residual_image_for_display(image, residual):
    width, height = image.size
    for j in range(height):
        for i in range(width):
            pixels = []
            try:
                pixels.append(image.getpixel((i-1,j)))
            except IndexError:
                pass
            try:
                pixels.append(image.getpixel((i-1,j-1)))
            except IndexError:
                pass
            try:
                pixels.append(image.getpixel((i,j-1)))
            except IndexError:
                pass
            try:
                pixels.append(image.getpixel((i+1,j-1)))
            except IndexError:
                pass
            if len(pixels) == 0:
                prediction = 0
            else:
                prediction = sum(pixels)/len(pixels)

            pixel = image.getpixel((i,j))
            r = pixel-prediction+128
            residual.putpixel((i,j),r)


def create_residual_image_for_encoding(image, residual):
    width, height = image.size
    for j in range(height):
        for i in range(width):
            pixels = []
            try:
                pixels.append(image.getpixel((i-1,j)))
            except IndexError:
                pass
            try:
                pixels.append(image.getpixel((i-1,j-1)))
            except IndexError:
                pass
            try:
                pixels.append(image.getpixel((i,j-1)))
            except IndexError:
                pass
            try:
                pixels.append(image.getpixel((i+1,j-1)))
            except IndexError:
                pass
            if len(pixels) == 0:
                prediction = 0
            else:
                prediction = int(sum(pixels)/len(pixels))

            pixel = image.getpixel((i,j))
            r = (pixel-prediction)%256
            residual.putpixel((i,j),r)


def reproduce_image_from_residual(residual, image):
    width, height = residual.size
    print width, height
    for j in range(height):
        for i in range(width):
            pixels = []
            try:
                pixels.append(image.getpixel((i-1,j)))
            except IndexError:
                pass
            try:
                pixels.append(image.getpixel((i-1,j-1)))
            except IndexError:
                pass
            try:
                pixels.append(image.getpixel((i,j-1)))
            except IndexError:
                pass
            try:
                pixels.append(image.getpixel((i+1,j-1)))
            except IndexError:
                pass
            if len(pixels) == 0:
                prediction = 0
            else:
                prediction = int(sum(pixels)/len(pixels))

            r = residual.getpixel((i,j))
            pixel = (prediction+r)%256
            image.putpixel((i,j),pixel)


def make_histogram(image, filename, numbins=32):
    width, height = image.size
    data = []
    for i in range(width):
        for j in range(height):
            pixel = image.getpixel((i,j))
            data.append(pixel)
    p = Plot()
    hist = Histogram(data, numbins)
    p.append(hist)
    p.write(filename)


def image_to_array(im):
    if im.mode not in ("L", "F"):
        raise ValueError, "can only convert single-layer images"
    if im.mode == "L":
        a = np.fromstring(im.tostring(), np.uint8)
    else:
        a = np.fromstring(im.tostring(), np.float32)
    a.shape = im.size[1], im.size[0]
    return a


def array_to_image(a):
    if a.dtype == np.uint8:
        mode = "L"
    elif a.dtype == np.float32 or a.dtype == np.float64:
        mode = "F"
    else:
        raise ValueError, "unsupported image mode"
    return Image.fromstring(mode, (a.shape[1], a.shape[0]), a.tostring())


# vim: et sw=4 sts=4
