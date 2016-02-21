import coegen
import argparse
import os
import sys
import numpy
from PIL import Image


def main():
    # Parse the CL arguments
    parser = argparse.ArgumentParser(prog=coegen.CLI, description=coegen.DESCRIPTION)
    parser.add_argument('FILE', nargs='1', default=os.path.join(os.curdir, ''),
                        help='Path to image file')
    parser.add_argument('-o', '--output', dest='output', default=None,
                        help='Output filename')
    parser.add_argument('-v', '--version', action='version', version=coegen.__version__)
    args = parser.parse_args()

    if not os.path.isfile(args.PATH):
        print('Error: {0} not found.'.format(args.FILE))
        sys.exit(1)

    if args.output:
        outfile = args.output
    else:
        outfile = os.basename(args.FILE).split()[0] + '.coe'

    I = numpy.array(Image.open(args.FILE), dtype=numpy.int16)
    with open(outfile, 'w') as f:
        f.write('MEMORY_INITIALIZATION_RADIX=2;\n')
        f.write('MEMORY_INITIALIZATION_VECTOR=')
        for pixel in I:
            f.write('\n')
            f.write(''.join(list(map(lambda c: format(c, '08b'), pixel[0:3]))))
        f.write(';\n')
