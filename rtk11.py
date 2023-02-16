from constants import *


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
