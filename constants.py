from enum import Enum
from collections import defaultdict

NUM_OFFICERS = 850
NUM_FORCES = 42


def reverse(d): return {v: k for k, v in d.items()}


class Version(Enum):
    PCEN = 0
    PCPUK = 1
    PS2EN = 2
    PS2PUK = 3

    def __index__(self):
        return self.value


class Force(Enum):
    ID = 0
    DIFFICULTY = 1
    DESC = 2
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


class Scenario(Enum):
    ID = 0
    NUMBER = 1
    YEAR = 2
    MONTH = 3
    UNKNOWN = 4
    NAME = 5
    DESC = 6
    INGAMEYEAR = 7
    INGAMEMONTH = 8
    UNKNOWN2 = 9
    EMPEROR = 10
    GAMEMODE = 11

    def __index__(self):
        return self.value


# 0xFF = index 255 maps to white
colour_map = {
    0x00: 0x2828E8, 0x01: 0x387800, 0x02: 0xD00028, 0x03: 0x8C662A, 0x04: 0x200070, 0x05: 0x5A5A5A, 0x06: 0x20DEE0, 0x07: 0xDAD23A, 0x08: 0xF69CB2, 0x09: 0xA0D488,
    0x0A: 0x1E1E1E, 0x0B: 0xF26C20, 0x0C: 0xA286AC, 0x0D: 0x5C1646, 0x0E: 0x900018, 0x0F: 0x8AC832, 0x10: 0xC4447A, 0x11: 0x8692BA, 0x12: 0xC2E088, 0x13: 0x009A7A,
    0x14: 0x463A00, 0x15: 0x423A80, 0x16: 0x9C9C9C, 0x17: 0x746442, 0x18: 0x005490, 0x19: 0xAA2C50, 0x1A: 0xF25E52, 0x1B: 0xFFFA88, 0x1C: 0xF89820, 0x1D: 0xA89870,
    0x1E: 0x942C78, 0x1F: 0x780094, 0x20: 0x86461E, 0x21: 0x007150, 0x22: 0xF79A64, 0x23: 0x12495C, 0x24: 0x8A80AC, 0x25: 0x008FC4, 0x26: 0x00A63C, 0x27: 0xF03450,
    0x28: 0xDCB06C, 0x29: 0xFFF416, 0x2A: 0x80CA87, 0x2B: 0x8EECEC, 0x2C: 0x80A6CC, 0x2D: 0x006FA9, 0x2E: 0xB8700C, 0x2F: 0x6EB8A7, 0x30: 0x20E020, 0x31: 0xE020DE,
    0xFF: 0xFFFFFF
}

city_map = {
    0x00: "Xiang Ping",
    0x01: "Bei Ping",
    0x02: "Ji",
    0x03: "Nan Pi",
    0x04: "Ping Yuan",
    0x05: "Jin Yang",
    0x06: "Ye",
    0x07: "Bei Hai",
    0x08: "Xia Pi",
    0x09: "Xiao Pei",
    0x0A: "Shou Chun",
    0x0B: "Pu Yang",
    0x0C: "Chen Liu",
    0x0D: "Xu Chang",
    0x0E: "Ru Nan",
    0x0F: "Luo Yang",
    0x10: "Wan",
    0x11: "Chang An",
    0x12: "Shang Yong",
    0x13: "An Ding",
    0x14: "Tian Shui",
    0x15: "Wu Wei",
    0x16: "Jian Ye",
    0x17: "Wu",
    0x18: "Hui Ji",
    0x19: "Lu Jiang",
    0x1A: "Chai Sang",
    0x1B: "Jiang Xia",
    0x1C: "Xin Ye",
    0x1D: "Xiang Yang",
    0x1E: "Jiang Ling",
    0x1F: "Chang Sha",
    0x20: "Wu Ling",
    0x21: "Gui Yang",
    0x22: "Ling Ling",
    0x23: "Yong An",
    0x24: "Han Zhong",
    0x25: "Zi Tong",
    0x26: "Jiang Zhou",
    0x27: "Cheng Du",
    0x28: "Jian Ning",
    0x29: "Yun Nan",
    0x2A: "Hu",
    0x2B: "Hu Lao gate",
    0x2C: "Tong Gate",
    0x2D: "Han Gu gate",
    0x2E: "Wu gate",
    0x2F: "Yang Ping",
    0x30: "Jian Ge",
    0x31: "Jia Meng",
    0x32: "Pei Shui",
    0x33: "Mian Zhu",
    0x34: "An Ping port",
    0x35: "Gao Tang",
    0x36: "Xi He",
    0x37: "Bai Ma",
    0x38: "Chang Yang",
    0x39: "Lin Ji",
    0x3A: "Hai Ling",
    0x3B: "Jiang Duo",
    0x3C: "Ru Xu",
    0x3D: "Dun Qiu",
    0x3E: "Guan Du",
    0x3F: "Meng Jin",
    0x40: "Jie Xian",
    0x41: "Xin Feng",
    0x42: "Xia Feng",
    0x43: "Fang Ling",
    0x44: "Wu Hu",
    0x45: "Hu Lin",
    0x46: "Qu A",
    0x47: "Ju Zhang",
    0x48: "Wan Kou",
    0x49: "Jiu Jiang",
    0x4A: "Lu Kou",
    0x4B: "Bou Yang",
    0x4C: "Lu Ling",
    0x4D: "Xia Kou",
    0x4E: "Hu Yang",
    0x4F: "Zhong Lu",
    0x50: "Wu Lin",
    0x51: "Han Jin",
    0x52: "Jiang Jin",
    0x53: "Lu Xian",
    0x54: "Dong Tine",
    0x55: "Gong An",
    0x56: "Wu Xian",
    0xFF: "Not Available",
    0xFFFF: "Not Available",
}


officer_status_map = {
    0x00: "Sovereign",
    0x01: "Viceroy",
    0x02: "Prefect",
    0x03: "Officer",
    0x04: "Free officer",
    0x05: "Prisoner",
    0x06: "Under aged",
    0x07: "Searchable",
    0x08: "Dead",
    0xff: "Not available",
}

officer_ranks_map = {
    0x00: "Prime Minister",
    0x01: "Chief Minister",
    0x02: "Chief Officer",
    0x03: "Senior Minister",
    0x04: "Minister",
    0x05: "Guard Captain",
    0x06: "Horse Captain",
    0x07: "Marshal",
    0x08: "Chancellor",
    0x09: "Sub-chancellor",
    0x0a: "Court Officer",
    0x0b: "Guard Officer",
    0x0c: "E Off. (conquest)",
    0x0d: "S Off. (conquest)",
    0x0e: "W Off. (conquest)",
    0x0f: "N Off. (conquest)",
    0x10: "Secretary General",
    0x11: "Chief Secretary",
    0x12: "Undersecretary",
    0x13: "Chief Administrator",
    0x14: "E Off(subjugation)",
    0x15: "S Off. (subjugation)",
    0x16: "W Off. (subjugation)",
    0x17: "N Off. (subjugation)",
    0x18: "Jnr Minister",
    0x19: "Chief of Records",
    0x1a: "Finance Advisor",
    0x1b: "Jnr Prefect",
    0x1c: "E Off. (defense)",
    0x1d: "S Off. (defense)",
    0x1e: "W Off. (defense)",
    0x1f: "N Off. (defense)",
    0x20: "Security Chief",
    0x21: "Commandant",
    0x22: "Records Officer",
    0x23: "Fellow",
    0x24: "E Commander",
    0x25: "W Commander",
    0x26: "Fore Commander",
    0x27: "Rear Commander",
    0x28: "Snr Advisor",
    0x29: "City Officer",
    0x2a: "Attendant",
    0x2b: "Records Secretary",
    0x2c: "Off. (strategy)",
    0x2d: "Off. (defense)",
    0x2e: "Off. (prisoners)",
    0x2f: "Off. (negotiaton)",
    0x30: "Senior Secretary",
    0x31: "Secretary",
    0x32: "Jnr Secretary",
    0x33: "Sima",
    0x34: "E Sub-officer",
    0x35: "S Sub-officer",
    0x36: "W Sub-officer",
    0x37: "N Sub-officer",
    0x38: "Administrator",
    0x39: "Treasury Officer",
    0x3a: "Armory Officer",
    0x3b: "Snr Guard",
    0x3c: "Gatekeeper",
    0x3d: "Guard",
    0x3e: "Lieutenant",
    0x3f: "2nd Lieutenant",
    0x40: "Senior Officer",
    0x41: "Negotiator",
    0x42: "Chief Retainer",
    0x43: "Retainer",
    0x44: "Officer",
    0x45: "Officer",
    0x46: "Officer",
    0x47: "Officer",
    0x48: "E Retainer",
    0x49: "W Retainer",
    0x4a: "Agric. Advisor",
    0x4b: "Vassal",
    0x4c: "Officer",
    0x4d: "Officer",
    0x4e: "Officer",
    0x4f: "Officer",
    0x50: "None",
    0xFF: "None"
}

growth_ability_map = {
    0x00: "Maintain + Long",
    0x01: "Maintain + Short",
    0x02: "Precocious + Short",
    0x03: "Precocious + Long",
    0x04: "Normal + Short",
    0x05: "Normal + Long",
    0x06: "Late Bloomer + Long",
    0x07: "Late Bloomer + Short",
    0x08: "Open"
}

skill_map = {
    0x5e: "Nanman ties",
    0x63: "Spousal support",
    0x62: "Prayer",
    0x61: "Feng shui",
    0x60: "Benevolent rule",
    0x5f: "Suppression",
    0x5d: "Shanyue ties",
    0x5c: "Qiang ties",
    0x5b: "Wuwan ties",
    0x5a: "Levy",
    0x59: "Taxation",
    0x58: "Sustenance",
    0x57: "Wealth",
    0x56: "Negotiator",
    0x55: "Enlister",
    0x54: "Pedagogy",
    0x53: "Shipbuilding",
    0x52: "Invention",
    0x51: "Breeding",
    0x50: "Efficacy",
    0x4f: "Fame",
    0x4e: "Colonization",
    0x4d: "Fortification",
    0x4c: "Stirring music",
    0x4b: "Gladdened heart",
    0x4a: "Clear thought",
    0x49: "Indomitable",
    0x48: "Integrity",
    0x47: "Black arts",
    0x46: "Sorcery",
    0x45: "Siren",
    0x44: "Counter plan",
    0x43: "Intensify",
    0x42: "Chain reaction",
    0x41: "Augment",
    0x40: "focus",
    0x3f: "Divine potency",
    0x3e: "Divine fire",
    0x3d: "Insight",
    0x3c: "Detection",
    0x3b: "Covert plan",
    0x3a: "Cunning",
    0x39: "Agile mind",
    0x38: "Trickery",
    0x37: "Disconcertion",
    0x36: "Poison tongue",
    0x35: "Fire assault",
    0x34: "Escort",
    0x33: "Vehemence",
    0x32: "Bowmanship",
    0x31: "Stampede",
    0x30: "Puissance",
    0x2f: "Divine waters",
    0x2e: "Divine forge",
    0x2d: "Divine cavalry",
    0x2c: "Divine bows",
    0x2b: "Divine pikes",
    0x2a: "Divine spears",
    0x29: "Divine right",
    0x28: "God\'s command",
    0x27: "Valiant general",
    0x26: "Admiral",
    0x25: "Cavalry general",
    0x24: "Archer general",
    0x23: "Pike general",
    0x22: "Spear general",
    0x21: "Escape route",
    0x20: "Providence",
    0x1f: "Aegis",
    0x1e: "Resolute",
    0x1d: "Iron wall",
    0x1c: "Indestructible",
    0x1b: "Fortitude",
    0x1a: "Assistance",
    0x19: "White riders",
    0x18: "Range",
    0x17: "Exterminate",
    0x16: "Beguile",
    0x15: "Plunder",
    0x14: "Masterful",
    0x13: "Capture",
    0x12: "Entrap",
    0x11: "Siege",
    0x10: "Critical ambush",
    0x0f: "Close combat",
    0x0e: "Marine raid",
    0x0d: "Raid",
    0x0c: "Chain attack",
    0x0b: "Promotion",
    0x0a: "Majesty",
    0x09: "Sweep asunder",
    0x08: "Antidote",
    0x07: "Transport",
    0x06: "Traverse",
    0x05: "Seamanship",
    0x04: "Propulsion",
    0x03: "Foced gallop",
    0x02: "Forced march",
    0x01: "Fleetness",
    0x00: "Flying general",
    0xff: "None",
}

character_map = {
    0x00:  "Timid",
    0x01:  "Cool",
    0x02:  "Bold",
    0x03:  "Reckless",
}

voice_map = {
    0x00: "Timid",
    0x01: "Cool",
    0x02: "Bold",
    0x03: "Reckless",
    0x04: "Female Cool",
    0x05: "Female Bold",
    0x06: "Lu Bu",
    0x07: "Zhuge Liang",
}

tone_map = {
    0x00: "Female Barbarian",
    0x01: "Female Reckless",
    0x02: "Female Dignified",
    0x03: "Xiao Qiao/Da Qiao",
    0x04: "Female Frank",
    0x05: "Zhang Fei",
    0x06: "Barbarian",
    0x07: "Guan Yu",
    0x08: "Frank",
    0x09: "Dignified",
    0x0a: "Pompus",
    0x0b: "Reckless",
    0x0c: "Humble",
    0x0d: "Courteous",
    0x0e: "Polite",
    0x0f: "Normal",
}

court_importance_map = {
    0x00: "Ignore",
    0x01: "Normal",
    0x02: "Important",
}

weapon_model_map = defaultdict(lambda: "Spear", {
    0x01: "Blue Dragon",
    0x02: "Serpent Spear",
    0x03: "Crescent Halberd",
    0x04: "Arrow",
    0x05: "Feather Fan",
})

horse_model_map = defaultdict(lambda: "Normal Horse", {
    0x01: "Red Hare",
    0x02: "Hex Mark",
    0x03: "Shadow Runner",
    0x04: "Gray Lightning",
    0x05: "Firestar",
})

stance_map = defaultdict(lambda: "Normal", {
    0x01: "Woman",
    0x02: "Bulky Warrior",
    0x03: "Zhuge Liang"
})


action_map = defaultdict(lambda: "Default", {
    0x68: "Available",
    0x20: "Available",
    0xC8: "Available",
})

affinity_map = {
    0x00: "C",
    0x01: "B",
    0x02: "A",
    0x03: "S",
}

use_map = {
    0x00: "Ability",
    0x01: "Performance",
    0x02: "Fame",
    0x03: "Righteousness",
    0x04: "Arbitrary"
}

debate_map = {
    0x00: "Fact",
    0x01: "Logic",
    0x02: "Time"
}

strategy_map = {
    0x2C: "Endless Might",
    0x00: "National Desires",
    0x01: "Local Desires",
    0x02: "State Desires",
    0x03: "Maintain"
}

campaign_map = {
    0x00: "Countryside",
    0x01: "Impromptu Strategy",
    0x02: "Sea is Home"
}

item_type_map = {
    0x00: "Elite Horse",
    0x01: "Sword",
    0x02: "Long Spear",
    0x03: "Throwing Knife",
    0x04: "Bow",
    0x05: "Writings",
    0x06: "Imperial Seal",
    0x07: "Bronze Pheasant",
    0xFF: "Not Available",
}

title_map = {
    0x00: "Emperor",
    0x01: "Regent",
    0x02: "Duke",
    0x03: "Baron",
    0x04: "Grand General",
    0x05: "Field Marshal",
    0x06: "General",
    0x07: "Governor",
    0x08: "Lt. Governor",
    0x09: "None",
    0xFF: "Not Available",
}

country_map = {
    0x00: "Wei",
    0x01: "Wu",
    0x02: "Shu",
    0x03: "Ji",
    0x04: "Cheng",
    0x05: "Yellow Turbans",
    0x06: "Han",
    0x07: "Xia",
    0x08: "Chang",
    0x09: "Zhou",
    0x0a: "Qin",
    0x0b: "Xin",
    0x0c: "Yan",
    0x0d: "Zhao",
    0x0e: "Qi",
    0x0f: "Ji",
    0x10: "Lu",
    0x11: "Cao",
    0x12: "Xue",
    0x13: "Xu",
    0x14: "Song",
    0x15: "Chen",
    0x16: "Su",
    0x17: "Han",
    0x18: "Gu",
    0x19: "Zheng",
    0x1a: "Xu",
    0x1b: "Yu",
    0x1c: "Liang",
    0x1d: "Liang",
    0x1e: "Cai",
    0x1f: "Tang",
    0x20: "Deng",
    0x21: "Shen",
    0x22: "Sui",
    0x23: "Chu",
    0x24: "Yue",
    0x25: "Wuwan",
    0x26: "Qiang",
    0x27: "Shanyue",
    0x28: "Nanman",
    0x29: "Bandit",
    0xFF: "Not Available",
}

ghost_officer_map = {
    0xD007: "Yuan Shao's father (Yuan Cheng I guess)",
    0xD107: "Yuan Yin's father",
    0xD207: "Yuan Shu's & Yuan Yi's father (Yuan Feng, but weren't Shu and Yi cousins?)",
    0xD307: "Wang Yun's father",
    0xD407: "Wang Ling's father",
    0xD507: "Kuai Liang's & Kuai Yue's father",
    0xD607: "Xiahou Dun's father",
    0xD707: "Xiahou De's & Xiahou Shang's father",
    0xD807: "Xiahou Yuan's father",
    0xD907: "Guanqiu Jian's & Guanqiu Xiu's father",
    0xDA07: "Han Xuan's & Han Hao's father",
    0xDB07: "Yan Baihu's & Yan Yu's father",
    0xDC07: "Gao Gan's & Gao Rou's father",
    0xDD07: "Gongsun Zan's & Gongsun Yue's father",
    0xDE07: "Gongsun Fan's father",
    0xDF07: "Cai He's & Cai Zhong's father",
    0xE007: "Cai Mao's & Cai Shi's father (I thought they were siblings of Cai He and Zhong?)",
    0xE107: "Sima Lang's, Sima Yi's & Sima Fu's father (Sima Fang I guess)",
    0xE207: "Zhou Xin's & Zhou Ang's father",
    0xE307: "Zhu Rong's & Dailai Dongzhu's father",
    0xE407: "Xun Yu's & Xun Chen's father (Xun Gun I guess)",
    0xE507: "Xun You's father",
    0xE607: "Xun Xu's father",
    0xE707: "Xiang Lang's father",
    0xE807: "Xiang Chong's father",
    0xE907: "Zhuge Jin's, Zhuge Liang's & Zhuge Jun's father (must be Zhuge Gui)",
    0xEA07: "Shen Yi's & Shen Dan's father",
    0xEB07: "Xin Ping's & Xin Pi's father",
    0xEC07: "Cao Cao's father (Cao Song)",
    0xED07: "Cao Xiu's father",
    0xEE07: "Cao Zhen's father (Cao/Qin Shao)",
    0xEF07: "Cao Ren's & Cao Chun's father (Cao Chi)",
    0xF007: "Cao Hong's father",
    0xF107: "Cao Mao's father (Cao Lin)",
    0xF207: "Sun Huan's father",
    0xF307: "Sun Shao's father",
    0xF407: "Sun Jian's & Sun Jing's father",
    0xF507: "Sun Xiu's father (General, not Emperor Sun Xiu)",
    0xF607: "Sun Jun's father",
    0xF707: "Sun Chen's father",
    0xF807: "None",
    0xF907: "Sun Xin's & Sun Zhen's father",
    0xFA07: "Zhang Jiao's, Zhang Bao's & Zhang Liang's father",
    0xFB07: "None",
    0xFC07: "Zhang Ji's father (Dong Zhuo's general)",
    0xFD07: "Zhang Xiu's father (Lord of Wan)",
    0xFE07: "Zhang Lu's & Zhang Wei's father",
    0xFF07: "Ding Feng's & Ding Feng's father",
    0x0008: "Dong Zhuo's & Dong Min's father",
    0x0108: "None",
    0x0208: "Ma Dai's father",
    0x0308: "Ma Liang's & Ma Su's father",
    0x0408: "Mi Zhu's, Mi Fang's & Mi Shi's father",
    0x0508: "Meng Huo's & Meng You's father",
    0x0608: "Yang Bo's & Yang Song's father",
    0x0708: "Lu Xun's father",
    0x0808: "Lu Kai's father (Wu general)",
    0x0908: "Liu Yao's & Liu Dai's father",
    0x0A08: "Lu Kuang's & Lu Xiang's father",
    0x0B08: "Wu Jing's & Wu Guotai's father",
    0xFFFF: "None"
}

specialty_options = {
    0: "Large City",
    1: "Spears",
    2: "Pikes",
    3: "Bows",
    4: "Horses",
    5: "Weaponry",
    6: "Navy"
}

specialty_hex = [int(n, 16) for n in [
    '000000000000',
    '010000000000',
    '000100000000',
    '000001000000',
    '000000010000',
    '000000000100',
    '000000000001'
]]

col_map = {
    'rank': officer_ranks_map,
    'status': officer_status_map,
    'title': title_map,
    'affinity': affinity_map,
    'skill': skill_map,
    'debatestyle': debate_map,
    'voice': voice_map,
    'location': city_map,
    'character': character_map,
    'tone': tone_map,
    'spearaffinity': affinity_map,
    'pikeaffinity': affinity_map,
    'bowaffinity': affinity_map,
    'cavalryaffinity': affinity_map,
    'siegeaffinity': affinity_map,
    'navyaffinity': affinity_map,
    'modelstance': stance_map,
    'modelweapon': weapon_model_map,
    'modelhorse': horse_model_map,
    'country': country_map,
    'type': item_type_map,
    'courtimportance': court_importance_map,
    'strategictendency': strategy_map
}

officer_columns = [
    'strategist',
    'ruler',
    'father',
    'mother',
    'spouse',
    'swornbrother',
    'likedofficer1',
    'likedofficer2',
    'likedofficer3',
    'likedofficer4',
    'likedofficer5',
    'dislikedofficer1',
    'dislikedofficer2',
    'dislikedofficer3',
    'dislikedofficer4',
    'dislikedofficer5',
    'clan',
    'emperor',
    'owner'
]

research_labels = [
    "Pikes", "Spears", "Horses", "Bows",
    "Invention", "Command", "Fire", "Defense"]

research_level_values = [0x0, 0x1, 0x3, 0x7, 0xf]

conquer_region_map = {
    0x00: "Hebei (Northern China)",
    0x01: "Zhongyuan (Central Plains)",
    0x02: "Xibei (Northwest)",
    0x03: "Jiangnan (Jing and Yang Provinces)",
    0x04: "Bashu (Yi Province)",
    0x05: "Nanzhong (Yunnan and Jianning)",
}

conquer_province_map = {
    0x00: "You Province (Xiangping, Beiping, Ji)",
    0x01: "Ji & Bing Province (Nanpi, Pingyuan, Jinyang, Ye)",
    0x02: "Qing & Xu Province (Beihai, Xiapi, Xiaopei, Shouchun)",
    0x03: "Yan & Yu Province (Puyang, Chenliu, Xuchang, Runan)",
    0x04: "Sili (Luoyang)",
    0x05: "Jingzhao (Wan, Chang'an, Shangyong)",
    0x06: "Liang Province (Anding, Tianshui, Wuwei)",
    0x07: "Yang Province (Jianye, Wu, Huiji, Lujiang, Chaisang)",
    0x08: "Jingbei (Jiangxia, Xinye, Xiangyang)",
    0x09: "Jingnan (Jiangling, Changsha, Wuling, Guiyang, Lingling)",
    0x0A: "Yi Province (Yong'an, Hanzhong, Zitong, Jiangzhou, Chengdu)",
    0x0B: "Nanzhong (Jianning, Yunnan)",
}

aspiration_map = {
    0x00: "Conquer China",
    0x01: "Conquer Region",
    0x02: "Conquer Province",
    0x03: "Passive",
    0xFF: "Unused"
}

ps2_scenarios = {
    name: offset for offset, name in zip(
        [0x1D3800 + 180224*i for i in range(10)],
        ["Yellow Turbans", "Dong Zhou's Rise", "Rival Warlords", "Clash at Guan Du", "The Three Visits",
         "Liu Bei in Shu", "Nanman Rebellion", "Rise of Heroes", "Lu Bu Campaign", "Power Struggle", "Country Basics", ])
}
# | {
#     name: offset for offset, name in zip(
#         [0x3FC808 + 118800*i for i in range(14)],
#         ["Military Basics", "Going to Battle", "Traps & Facilities", "Techniques",
#          "Capturing Cheng Du", "Hunting Dong Zhuo", "The Turbans' End", "Liu Bei Subjugation", "Guan Du Skirmish",
#          "Huang Zu", "Mai Castle Escape", "Nanman Rebellion", "Defense of Jie Ting",])
# }
