import difflib
import filecmp
import os
import shutil

from binary_parser.binary_parser import BinaryParser


def main():
    scen2 = 'scenario/SCEN009.S11'
    db = '/tmp/rtk11.db'
    lyt = 'rtk11.lyt'
    for i in range(8):
        scen1 = f'scenario/SCEN00{i}.S11'
        print(scen1)

        with BinaryParser(lyt) as bp:
            if os.path.exists(db):
                os.remove(db)
            if os.path.exists(scen2):
                os.remove(scen2)
            bp.parse_file(scen1, db)
            shutil.copyfile(scen1, scen2)
            bp.write_back(scen2, db)

        assert filecmp.cmp(scen1, scen2)
    print("All tests passed")


if __name__ == "__main__":
    main()
