import glob

# 0xFF = index 255 maps to white
colour_map = [
    0x2828E8, 0x387800, 0xD00028, 0x8C662A, 0x200070, 0x5A5A5A, 0x20DEE0, 0xDAD23A, 0xF69CB2, 0xA0D488,
    0x1E1E1E, 0xF26C20, 0xA286AC, 0x5C1646, 0x900018, 0x8AC832, 0xC4447A, 0x8692BA, 0xC2E088, 0x009A7A,
    0x463A00, 0x423A80, 0x9C9C9C, 0x746442, 0x005490, 0xAA2C50, 0xF25E52, 0xFFFA88, 0xF89820, 0xA89870,
    0x942C78, 0x780094, 0x86461E, 0x007150, 0xF79A64, 0x12495C, 0x8A80AC, 0x008FC4, 0x00A63C, 0xF03450,
    0xDCB06C, 0xFFF416, 0x80CA87, 0x8EECEC, 0x80A6CC, 0x006FA9, 0xB8700C, 0x6EB8A7, 0x20E020, 0xE020DE
]

city_map = [
    "Xiang Ping ",
    "Bei Ping ",
    "Ji ",
    "Nan Pi ",
    "Ping Yuan ",
    "Jin Yang ",
    "Ye ",
    "Bei Hai ",
    "Xia Pi ",
    "Xiao Pei ",
    "Shou Chun ",
    "Pu Yang ",
    "Chen Liu ",
    "Xu Chang ",
    "Ru Nan ",
    "Luo Yang ",
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
    "Hu ",
    "Hu Lao gate ",
    "Tong Gate ",
    "Han Gu gate ",
    "Wu gate ",
    "Yang Ping ",
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


def parsefile(f):
    # Attributes are marked as [OFFSET];[LENGTH]x[REPETITION]

    # 91;4 YEAR-00-MONTH-01 (Displayed Starting Date)
    f.seek(91)
    year, _, month, _ = f.read(4)
    print(year, month)

    # 95;26: Scenario Name.
    scenname = f.read(26).decode()
    print(scenname)

    # 121;600: Scenario Description.
    f.seek(121)
    tmp = f.read(600).decode()
    print(tmp)

    # 722;42: Force Colours.
    f.seek(722)
    data = f.read(42)
    colours = [
        colour_map[byte] if byte != 0xFF else 0xFFFFFF
        for byte in data
    ]
    print(colours)

    # 931;607x42: Force Descriptions.
    f.seek(931)
    for i in range(42):
        forcedesc = f.read(607).decode()
        print(i, forcedesc)

    # 26426;4 YEAR-00-MONTH-01 (In-Game Starting Date)
    f.seek(26427)
    year, _, month, _ = f.read(4)
    print(year, month)


def main():
    # for filename in glob.glob("scenario/SCEN*"):
    scenfile = open('scenario/SCEN000.S11', 'rb')
    parsefile(scenfile)


if __name__ == '__main__':
    main()
