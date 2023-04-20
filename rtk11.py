import glob
import os
from pathlib import Path
import shutil

from binary_parser.binary_parser import BinaryParser
from constants import *


def main():
    with BinaryParser('rtk11.lyt') as bp:
        for binary_path in sorted(glob.glob("scenario/SCEN*")):
            scenario_name = Path(binary_path).stem
            new_binary_path = binary_path.replace(
                scenario_name, f"new_{scenario_name}")
            shutil.copyfile(binary_path, new_binary_path)
            db_path = f'databases/{scenario_name}.db'
            if os.path.exists(db_path):
                os.remove(db_path)
            bp.parse_file(binary_path, db_path)
            # Should result in identical file
            bp.write_back(new_binary_path, db_path)


if __name__ == '__main__':
    main()
