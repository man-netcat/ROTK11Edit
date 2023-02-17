import glob
from constants import *


def parseint(bytes):
    return int.from_bytes(bytes, "little")


def parsestr(bytes):
    return bytes.decode('utf-8').replace('\x00', '')


def parsedata(f, offset, lengths, repetitions=1, excess=0):
    def helper():
        if type(lengths) == int:
            data = f.read(lengths)
        elif type(lengths) == list:
            data = [f.read(length) for length in lengths]
        return data

    f.seek(offset)
    if repetitions == 1:
        return helper()
    else:
        datas = []
        for _ in range(repetitions):
            datas.append(helper())
            f.read(excess)
        return datas


def parsefile(f):
    # Attributes are marked as [OFFSET];[LENGTH]x[REPETITION]~[EXCESS]

    # YEAR-00-MONTH-01 (Displayed Starting Date)
    # 91;1,1,1,1
    year, _, month, _ = parsedata(f, 91, [1, 1, 1, 1])
    print(parseint(year), parseint(month))

    # Scenario Name
    # 95;26
    scenname = parsedata(f, 95, 26)
    print(parsestr(scenname))

    # Scenario Description
    # 121;600
    scendesc = parsedata(f, 121, 600)
    print(parsestr(scendesc))

    # Force Colours
    # 722;1x42
    colourdata = parsedata(f, 722, 1, 42)
    colours = [colour_map[parseint(byte)] for byte in colourdata]
    print(colours)

    # Force Descriptions
    # 933;607x42
    forcedescs = parsedata(f, 933, 607, 42)
    for forcedesc in forcedescs:
        print(parsestr(forcedesc))

    # YEAR-00-MONTH-01 (In-Game Starting Date)
    # 26427;1,1,1,1
    year, _, month, _ = parsedata(f, 26427, [1, 1, 1, 1])
    print(parseint(year), parseint(month))

    # District code + Max HP of cities
    # Max HP is 2 bytes in little endian
    # 15 Unknown bytes left
    # 26438;1,2x86~15
    districthp = parsedata(f, 26438, [1, 2], 86, 15)
    for district, hp in districthp:
        print(parseint(district), parseint(hp))

    # Officer Data
    # Family Name, Given Name, Portrait id, Sex, Available Date, Birth Date, Death Date
    # 28003;12,41,2,1,2,2,2,3,2,2,1,2,80x850
    officerdata = parsedata(
        f, 28003, [12, 41, 2, 1, 2, 2, 2, 3, 2, 2, 1, 2, 2, 1, 77], 850)
    for officerid, officer in enumerate(officerdata):
        print(officerid)
        officerfamilyname, officergivenname, officerportrait, officersex, officeravailabledate, officerbirthdate, officerdeathdate, _, officerparent1, officerparent2, _, officerspouse, officerswornbrother, officercompatibility, _ = officer
        print(
            parsestr(officerfamilyname),
            parsestr(officergivenname)
        )
        print(parseint(officerportrait))
        print(parseint(officersex))
        print(
            parseint(officeravailabledate),
            parseint(officerbirthdate),
            parseint(officerdeathdate)
        )
        print(
            parseint(officerparent1),
            parseint(officerparent2)
        )
        print(parseint(officerspouse))
        print(parseint(officerswornbrother))
        print(parseint(officercompatibility))
        print()

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
