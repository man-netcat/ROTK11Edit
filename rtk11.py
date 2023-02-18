import glob
from constants import *
from queries import *
import string
import sqlite3
import os


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


def makedatabase(scenario_filename):
    db_filename = scenario_filename \
        .replace('scenario', 'databases') \
        .replace('.S11', '.db')

    if os.path.exists(db_filename):
        os.remove(db_filename)

    conn = sqlite3.connect(db_filename)

    conn.execute(scenariocreatequery)
    conn.execute(forcescreatequery)
    conn.execute(officercreatequery)
    conn.execute(itemscreatequery)


def parsefile(scenario_filename):
    f = open(scenario_filename, 'rb')
    db_filename = scenario_filename \
        .replace('scenario', 'databases') \
        .replace('.S11', '.db')
    # Create a connection to the database
    conn = sqlite3.connect(db_filename)

    # Attributes are marked as [OFFSET];[LENGTH]x[REPETITION]

    # YEAR-00-MONTH-01 (Displayed Starting Date)
    year, _, month, _ = parsedata(f, 91, [1, 1, 1, 1])

    # Scenario Name
    scenname = parsedata(f, 95, 26)

    # Scenario Description
    scendesc = parsedata(f, 121, 600)
    scenariovalues = (
        parsestr(scenname),
        parsestr(scendesc),
        parseint(year),
        parseint(month)
    )

    conn.execute(scenarioinsertquery, scenariovalues)

    forcedata1 = parsedata(f, 932, [1, 606], 42)
    forcedata2 = parsedata(f, 163799, [1, 1, 2, 1, 3], 42)
    for forceid, (force1, force2) in enumerate(zip(forcedata1, forcedata2)):
        forcedifficulty, forcedesc = force1
        forcecolour, forcedistrictnumber, forceruler, forcebehaviour, _ = force2
        forcesvalues = (
            forceid,
            parseint(forceruler),
            parsestr(forcedesc),
            parseint(forcecolour),
            parseint(forcedistrictnumber),
            parseint(forcedifficulty),
            parseint(forcebehaviour)
        )
        conn.execute(forcesinsertquery, forcesvalues)

    # YEAR-00-MONTH-01 (In-Game Starting Date)
    year, _, month, _ = parsedata(f, 26427, [1, 1, 1, 1])

    # Officer Data+
    # Family Name, Given Name, Portrait id, Sex, Available Date, Birth Date, Death Date, _, Father, Mother, _, Spouse, Sworn Brother, Compatibility Score, Liked Officers
    officerdata = parsedata(f, 28003, [12, 41, 2, 1, 2, 2, 2, 3, 2, 2, 1, 2, 2, 1, 10, 10, 1, 2, 2,
                            1, 1, 2, 1, 2, 6, 5, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 1, 1, 5, 1, 1, 2, 1], 850)
    for officerid, officer in enumerate(officerdata):
        officerfamilyname, officergivenname, officerportrait, officersex, officeravailabledate, officerbirthdate, \
            officerdeathdate, _, officerfather, officermother, _, officerspouse, officerswornbrother, officercompatibility, \
            officerlikedofficers, officerdislikedofficers, officerallegiance, officerlocation, officerservice, \
            officerstatus, officerrank, _, officerloyalty, officerdeeds, officeraffinities, officerstats, officergrowth, _, \
            officerskill, officerdebatestyle, officerloyaltylevel, officerambition, officeruse, officercharacter, officervoice, \
            officertone, officercourtimportance, officerstrategy, officercampaignstyle, officersexmodel, officermodel, \
            officerweaponmodel, officerhorsemodel, _, officerportraitage, officeraction, _, officerdebateability = officer
        officervalues = (
            officerid,
            parsestr(officerfamilyname),
            parsestr(officergivenname),
            parseint(officerportrait),
            parseint(officersex),
            parseint(officeravailabledate),
            parseint(officerbirthdate),
            parseint(officerdeathdate),
            # Values about 2000 are used to signify brotherly bonds whose father is not available in-game
            parseint(officerfather),
            parseint(officermother),
            parseint(officerspouse),
            parseint(officerswornbrother),
            parseint(officercompatibility),
            *[parseint(likedofficer)
              for likedofficer in sliced(officerlikedofficers, 2)],
            *[parseint(dislikedofficer)
              for dislikedofficer in sliced(officerdislikedofficers, 2)],
            parseint(officerallegiance),
            parseint(officerlocation),
            parseint(officerservice),
            parseint(officerstatus),
            parseint(officerrank),
            parseint(officerloyalty),
            parseint(officerdeeds),
            *[affinity for affinity in officeraffinities],
            *[stat for stat in officerstats],
            *[growth for growth in officergrowth],
            parseint(officerskill),
            parseint(officerdebatestyle),
            parseint(officerloyaltylevel),
            parseint(officerambition),
            parseint(officeruse),
            parseint(officercharacter),
            parseint(officervoice),
            parseint(officertone),
            parseint(officercourtimportance),
            parseint(officerstrategy),
            parseint(officercampaignstyle),
            parseint(officersexmodel),
            parseint(officermodel),
            parseint(officerweaponmodel),
            parseint(officerhorsemodel),
            parseint(officerportraitage),
            parseint(officeraction),
            parseint(officerdebateability)
        )
        conn.execute(officerinsertquery, officervalues)

    # Item Data
    itemdata = parsedata(f, 157203, [27, 1, 1, 1, 2, 1, 1], 50)
    for itemid, item in enumerate(itemdata):
        print(itemid)
        itemname, itemtype, itemloyalty, itempicture, itemowner, itemcity, itemowned = item
        itemvalues = (
            itemid,
            parsestr(itemname),
            parseint(itemtype),
            parseint(itemloyalty),
            parseint(itempicture),
            parseint(itemowner),
            parseint(itemcity),
            parseint(itemowned)
        )
        conn.execute(itemsinsertquery, itemvalues)

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

    # District code + Max HP of cities
    # Max HP is 2 bytes in little endian
    # 15 Unknown bytes left
    citydistricthp = parsedata(f, 26438, [1, 2, 15], 42)
    for district, hp, _ in citydistricthp:
        printint(district, hp)

    citycolourdata = parsedata(f, 722, 1, 42)
    citycolours = [parseint(byte) for byte in citycolourdata]
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

    citydistricthp = parsedata(f, 26438, [1, 2, 15], 45)
    for district, hp, _ in citydistricthp:
        printint(district, hp)

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

    countrydata = parsedata(f, 170457, [17, 80, 6], 42)
    for countryid, country in enumerate(countrydata):
        countryname, countrydesc, _ = country
        print(countryid)
        printstr(countryname)
        printstr(countrydesc)
        print()

    conn.commit()


def main():
    for filename in glob.glob("scenario/SCEN*"):
        makedatabase(filename)
        parsefile(filename)

    # filename = 'scenario/SCEN000.S11'
    # makedatabase(filename)
    # parsefile(filename)


if __name__ == '__main__':
    main()
