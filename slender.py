"""Finds the slender hull of an input image."""

from PIL import Image
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
    pass

def waterfall_fill(slender):
    """Fills in all pixels below any true pixels (makes the shape contiguous).

    Args:
        slender: a 2D array of boolean occupancy.

    Returns:
        Nothing, but modifies slender in-place to contiguos-ify it.
    """
    pass

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
    waterfall_fill(slender)
    return slender



if __name__ == '__main__':
    if len(sys.argv) < 1:
        print "please provide an input filename"
    input_filename = sys.argv[1]
    output_filename = sys.argv[2] if len(sys.argv) > 2 else input_filename + '.out'

    f = Image.open(input_filename)
    pixels = read_file(f)
    slender_hull(pixels)