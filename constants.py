from collections import defaultdict

# 0xFF = index 255 maps to white
colour_map = {
    0x00: 0x2828E8, 0x01: 0x387800, 0x02: 0xD00028, 0x03: 0x8C662A, 0x04: 0x200070, 0x05: 0x5A5A5A, 0x06: 0x20DEE0, 0x07: 0xDAD23A, 0x08: 0xF69CB2, 0x09: 0xA0D488,
    0x0A: 0x1E1E1E, 0x0B: 0xF26C20, 0x0C: 0xA286AC, 0x0D: 0x5C1646, 0x0E: 0x900018, 0x0F: 0x8AC832, 0x10: 0xC4447A, 0x11: 0x8692BA, 0x12: 0xC2E088, 0x13: 0x009A7A,
    0x14: 0x463A00, 0x15: 0x423A80, 0x16: 0x9C9C9C, 0x17: 0x746442, 0x18: 0x005490, 0x19: 0xAA2C50, 0x1A: 0xF25E52, 0x1B: 0xFFFA88, 0x1C: 0xF89820, 0x1D: 0xA89870,
    0x1E: 0x942C78, 0x1F: 0x780094, 0x20: 0x86461E, 0x21: 0x007150, 0x22: 0xF79A64, 0x23: 0x12495C, 0x24: 0x8A80AC, 0x25: 0x008FC4, 0x26: 0x00A63C, 0x27: 0xF03450,
    0x28: 0xDCB06C, 0x29: 0xFFF416, 0x2A: 0x80CA87, 0x2B: 0x8EECEC, 0x2C: 0x80A6CC, 0x2D: 0x006FA9, 0x2E: 0xB8700C, 0x2F: 0x6EB8A7, 0x30: 0x20E020, 0x31: 0xE020DE,
    0xFF: 0xFFFFFF
}

city_map = [
    "Xiang Ping",
    "Bei Ping",
    "Ji",
    "Nan Pi",
    "Ping Yuan",
    "Jin Yang",
    "Ye",
    "Bei Hai",
    "Xia Pi",
    "Xiao Pei",
    "Shou Chun",
    "Pu Yang",
    "Chen Liu",
    "Xu Chang",
    "Ru Nan",
    "Luo Yang",
    "Wan",
    "Chang An",
    "Shang Yong",
    "An Ding",
    "Tian Shui",
    "Wu Wei",
    "Jian Ye",
    "Wu",
    "Hui Ji",
    "Lu Jiang",
    "Chai Sang",
    "Jiang Xia",
    "Xin Ye",
    "Xiang Yang",
    "Jiang Ling",
    "Chang Sha",
    "Wu Ling",
    "Gui Yang",
    "Ling Ling",
    "Yong An",
    "Han Zhong",
    "Zi Tong",
    "Jiang Zhou",
    "Cheng Du",
    "Jian Ning",
    "Yun Nan",
    "Hu",
    "Hu Lao gate",
    "Tong Gate",
    "Han Gu gate",
    "Wu gate",
    "Yang Ping",
    "Jian Ge",
    "Jia Meng",
    "Pei Shui",
    "Mian Zhu",
    "An Ping port",
    "Gao Tang",
    "Xi He",
    "Bai Ma",
    "Chang Yang",
    "Lin Ji",
    "Hai Ling",
    "Jiang Duo",
    "Ru Xu",
    "Dun Qiu",
    "Guan Du",
    "Meng Jin",
    "Jie Xian",
    "Xin Feng",
    "Xia Feng",
    "Fang Ling",
    "Wu Hu",
    "Hu Lin",
    "Qu A",
    "Ju Zhang",
    "Wan Kou",
    "Jiu Jiang",
    "Lu Kou",
    "Bou Yang",
    "Lu Ling",
    "Xia Kou",
    "Hu Yang",
    "Zhong Lu",
    "Wu Lin",
    "Han Jin",
    "Jiang Jin",
    "Lu Xian",
    "Dong Tine",
    "Gong An",
    "Wu Xian",
]


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
    0x03: "SeniorMinister",
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
    0x05: "Zhang Fei",
    0x06: "barbarian",
    0x08: "frank",
    0x09: "dignified",
    0x0a: "pompus",
    0x0b: "reckless",
    0x0c: "humble",
    0x0d: "courteous",
    0x0e: "polite",
    0x0f: "normal",
}

court_importance_map = {
    0x00: "Ignore",
    0x01: "Normal",
    0x02: "Important",
}

weapon_model_map = defaultdict(lambda: "Default", {
    0x01: "Serpent Spear",
    0x02: "Blue Dragon",
    0x03: "Sky Scorcher",
    0x04: "Arrow",
    0x05: "Fan",
})

horse_model_map = defaultdict(lambda: "Default", {
    0x01: "Red Hare",
    0x02: "Hex Mark",
    0x03: "Shadow Runner",
    0x04: "Gray Lightning",
})


action_map = defaultdict(lambda: "Default", {
    0x68: "Available",
    0x20: "Available",
    0xC8: "Available",
})
