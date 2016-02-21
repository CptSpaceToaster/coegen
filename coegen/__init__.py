"""Package for coegen"""
# System
import sys

__project__ = 'Coegen'
__version__ = '1.0.1'

CLI = 'coegen'
MAIN = 'coegen.main:main'
VERSION = '{0} v{1}'.format(__project__, __version__)
DESCRIPTION = 'Convert image files into a .coe'

MIN_PYTHON_VERSION = 3, 4

if not sys.version_info >= MIN_PYTHON_VERSION:
    exit("Python {}.{}+ is required.".format(*MIN_PYTHON_VERSION))

import logging
logger = logging.getLogger(__name__)

try:
    from . import main
except ImportError:
    pass
