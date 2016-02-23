import coegen
import argparse
import os
import sys
import numpy
from PIL import Image


def main():
    # Parse the CL arguments
    parser = argparse.ArgumentParser(prog=coegen.CLI, description=coegen.DESCRIPTION)
    parser.add_argument('FILE', help='Path to image file')
    parser.add_argument('-o', '--output', dest='output', default=None,
                        help='Output filename')
    parser.add_argument('-f', '--format', dest='format', default='01x',
                        help='Pixel format (default="01x"), try "04b"')
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
    I = numpy.array(Image.open(args.FILE), dtype=numpy.uint8)
    print('writing {0}'.format(outfile))

    """
    iteration happens like this
      ---------->
     | 1 2 3 4 5
     | 6 7 8 9 10

    """
    with open(outfile, 'w') as f:
        if args.format in ['04b', '01x']:
            f.write('MEMORY_INITIALIZATION_RADIX=16;\n')
        elif args.format in ['01b']:
            f.write('MEMORY_INITIALIZATION_RADIX=2;\n')
        else:
            print('Error: Format not recognized: {0}'.format(args.format))
            sys.exit(1)

        f.write('MEMORY_INITIALIZATION_VECTOR=')
        for row in I:
            f.write('\n')
            # Assume full alpha
            if args.format in ['04b', '01x']:
                f.write(''.join(map(lambda pixel: ''.join(map(lambda c: format(c >> 4, args.format), pixel[0:4])), row)))
            elif args.format in ['01b']:
                f.write(''.join(map(lambda pixel: ''.join(map(lambda c: format(c >> 7, args.format), pixel[0:4])), row)))
        f.write(';\n')
