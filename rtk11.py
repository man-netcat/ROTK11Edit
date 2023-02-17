import glob
from constants import *


def parsedata(f, offset, lengths, repetitions=1, excess=0):
    f.seek(offset)
    if repetitions == 1:
        data = f.read(lengths)
    else:
        data = []
        for _ in range(repetitions):
            data.append(f.read(lengths))
            f.read(excess)
    return data


def parsefile(f):
    # Attributes are marked as [OFFSET];[LENGTH]x[REPETITION]~[EXCESS]

    # YEAR-00-MONTH-01 (Displayed Starting Date)
    # 91;4
    year, _, month, _ = parsedata(f, 91, 4)
    print(year, month)

    # Scenario Name
    # 95;26
    scenname = parsedata(f, 95, 26).decode()
    print(scenname)

    # Scenario Description
    # 121;600
    scendesc = parsedata(f, 121, 600).decode()
    print(scendesc)

    # Force Colours
    # 722;42
    f.seek(722)
    data = parsedata(f, 722, 42)
    colours = [
        colour_map[byte] if byte != 0xFF else 0xFFFFFF
        for byte in data
    ]
    print(colours)

    # Force Descriptions
    # 933;607x42
    forcedescs = parsedata(f, 933, 607, 42)
    for forcedesc in forcedescs:
        print(forcedesc.decode())

    # YEAR-00-MONTH-01 (In-Game Starting Date)
    # 26427;4
    year, _, month, _ = parsedata(f, 26427, 4)
    print(year, month)

    # District code + Max HP of cities
    # Max HP is 2 bytes in little endian
    # 15 Unknown bytes left
    # 26438;(1+2)x86~15
    districthp = parsedata(f, 26438, 3, 86, 15)
    for d, *hpdata in districthp:
        hp = int.from_bytes(hpdata, "little")
        print(d, hp)

    # Officer Data
    # 28003;152x850
    officerdata = parsedata(f, 28003, 152, 850)
    print(officerdata)

    # Item Data
    # 157203;34x50
    itemdata = parsedata(f, 157203, 34, 50)
    print(itemdata)

    # Force Data
    # 160603;68x20
    forcedata = parsedata(f, 160603, 68, 28)
    print(forcedata)


def main():
    # for filename in glob.glob("scenario/SCEN*"):
    #     scenfile = open(filename, 'rb')
    #     parsefile(scenfile)

    scenfile = open('scenario/SCEN000.S11', 'rb')
    parsefile(scenfile)


if __name__ == '__main__':
    main()
