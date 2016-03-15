import coegen
import argparse
import os
import sys
from PIL import Image
from collections import OrderedDict


def main():
    # Parse the CL arguments
    parser = argparse.ArgumentParser(prog=coegen.CLI, description=coegen.DESCRIPTION)
    parser.add_argument('FILE', help='Path to image file')
    parser.add_argument('-o', '--output', dest='output', default=None,
                        help='Output filename')
    parser.add_argument('-v', '--version', action='version', version=coegen.__version__)
    args = parser.parse_args()

    if not os.path.isfile(args.FILE):
        print('Error: {0} not found.'.format(args.FILE))
        sys.exit(1)

    if args.output:
        outfile = args.output
    else:
        outfile = os.path.basename(args.FILE).split('.')[0] + '.coe'

    print('reading {0}'.format(args.FILE))
    I = Image.open(args.FILE)
    # Create a color LUT
    LUT = OrderedDict()
    # Count the number of unique colors, while creating a lookup table
    colors = I.getcolors()
    uniq = len(colors)
    if uniq <= 0:
        print('Error: no colors were detected. Please use images with colors?')
        sys.exit(1)
    if uniq > 0:
        radix = 2
        vformat = "01b"
    if uniq > 2:
        radix = 16
        vformat = "01x"
    if uniq > 16:
        radix = 10
        vformat = "08x"
    if uniq > 4294967296:
        print('Error: too many colors detected. Please use an image with less than 4294967296 (2^32) colors')
        sys.exit(1)

    uniq = 0
    for _, color in reversed(colors):
        LUT[color] = uniq
        uniq += 1

    print('selecting radix: {0}'.format(radix))
    print('writing {0}'.format(outfile))

    """
    iteration happens like this
      ---------->
     | 1 2 3 4 5
     | 6 7 8 9 10

    """
    with open(outfile, 'w') as f:
        f.write('MEMORY_INITIALIZATION_RADIX={0};\nMEMORY_INITIALIZATION_VECTOR='.format(radix))
        idx = 0
        for pixel in I.getdata():
            if (idx % I.width == 0):
                f.write('\n')
            f.write(format(LUT[pixel], vformat))
            idx += 1
            if (radix == 10 and idx != I.width*I.height):
                f.write(',')
        f.write(';\n')
    print('complete')
    print('------------')
    print('colors used:')
    for key, value in LUT.items():
        print('  {value}: #{r}{g}{b}'.format(value=format(value, vformat),
                                             r=format(key[0], '02x'),
                                             g=format(key[1], '02x'),
                                             b=format(key[2], '02x')))
