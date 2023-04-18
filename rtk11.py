import glob
import os
from pathlib import Path

from binary_parser.binary_parser import BinaryParser
from constants import *


def main():
    with BinaryParser('rtk11.lyt') as bp:
        for binary_path in glob.glob("scenario/SCEN*"):
            db_name = Path(binary_path).stem
            db_path = f'databases/{db_name}.db'
            if os.path.exists(db_path):
                os.remove(db_path)
            bp.parse_file(binary_path, db_path)


if __name__ == '__main__':
    main()
