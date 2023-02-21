scenariocreatequery = '''
CREATE TABLE IF NOT EXISTS scenario (
    name TEXT(26),
    desc TEXT(600),
    year INTEGER,
    month INTEGER
)'''

forcescreatequery = '''
CREATE TABLE IF NOT EXISTS forces (
    id INTEGER PRIMARY KEY,
    ruler INTEGER,
    desc TEXT(60),
    colour INTEGER,
    district_number INTEGER,
    difficulty INTEGER,
    behaviour INTEGER
)'''

officercreatequery = '''
CREATE TABLE IF NOT EXISTS officers (
    id INTEGER PRIMARY KEY,
    family_name TEXT(12),
    given_name TEXT(41),
    portrait INTEGER,
    sex INTEGER,
    available_date INTEGER,
    birth_date INTEGER,
    death_date INTEGER,
    father INTEGER,
    mother INTEGER,
    spouse INTEGER,
    sworn_brother INTEGER,
    compatibility INTEGER,
    liked_officer_1 INTEGER,
    liked_officer_2 INTEGER,
    liked_officer_3 INTEGER,
    liked_officer_4 INTEGER,
    liked_officer_5 INTEGER,
    disliked_officer_1 INTEGER,
    disliked_officer_2 INTEGER,
    disliked_officer_3 INTEGER,
    disliked_officer_4 INTEGER,
    disliked_officer_5 INTEGER,
    allegiance INTEGER,
    location INTEGER,
    service INTEGER,
    status INTEGER,
    rank INTEGER,
    loyalty INTEGER,
    deeds INTEGER,
    spear_affinity INTEGER,
    pike_affinity INTEGER,
    bow_affinity INTEGER,
    cavalry_affinity INTEGER,
    weaponry_affinity INTEGER,
    navy_affinity INTEGER,
    ldr INTEGER,
    war INTEGER,
    int INTEGER,
    pol INTEGER,
    chr INTEGER,
    ldr_growth INTEGER,
    war_growth INTEGER,
    int_growth INTEGER,
    pol_growth INTEGER,
    chr_growth INTEGER,
    skill INTEGER,
    debatestyle INTEGER,
    loyaltylevel INTEGER,
    ambition INTEGER,
    use INTEGER,
    character INTEGER,
    voice INTEGER,
    tone INTEGER,
    court_importance INTEGER,
    strategy INTEGER,
    campaign_style INTEGER,
    model_sex INTEGER,
    model INTEGER,
    weapon_model INTEGER,
    horse_model INTEGER,
    portrait_age INTEGER,
    action INTEGER,
    debate_ability INTEGER
)'''

itemscreatequery = '''
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY,
    name TEXT(27),
    type INTEGER,
    loyalty INTEGER,
    picture INTEGER,
    owner INTEGER,
    city INTEGER,
    owned INTEGER
)'''

citiescreatequery = '''
CREATE TABLE IF NOT EXISTS cities (
    id INTEGER PRIMARY KEY,
    name TEXT,
    owner INTEGER,
    maxtroops INTEGER,
    inittroops INTEGER,
    gold INTEGER,
    food INTEGER,
    spears INTEGER,
    pikes INTEGER,
    bows INTEGER,
    horses INTEGER,
    rams INTEGER,
    towers INTEGER,
    boats INTEGER,
    marketrate INTEGER,
    revenue INTEGER,
    harvest INTEGER,
    maxhp INTEGER,
    inithp INTEGER,
    will INTEGER,
    \"order\" INTEGER,
    specialty INTEGER,
    districtnr INTEGER,
    citycolour INTEGER
)'''


def paramstr(n):
    return f"({','.join(['?']*n)})"


scenarioinsertquery = "INSERT INTO scenario VALUES" + paramstr(4)

forcesinsertquery = "INSERT INTO forces VALUES" + paramstr(7)

officerinsertquery = "INSERT INTO officers VALUES" + paramstr(64)

itemsinsertquery = "INSERT INTO items VALUES" + paramstr(8)

citiesinsertquery = "INSERT INTO cities VALUES" + paramstr(24)
