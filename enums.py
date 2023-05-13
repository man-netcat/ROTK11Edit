from enum import Enum


class Version(Enum):
    PCEN = 0
    PCPUK = 1
    PS2EN = 2
    PS2PUK = 3

    def __index__(self):
        return self.value


class Scenario(Enum):
    ID = 0
    NUMBER = 1
    YEAR = 2
    MONTH = 3
    UNKNOWN = 4
    NAME = 5
    DESCRIPTION = 6
    INGAMEYEAR = 7
    INGAMEMONTH = 8
    UNKNOWN2 = 9
    EMPEROR = 10
    GAMEMODE = 11

    def __index__(self):
        return self.value


class Force(Enum):
    ID = 0
    DIFFICULTY = 1
    DESCRIPTION = 2
    RULER = 3
    STRATEGIST = 4
    RELATIONSHIP1 = 5
    RELATIONSHIP2 = 6
    RELATIONSHIP3 = 7
    RELATIONSHIP4 = 8
    RELATIONSHIP5 = 9
    RELATIONSHIP6 = 10
    RELATIONSHIP7 = 11
    RELATIONSHIP8 = 12
    RELATIONSHIP9 = 13
    RELATIONSHIP10 = 14
    RELATIONSHIP11 = 15
    RELATIONSHIP12 = 16
    RELATIONSHIP13 = 17
    RELATIONSHIP14 = 18
    RELATIONSHIP15 = 19
    RELATIONSHIP16 = 20
    RELATIONSHIP17 = 21
    RELATIONSHIP18 = 22
    RELATIONSHIP19 = 23
    RELATIONSHIP20 = 24
    RELATIONSHIP21 = 25
    RELATIONSHIP22 = 26
    RELATIONSHIP23 = 27
    RELATIONSHIP24 = 28
    RELATIONSHIP25 = 29
    RELATIONSHIP26 = 30
    RELATIONSHIP27 = 31
    RELATIONSHIP28 = 32
    RELATIONSHIP29 = 33
    RELATIONSHIP30 = 34
    RELATIONSHIP31 = 35
    RELATIONSHIP32 = 36
    RELATIONSHIP33 = 37
    RELATIONSHIP34 = 38
    RELATIONSHIP35 = 39
    RELATIONSHIP36 = 40
    RELATIONSHIP37 = 41
    RELATIONSHIP38 = 42
    RELATIONSHIP39 = 43
    RELATIONSHIP40 = 44
    RELATIONSHIP41 = 45
    RELATIONSHIP42 = 46
    RELATIONSHIPQIANG = 47
    RELATIONSHIPSHANYUE = 48
    RELATIONSHIPWHUHUAN = 49
    RELATIONSHIPNANMAN = 50
    RELATIONSHIPBANDITS = 51
    TITLE = 52
    COUNTRY = 53
    COLOUR = 54
    GOAL = 55
    ALLIANCE = 56
    RESEARCH = 57
    UNKNOWN = 58

    def __index__(self):
        return self.value


class Officer(Enum):
    ID = 0
    FAMILYNAME = 1
    GIVENNAME = 2
    PORTRAIT = 3
    SEX = 4
    AVAILABLEDATE = 5
    BIRTHDATE = 6
    DEATHDATE = 7
    DEATH = 8
    CLAN = 9
    FATHER = 10
    MOTHER = 11
    GENERATION = 12
    SPOUSE = 13
    SWORNBROTHER = 14
    COMPATIBILITY = 15
    LIKEDOFFICER1 = 16
    LIKEDOFFICER2 = 17
    LIKEDOFFICER3 = 18
    LIKEDOFFICER4 = 19
    LIKEDOFFICER5 = 20
    DISLIKEDOFFICER1 = 21
    DISLIKEDOFFICER2 = 22
    DISLIKEDOFFICER3 = 23
    DISLIKEDOFFICER4 = 24
    DISLIKEDOFFICER5 = 25
    ALLEGIANCE = 26
    SERVICE = 27
    LOCATION = 28
    STATUS = 29
    RANK = 30
    DEPENDENCE = 31
    LOYALTY = 32
    DEEDS = 33
    SPEARAFFINITY = 34
    PIKEAFFINITY = 35
    BOWAFFINITY = 36
    CAVALRYAFFINITY = 37
    SIEGEAFFINITY = 38
    NAVYAFFINITY = 39
    LDR = 40
    WAR = 41
    INT = 42
    POL = 43
    CHR = 44
    LDRGROWTH = 45
    WARGROWTH = 46
    INTGROWTH = 47
    POLGROWTH = 48
    CHRGROWTH = 49
    BIRTHPLACE = 50
    SKILL = 51
    DEBATESTYLE = 52
    VIRTUE = 53
    DESIRE = 54
    RANKSELECTION = 55
    CHARACTER = 56
    VOICE = 57
    TONE = 58
    COURTIMPORTANCE = 59
    STRATEGICTENDENCY = 60
    LOCALAFFILIATION = 61
    MODELSTANCE = 62
    MODELHEADGEAR = 63
    MODELFACE = 64
    MODELBODY = 65
    MODELCAPE = 66
    MODELARMS = 67
    MODELBOOTS = 68
    MODELARROWS = 69
    MODELUNKNOWN = 70
    MODELBOW = 71
    MODELWEAPON = 72
    MODELHORSE = 73
    PORTRAITAGE = 74
    GUILECARDS = 75

    def __index__(self):
        return self.value


class Item(Enum):
    ID = 0
    NAME = 1
    TYPE = 2
    LOYALTY = 3
    PICTURE = 4
    OWNER = 5
    CITY = 6
    OWNERORCITY = 7

    def __index__(self):
        return self.value


class District(Enum):
    ID = 0
    POSITION = 1
    NUMBER = 2
    RULER = 3
    TARGET = 4
    SPECIFICTARGET = 5

    def __index__(self):
        return self.value


class City(Enum):
    ID = 0
    FORCE = 1
    MAXTROOPS = 2
    TROOPS = 3
    GOLD = 4
    FOOD = 5
    SPEARS = 6
    PIKES = 7
    BOWS = 8
    HORSERS = 9
    RAMS = 10
    TOWERS = 11
    SHIPS = 12
    UNKNOWN = 13
    TRADE = 14
    REVENUE = 15
    HARVEST = 16
    MAXHP = 17
    WILL = 18
    ORDER_ = 19
    SPECIALTY = 20

    def __index__(self):
        return self.value


class Gate_port(Enum):
    ID = 0
    FORCE = 1
    TROOPS = 2
    GOLD = 3
    FOOD = 4
    SPEARS = 5
    PIKES = 6
    BOWS = 7
    HORSES = 8
    RAMS = 9
    TOWERS = 10
    SHIPS = 11
    WILL = 12
    UNKNOWN = 13

    def __index__(self):
        return self.value


class Country(Enum):
    ID = 0
    NAME = 1
    DESCRIPTION = 2
    UNKNOWN1 = 3
    UNKNOWN2 = 4
    USED = 5

    def __index__(self):
        return self.value
