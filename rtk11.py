import glob
from pathlib import Path

from binary_parser.binary_parser import BinaryParser
from constants import *
import os


def main():
    with BinaryParser('rtk11.lyt') as bp:
        for filename in glob.glob("scenario/SCEN*"):
            stem = Path(filename).stem
            os.remove(f'databases/{stem}.db')
            bp.parse_file(filename, f'databases/{stem}.db')


if __name__ == '__main__':
    main()
