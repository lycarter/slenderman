# slenderman
Finds the slender hull of a given shape.

`input`

![test in](https://github.com/lycarter/slenderman/blob/master/not_slender.png)

`output`

![test out](https://github.com/lycarter/slenderman/blob/master/not_slender_out.png)

## A more complicated example

`input`

![test in 2](https://github.com/lycarter/slenderman/blob/master/slenderman_prepped.png)

`output`

![test out 2](https://github.com/lycarter/slenderman/blob/master/slenderman_out.png)

## Usage

Note that for best results, the input file should be very clean. `slenderman` takes the top left pixel as the "background" color, and pixels with any deviation from that will count as the foreground color.

`python slenderman.py input_file.png output_file.png`

Requirements: [PIL](http://www.pythonware.com/products/pil/), [numpy](http://www.numpy.org/)
