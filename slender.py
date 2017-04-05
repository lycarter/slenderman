"""Finds the slender hull of an input image."""

from PIL import Image
import numpy as np
import sys


def read_file(f):
    """Converts a file to array.

    Args:
        f: An image file

    Returns:
        An m x n 2-D array which contains True for filled pixels and False otherwise.
    """
    pix = f.load()
    dims = f.size

    # assume the top-left pixel is empty
    empty = pix[0, 0]
    # print empty
    return [[pix[i,j] != empty for j in range(dims[1])] for i in range(dims[0])]

def dist(p1, p2):
    """2D distance function.

    Args:
        p1: two-element tuple
        p2: two-element tuple

    Returns: the distance from p1 to p2.
    """
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

def add_arc(i, j, slender):
    """Adds the arc from (i,j) to the segment, centered at the two segment ends.

    Args:
        i: coord index 1
        j: coord index 2
        slender: a 2D array of boolean occupancy.

    Returns:
        Nothing, but modifies slender in-place to add the arcs.
    """
    # print('add arc called for (%s, %s)' % (i, j))
    r1 = dist((0, len(slender[0])), (i, j))
    r2 = dist((len(slender), len(slender[-1])), (i, j))
    # print('r1, r2: %s, %s' % (r1, r2))


    for a in range(i, len(slender)):
        if a > r1:
            break
        b = int((r1**2 - a**2)**0.5)
        if b >= len(slender[0]):
            break
        # print("marking (%s, %s) as true" % (a, b))
        slender[a][b] = True

    for a in range(i, -1, -1):
        if (len(slender) - a) > r2:
            break
        b = int((r2**2 - (len(slender) - a)**2)**0.5)
        if b >= len(slender[0]):
            break
        slender[a][b] = True

def waterfall_fill(slender):
    """Fills in all pixels below any true pixels (makes the shape contiguous).

    Args:
        slender: a 2D array of boolean occupancy.

    Returns:
        Nothing, but modifies slender in-place to contiguos-ify it.
    """
    for i in range(len(slender)):
        for j in range(len(slender[i])):
            fill_in = False
            if slender[i][j]:
                fill_in = True
            if fill_in:
                slender[i][j] = True

def convert_rgb(slender):
    """Converts slender true/false pixels to RGB values.

    Args:
        slender: a 2D array of boolean occupancy.

    Returns:
        Nothing, but turns slender into an array with the same dimensions,
    with each True value replaced by a white pixel, and each false value
    replaced with a black pixel.
    """
    print("slender is %s x %s and the inner type is %s" % (len(slender), len(slender[0]), type(slender[0][0])))
    for i in range(len(slender)):
        for j in range(len(slender[i])):
            if slender[i][j]:
                slender[i][j] = 255
            else:
                slender[i][j] = 0

    print("slender is %s x %s and the inner type is %s" % (len(slender), len(slender[0]), type(slender[0][0])))


def slender_hull(pixels):
    """Computes the slender hull of a pixel input.

    Args:
        pixels: a 2D array of boolean occupancy.

    Returns:
        A 2D array of boolean occupancy, stating the slender hull
    """
    slender = [[False for j in range(len(pixels[0]))] for i in range(len(pixels))]
    # print "before add_arc"
    # for col in slender:
        # print col
    for i in range(len(pixels)):
        for j in range(len(pixels[0])):
            if pixels[i][j]:
                add_arc(i, j, slender)
                # print "after add_arc"
                # for col in slender:
                    # print col
                slender[i][j] = True
    waterfall_fill(slender)
    # print "after waterfall fill"
    # for col in slender:
        # print col
    return slender



if __name__ == '__main__':
    if len(sys.argv) < 1:
        print "please provide an input filename"
    input_filename = sys.argv[1]
    output_filename = sys.argv[2] if len(sys.argv) > 2 else input_filename + '.out'

    f = Image.open(input_filename)
    pixels = read_file(f)
    # for col in pixels:
        # print col
    slender_hull(pixels)
    convert_rgb(pixels)
    pixels = np.array(pixels)
    f_out = Image.fromarray(pixels, 'L')
    f_out.save(output_filename)