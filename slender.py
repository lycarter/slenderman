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


if __name__ == '__main__':
    if len(sys.argv) < 1:
        print "please provide an input filename"
    input_filename = sys.argv[1]
    output_filename = sys.argv[2] if len(sys.argv) > 2 else input_filename + '.out'

    f = Image.open(input_filename)
    pixels = read_file(f)
