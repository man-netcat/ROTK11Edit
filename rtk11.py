import glob
from constants import *


def parsefile(f):
    # Attributes are marked as [OFFSET];[LENGTH]x[REPETITION]

    # 91;4 YEAR-00-MONTH-01 (Displayed Starting Date)
    f.seek(91)
    year, _, month, _ = f.read(4)
    print(year, month)

    # 95;26: Scenario Name.
    scenname = f.read(26).decode()
    print(scenname)

    # 121;600: Scenario Description.
    f.seek(121)
    tmp = f.read(600).decode()
    print(tmp)

    # 722;42: Force Colours.
    f.seek(722)
    data = f.read(42)
    colours = [
        colour_map[byte] if byte != 0xFF else 0xFFFFFF
        for byte in data
    ]
    print(colours)

    # 931;607x42: Force Descriptions.
    f.seek(931)
    for i in range(42):
        forcedesc = f.read(607).decode()
        print(i, forcedesc)

    # 26426;4 YEAR-00-MONTH-01 (In-Game Starting Date)
    f.seek(26427)
    year, _, month, _ = f.read(4)
    print(year, month)

    # 26438;(1+2)x86 District code + Max HP of cities.
    # Max HP is 2 bytes in little endian
    # 15 Unknown bytes left
    f.seek(26438)
    for i in range(86):
        district = f.read(1)
        maxhp = int.from_bytes(f.read(2), "little")
        print(district, maxhp)
        f.read(15)


def main():
    # for filename in glob.glob("scenario/SCEN*"):
    #     scenfile = open(filename, 'rb')
    #     parsefile(scenfile)

    scenfile = open('scenario/SCEN000.S11', 'rb')
    parsefile(scenfile)


if __name__ == '__main__':
    main()
