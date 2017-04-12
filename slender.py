"""Finds the slender hull of an input image."""

from PIL import Image
import numpy as np
import sys


def read_file(f):
    """Converts a file to array.

    Args:
        f: An image file

    Returns:
        An m x n 2-D array which contains True for filled pixels and False
        otherwise.
    """
    pix = f.load()
    dims = f.size

    # assume the top-left pixel is empty, set it as the value to compare against
    empty = pix[0, 0]
    return [[pix[i,j] != empty for j in range(dims[1])] for i in range(dims[0])]

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
    r1 = np.linalg.norm(np.array((0, len(slender[0]))) -
                        np.array((i, j)))
    r2 = np.linalg.norm(np.array((len(slender), len(slender[-1]))) -
                        np.array((i, j)))


    for a in range(i, len(slender)):
        if a > r1:
            break
        b = int((r1**2 - a**2)**0.5)
        if b >= len(slender[0]):
            break
        slender[a][len(slender[0]) - b - 1] = True

    for a in range(i, -1, -1):
        if (len(slender) - a) > r2:
            break
        b = int((r2**2 - (len(slender) - a)**2)**0.5)
        if b >= len(slender[0]):
            break
        slender[a][len(slender[0]) - b - 1] = True

def waterfall_fill(slender):
    """Fills in all pixels below any true pixels (makes the shape contiguous).

    Args:
        slender: a 2D array of boolean occupancy.

    Returns:
        Nothing, but modifies slender in-place to contiguos-ify it.
    """
    for i in range(len(slender)):
        fill_in = False
        for j in range(len(slender[i])):
            if slender[i][j]:
                fill_in = True
            if fill_in:
                slender[i][j] = True

def convert_rgb(slender, out_pixels):
    """Converts slender true/false pixels to RGB values.

    Args:
        slender: a 2D array of boolean occupancy.
        out_pixels: Image.pixels of the output image.

    Returns:
        Nothing, but copies slender values to out_pixels
        (True -> white, False -> black)
    """

    for i in range(len(slender)):
        for j in range(len(slender[i])):
            if slender[i][j]:
                out_pixels[i, j] = (255, 255, 255)
            else:
                out_pixels[i, j] = (0, 0, 0)


def slender_hull(pixels):
    """Computes the slender hull of a pixel input.

    Args:
        pixels: a 2D array of boolean occupancy.

    Returns:
        A 2D array of boolean occupancy, stating the slender hull
    """
    slender = [[False for j in range(len(pixels[0]))] for i in range(len(pixels))]

    for i in range(len(pixels)):
        for j in range(len(pixels[0])):
            if pixels[i][j]:
                add_arc(i, j, slender)
                slender[i][j] = True
    waterfall_fill(slender)
    return slender


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "please provide input and output filenames"
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    f = Image.open(input_filename)
    pixels = read_file(f)
    pixels = slender_hull(pixels)

    img = Image.new('RGB', (len(pixels), len(pixels[0])), "black")
    out_pixels = img.load()
    convert_rgb(pixels, out_pixels)

    img.show()
    img.save(output_filename)