import filecmp
import os
import shutil

from binary_parser.binary_parser import BinaryParser


def main():
    newscen = 'scenario/SCEN009.S11'
    db = '/tmp/rtk11.db'
    lyt = 'rtk11.lyt'
    for i in range(8):
        oldscen = f'scenario/SCEN00{i}.S11'

        with BinaryParser(lyt, encoding='shift-jis') as bp:
            if os.path.exists(db):
                os.remove(db)
            if os.path.exists(newscen):
                os.remove(newscen)
            bp.parse_file(oldscen, db)
            shutil.copyfile(oldscen, newscen)
            bp.write_back(newscen, db)

        assert filecmp.cmp(oldscen, newscen)
    print("All tests passed")


if __name__ == "__main__":
    main()
