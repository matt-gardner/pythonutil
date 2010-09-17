#!/usr/bin/env python

from __future__ import division

import Image, ImageFilter, ImageChops
import numpy as np
from evilplot import Plot, Histogram
from math import cos, sin, sqrt
from scipy import signal

def mask_image(image, new_image, mask):
    width, height = image.size
    mw, mh = mask.shape
    for i in range(width):
        for j in range(height):
            newpixel = 0
            for x in range(-int((mw-1)/2),int((mw-1)/2+1)):
                for y in range(-int((mh-1)/2),int((mh-1)/2+1)):
                    if i+x > 0 and j+y > 0 and i+x < width and j+y < height:
                        newpixel += image.getpixel((i+x,j+y))\
                            *mask[x+(mw+1)/2-1,y+(mh+1)/2-1]
            new_image.putpixel((i,j),newpixel)


def mask_image_and_scale(image, new_image, mask, low, high):
    width, height = image.size
    mw, mh = mask.shape
    pixelmin = float('inf')
    pixelmax = -float('inf')
    for i in range(width):
        for j in range(height):
            newpixel = 0
            for x in range(-int((mw-1)/2),int((mw-1)/2+1)):
                for y in range(-int((mh-1)/2),int((mh-1)/2+1)):
                    if i+x > 0 and j+y > 0 and i+x < width and j+y < height:
                        newpixel += image.getpixel((i+x,j+y))\
                            *mask[x+(mw+1)/2-1,y+(mh+1)/2-1]
            if newpixel < pixelmin:
                pixelmin = newpixel
            if newpixel > pixelmax:
                pixelmax = newpixel
    offset = pixelmin-low
    scale = (high-low)/(pixelmax-pixelmin)
    print high, low
    print pixelmin, pixelmax
    print offset, scale
    for i in range(width):
        for j in range(height):
            newpixel = 0
            for x in range(-int((mw-1)/2),int((mw-1)/2+1)):
                for y in range(-int((mh-1)/2),int((mh-1)/2+1)):
                    if i+x > 0 and j+y > 0 and i+x < width and j+y < height:
                        newpixel += image.getpixel((i+x,j+y))\
                            *mask[x+(mw+1)/2-1,y+(mh+1)/2-1]
            new_image.putpixel((i,j),(newpixel-offset)*scale)


def two_image_mask_and_operation(image1, image2, new_image, mask, operation):
    width, height = image.size
    mw, mh = mask.shape
    for i in range(width):
        for j in range(height):
            newpixel1 = 0
            newpixel2 = 0
            for x in range(-int((mw-1)/2),int((mw-1)/2+1)):
                for y in range(-int((mh-1)/2),int((mh-1)/2+1)):
                    if i+x > 0 and j+y > 0 and i+x < width and j+y < height:
                        newpixel1 += image1.getpixel((i+x,j+y))\
                            *mask[x+(mw+1)/2-1,y+(mh+1)/2-1]
                        newpixel2 += image2.getpixel((i+x,j+y))\
                            *mask[x+(mw+1)/2-1,y+(mh+1)/2-1]
            new_image.putpixel((i,j),operation(newpixel1,
                newpixel2))


def two_masks_and_operation(image, mask1, mask2, new_image, operation):
    width, height = image.size
    mw, mh = mask1.shape
    for i in range(width):
        for j in range(height):
            newpixel1 = 0
            newpixel2 = 0
            for x in range(-int((mw-1)/2),int((mw-1)/2+1)):
                for y in range(-int((mh-1)/2),int((mh-1)/2+1)):
                    if i+x > 0 and j+y > 0 and i+x < width and j+y < height:
                        newpixel1 += image.getpixel((i+x,j+y))\
                            *mask1[x+(mw+1)/2-1,y+(mh+1)/2-1]
                        newpixel2 += image.getpixel((i+x,j+y))\
                            *mask2[x+(mw+1)/2-1,y+(mh+1)/2-1]
            new_image.putpixel((i,j),operation(newpixel1,
                newpixel2))


def grad_magnitude_slow(image):
    mask1 = np.ones((3,3))
    mask1[0,0] = -1
    mask1[0,1] = 0
    mask1[0,2] = 1
    mask1[1,0] = -2
    mask1[1,1] = 0
    mask1[1,2] = 2
    mask1[2,0] = -1
    mask1[2,1] = 0
    mask1[2,2] = 1
    mask1 = mask1/8;
    mask2 = np.ones((3,3))
    mask2[0,0] = -1
    mask2[0,1] = -2
    mask2[0,2] = -1
    mask2[1,0] = 0
    mask2[1,1] = 0
    mask2[1,2] = 0
    mask2[2,0] = 1
    mask2[2,1] = 2
    mask2[2,2] = 1
    mask2 = mask2/8;
    def magnitude(p1, p2):
        return sqrt(p1**2+p2**2)
    grad_mag = Image.new('L', image.size)
    two_masks_and_operation(image, mask1, mask2, grad_mag, magnitude)
    return scale_image(grad_mag, 0, 255)


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


def median_mask(image, new_image, mask):
    width, height = image.size
    mw, mh = mask.shape
    for i in range(width):
        for j in range(height):
            pixels = []
            for x in range(-int((mw-1)/2),int((mw-1)/2+1)):
                for y in range(-int((mh-1)/2),int((mh-1)/2+1)):
                    if i+x > 0 and j+y > 0 and i+x < width and j+y < height:
                        pixels.append(image.getpixel((i+x,j+y)))
            pixels.sort()
            new_image.putpixel((i,j),pixels[int(len(pixels)/2)])


def scale_image(image, low, high):
    pixelmin, pixelmax = image.getextrema()
    offset = pixelmin-low
    scale = (high-low)/(pixelmax-pixelmin)
    return image.point(lambda i: i * scale + offset)


def scale_array(array, low, high):
    minval, maxval = np.min(array), np.max(array)
    offset = minval - low
    scale = (high - low) / (maxval - minval)
    return array * scale - offset


def scale_array_to_image(array, newimage, low=0, high=255):
    width, height = newimage.size
    pixelmin = float('inf')
    pixelmax = -float('inf')
    for i in range(width):
        for j in range(height):
            val = array[i,j]
            if val < pixelmin:
                pixelmin = val
            if val > pixelmax:
                pixelmax = val
    offset = pixelmin-low
    scale = (high-low)/(pixelmax-pixelmin)
    for i in range(width):
        for j in range(height):
            newimage.putpixel((i,j),(array[i,j]-offset)*scale)


def two_image_operation(image1, image2, newimage, operation):
    width, height = newimage.size
    for i in range(width):
        for j in range(height):
            newimage.putpixel((i,j),operation(image1.getpixel((i,j)),
                image2.getpixel((i,j))))


def invert_image(image1, newimage, maxpixelval=255):
    width, height = image1.size
    for i in range(width):
        for j in range(height):
            newimage.putpixel((i,j),maxpixelval-image1.getpixel((i,j)))


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


def resize_image(image, factor):
    width, height = image.size
    newwidth = int(width*factor)
    newheight = int(height*factor)
    newimage = Image.new(image.mode, (newwidth, newheight))
    def coords(x,y):
        return x/factor, y/factor
    for i in range(newwidth):
        for j in range(newheight):
            newimage.putpixel((i,j), bilinear_interpolate(image, *coords(i,j)))
    return newimage


def rotate_image(image, angle, maxlength=None):
    width, height = image.size
    xc = int(width/2)
    yc = int(height/2)
    if maxlength is not None:
        newwidth = int(maxlength)
        newheight = int(maxlength)
        xcdiff = int(newwidth/2) - xc
        ycdiff = int(newheight/2) - yc
    else:
        newwidth = width
        newheight = height
        xcdiff = 0
        ycdiff = 0
    newimage = Image.new(image.mode, (newwidth,newheight))
    def coords(x,y):
        tmpx = x-xcdiff
        tmpy = y-ycdiff
        newx = (tmpx-xc)*cos(angle)+(tmpy-yc)*sin(angle)+xc
        newy = (xc-tmpx)*sin(angle)+(tmpy-yc)*cos(angle)+yc
        return newx, newy
    for i in range(newwidth):
        for j in range(newheight):
            try:
                value = bilinear_interpolate(image, *coords(i,j))
            except IndexError:
                value = 255
            newimage.putpixel((i,j),value)
    return newimage


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
