import glob
from constants import *


def parsefile(f):
    # Attributes are marked as [OFFSET];[LENGTH]x[REPETITION]

    # YEAR-00-MONTH-01 (Displayed Starting Date)
    # 91;4
    f.seek(91)
    year, _, month, _ = f.read(4)
    print(year, month)

    # Scenario Name.
    # 95;26
    scenname = f.read(26).decode()
    print(scenname)

    # Scenario Description.
    # 121;600
    f.seek(121)
    tmp = f.read(600).decode()
    print(tmp)

    # Force Colours.
    # 722;42
    f.seek(722)
    data = f.read(42)
    colours = [
        colour_map[byte] if byte != 0xFF else 0xFFFFFF
        for byte in data
    ]
    print(colours)

    # Force Descriptions.
    # 931;607x42
    f.seek(931)
    for i in range(42):
        forcedesc = f.read(607).decode()
        print(i, forcedesc)

    # YEAR-00-MONTH-01 (In-Game Starting Date)
    # 26426;4
    f.seek(26427)
    year, _, month, _ = f.read(4)
    print(year, month)

    # District code + Max HP of cities.
    # Max HP is 2 bytes in little endian
    # 15 Unknown bytes left
    # 26438;(1+2)x86
    f.seek(26438)
    for i in range(86):
        district = f.read(1)
        maxhp = int.from_bytes(f.read(2), "little")
        print(i, district, maxhp)
        f.read(15)

    # Officer Data.
    # 28003;152x850
    f.seek(28003)
    for i in range(850):
        officerdata = f.read(152)
        print(i, officerdata)

    # Item Data
    # 157203;152x50
    f.seek(157203)
    for i in range(50):
        officerdata = f.read(34)
        print(i, officerdata)


def main():
    # for filename in glob.glob("scenario/SCEN*"):
    #     scenfile = open(filename, 'rb')
    #     parsefile(scenfile)

    scenfile = open('scenario/SCEN000.S11', 'rb')
    parsefile(scenfile)


if __name__ == '__main__':
    main()
