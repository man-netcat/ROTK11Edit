import glob
from constants import *


def sliced(bytes, n):
    return [bytes[i:i+n] for i in range(0, len(bytes), n)]


def parseint(bytes):
    return int.from_bytes(bytes, "little")


def parsestr(bytes):
    return bytes.decode('utf-8').replace('\x00', '')


def printints(*bytestrings):
    for bytes in bytestrings:
        print(parseint(bytes), end=' ')
    print()


def printstrs(*bytestrings):
    for bytes in bytestrings:
        print(parsestr(bytes), end=' ')
    print()


def parsedata(f, offset, lengths, repetitions=1):
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
        return [helper() for _ in range(repetitions)]


def parsefile(f):
    # Attributes are marked as [OFFSET];[LENGTH]x[REPETITION]

    # YEAR-00-MONTH-01 (Displayed Starting Date)
    # 91;1,1,1,1
    year, _, month, _ = parsedata(f, 91, [1, 1, 1, 1])
    printints(year, month)

    # Scenario Name
    # 95;26
    scenname = parsedata(f, 95, 26)
    printstrs(scenname)

    # Scenario Description
    # 121;600
    scendesc = parsedata(f, 121, 600)
    printstrs(scendesc)

    # Force Colours
    # 722;1x42
    colourdata = parsedata(f, 722, 1, 42)
    colours = [colour_map[parseint(byte)] for byte in colourdata]
    print(colours)

    # Force Descriptions
    # 933;607x42
    forcedescs = parsedata(f, 933, 607, 42)
    for forceid, forcedesc in enumerate(forcedescs):
        print(forceid)
        printstrs(forcedesc)

    # YEAR-00-MONTH-01 (In-Game Starting Date)
    # 26427;1,1,1,1
    year, _, month, _ = parsedata(f, 26427, [1, 1, 1, 1])
    printints(year, month)

    # District code + Max HP of cities
    # Max HP is 2 bytes in little endian
    # 15 Unknown bytes left
    # 26438;1,2,15x86
    districthp = parsedata(f, 26438, [1, 2, 15], 86)
    for district, hp, _ in districthp:
        printints(district, hp)

    # Officer Data
    # Family Name, Given Name, Portrait id, Sex, Available Date, Birth Date, Death Date, _, Sarents, _, Spouse, Sworn Brother, Compatibility Score, Liked Officers
    # 28003;12,41,2,1,2,2,2,3,4,1,2,80x850
    officerdata = parsedata(
        f, 28003, [12, 41, 2, 1, 2, 2, 2, 3, 4, 1, 2, 2, 1, 10, 10, 57], 850)
    for officerid, officer in enumerate(officerdata):
        print(officerid)
        officerfamilyname, officergivenname, officerportrait, officersex, officeravailabledate, officerbirthdate, officerdeathdate, _, officerparents, _, officerspouse, officerswornbrother, officercompatibility, officerlikedofficers, officerdislikedofficers, _ = officer
        printstrs(officerfamilyname, officergivenname)
        printints(officerportrait)
        printints(officersex)
        printints(officeravailabledate, officerbirthdate, officerdeathdate)
        printints(*sliced(officerparents, 2))
        printints(officerspouse)
        printints(officerswornbrother)
        printints(officercompatibility)
        printints(*sliced(officerlikedofficers, 2))
        printints(*sliced(officerdislikedofficers, 2))
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
