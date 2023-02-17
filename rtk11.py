import glob
from constants import *


def sliced(bytes, n):
    return [bytes[i:i+n] for i in range(0, len(bytes), n)]


def parseint(bytes):
    return int.from_bytes(bytes, "little")


def parsestr(bytes):
    return bytes.decode('utf-8').replace('\x00', '')


def printint(*bytestrings):
    for bytes in bytestrings:
        print(parseint(bytes), end=' ')
    print()


def printstr(*bytestrings):
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
    year, _, month, _ = parsedata(f, 91, [1, 1, 1, 1])
    printint(year, month)

    # Scenario Name
    scenname = parsedata(f, 95, 26)
    printstr(scenname)

    # Scenario Description
    scendesc = parsedata(f, 121, 600)
    printstr(scendesc)

    # Force Colours
    colourdata = parsedata(f, 722, 1, 42)
    colours = [colour_map[parseint(byte)] for byte in colourdata]
    print(colours)

    # Force Descriptions
    forcedescs = parsedata(f, 933, 607, 42)
    for forceid, forcedesc in enumerate(forcedescs):
        print(forceid)
        printstr(forcedesc)

    # YEAR-00-MONTH-01 (In-Game Starting Date)
    year, _, month, _ = parsedata(f, 26427, [1, 1, 1, 1])
    printint(year, month)

    # District code + Max HP of cities
    # Max HP is 2 bytes in little endian
    # 15 Unknown bytes left
    districthp = parsedata(f, 26438, [1, 2, 15], 86)
    for district, hp, _ in districthp:
        printint(district, hp)

    # Officer Data+
    # Family Name, Given Name, Portrait id, Sex, Available Date, Birth Date, Death Date, _, Sarents, _, Spouse, Sworn Brother, Compatibility Score, Liked Officers
    officerdata = parsedata(f, 28003, [12, 41, 2, 1, 2, 2, 2, 3, 4, 1, 2, 2, 1, 10, 10, 1, 2, 2,
                            1, 1, 2, 1, 2, 6, 5, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 1, 1, 5, 1, 1, 2, 1], 850)
    for officerid, officer in enumerate(officerdata):
        print(officerid)
        officerfamilyname, officergivenname, officerportrait, officersex, officeravailabledate, officerbirthdate, \
            officerdeathdate, _, officerparents, _, officerspouse, officerswornbrother, officercompatibility, \
            officerlikedofficers, officerdislikedofficers, officerallegiance, officerlocation, officerservice, \
            officerstatus, officerrank, _, officerloyalty, officerdeeds, officeraffinities, officerstats, officergrowth, _, \
            officerskill, officerdebatestyle, officerloyaltylevel, officerambition, officeruse, officercharacter, officervoice, \
            officertone, officercourtimportance, officerstrategy, officercampaignstyle, officersexmodel, officermodel, \
            officerweaponmodel, officerhorsemodel, _, officerportraitage, officeraction, _, officerdebateability = officer
        printstr(officerfamilyname, officergivenname)
        printint(officerportrait)
        printint(officersex)
        printint(officeravailabledate, officerbirthdate, officerdeathdate)
        printint(*sliced(officerparents, 2))
        printint(officerspouse)
        printint(officerswornbrother)
        printint(officercompatibility)
        printint(*sliced(officerlikedofficers, 2))
        printint(*sliced(officerdislikedofficers, 2))
        print(
            parseint(officerallegiance),
            city_map[parseint(officerlocation)],
            city_map[parseint(officerservice)]
        )
        print(officer_status_map[parseint(officerstatus)])
        print(officer_ranks_map[parseint(officerrank)])
        printint(officerloyalty)
        printint(officerdeeds)
        print(*[affinity_map[byte] for byte in officeraffinities])
        printint(*sliced(officerstats, 1))
        print(*[growth_ability_map[parseint(growth)]
              for growth in sliced(officergrowth, 1)])
        print(skill_map[parseint(officerskill)])
        print(debate_map[parseint(officerdebatestyle)])
        printint(officerloyaltylevel)
        printint(officerambition)
        print(use_map[parseint(officeruse)])
        print(character_map[parseint(officercharacter)])
        print(voice_map[parseint(officervoice)])
        print(tone_map[parseint(officertone)])
        print(court_importance_map[parseint(officercourtimportance)])
        print(strategy_map[parseint(officerstrategy)])
        print(campaign_map[parseint(officercampaignstyle)])
        print(printint(officersexmodel, officermodel,
              officerweaponmodel, officerhorsemodel, officerportraitage))
        print(action_map[parseint(officeraction)])
        printint(officerdebateability)
        print()

    # # Item Data
    # itemdata = parsedata(f, 157203, 34, 50)
    # print(itemdata)

    # # Force Data
    # forcedata = parsedata(f, 160603, 68, 28)
    # print(forcedata)


def main():
    for filename in glob.glob("scenario/SCEN*"):
        scenfile = open(filename, 'rb')
        parsefile(scenfile)

    # scenfile = open('scenario/SCEN000.S11', 'rb')
    # parsefile(scenfile)


if __name__ == '__main__':
    main()
