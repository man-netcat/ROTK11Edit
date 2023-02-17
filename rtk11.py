import glob
from constants import *
import string


def sliced(bytes, n):
    return [bytes[i:i+n] for i in range(0, len(bytes), n)]


def parseint(bytes):
    return int.from_bytes(bytes, "little")


def parsestr(bytes):
    return ''.join([c for c in bytes.decode('utf-8') if c.isalnum() or c.isspace() or c in string.punctuation])


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

    # Item Data
    itemdata = parsedata(f, 157203, [27, 1, 1, 1, 2, 1, 1], 50)
    for itemid, item in enumerate(itemdata):
        print(itemid)
        itemname, itemtype, itemloyalty, itempicture, itemowner, itemcity, itemowned = item
        printstr(itemname)
        print(item_type_map[parseint(itemtype)])
        printint(itemloyalty, itempicture, itemowner, itemowned)
        print(city_map[parseint(itemcity)])
        print()

    # Force Data
    forcedata = parsedata(f, 160603, [2, 2, 42, 5, 1, 1, 1, 2, 8, 4], 42)
    for forceid, force in enumerate(forcedata):
        print(forceid)
        forceleader, forcestrategist, forcerelationships, _, forcetitle, forcecountry, forcecolour, _, forcealliances, forcetechniques = force
        printint(forceleader, forcestrategist)
        print(*[parseint(forcerelationship)
              for forcerelationship in sliced(forcerelationships, 1)])
        print(title_map[parseint(forcetitle)])
        print(country_map[parseint(forcecountry)])
        print(hex(colour_map[parseint(forcecolour)]))
        printint(forcealliances)

        # Pikes, Spears, Horses, Bows, Invention, Command, Fire, Defense
        print(forcetechniques.hex())
        print()

    # Force Data (when starting a game)
    forcedatamainmenu = parsedata(f, 163799, [1, 1, 2, 1, 3], 42)
    for forceid, force in enumerate(forcedatamainmenu):
        print(forceid)
        forcecolour, forcedistrictnumber, forceruler, forcebehaviour, _ = force
        print(colour_map[parseint(forcecolour)])
        printint(forcedistrictnumber)
        printint(forceruler)
        printint(forcebehaviour)
        print()

    citydata = parsedata(f, 164256,
                         [5, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 6, 2, 14, 2, 7, 1, 2, 2, 2, 1, 1, 6], 42)
    for cityid, city in enumerate(citydata):
        _, troops, _, gold, _, food, _, spears, _, pikes, _, bows, _, horses, _, rams, _, towers, _, boats, _, marketrate, revenue, harvest, maxhp, will, order, specialty = city
        print(cityid)
        printint(troops, gold, food, spears, pikes,
                 bows, horses, rams, towers, boats)
        printint(marketrate, revenue, harvest, maxhp, will, order)
        print(specialty.hex())
        print()

    gateportdata = parsedata(f, 167577,
                             [1, 2, 2, 2, 2, 2, 6, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 14, 2, 6, 1, 2], 45)
    for gateportid, gateport in enumerate(gateportdata):
        ownership, troops, _, gold, _, food, _, spears, _, pikes, _, bows, _, horses, _, rams, _, towers, _, boats, _, will, _ = gateport
        print(gateportid)
        printint(ownership)
        printint(troops, gold, food, spears, pikes,
                 bows, horses, rams, towers, boats)
        printint(will)
        print()


def main():
    # for filename in glob.glob("scenario/SCEN*"):
    #     print(filename)
    #     scenfile = open(filename, 'rb')
    #     parsefile(scenfile)

    scenfile = open('scenario/SCEN006.S11', 'rb')
    parsefile(scenfile)


if __name__ == '__main__':
    main()
