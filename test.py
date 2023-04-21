import difflib
import filecmp
import os
import shutil

from binary_parser.binary_parser import BinaryParser


def main():
    scen1 = 'scenario/SCEN000.s11'
    scen2 = 'scenario/SCEN009.S11'
    db = '/tmp/rtk11.db'
    lyt = 'rtk11.lyt'

    with BinaryParser(lyt) as bp:
        if os.path.exists(db):
            os.remove(db)
        bp.parse_file(scen1, db)
        if os.path.exists(scen2):
            os.remove(scen2)
        shutil.copyfile(scen1, scen2)
        bp.write_back(scen2, db)

        assert filecmp.cmp(scen1, scen2)


if __name__ == "__main__":
    main()
