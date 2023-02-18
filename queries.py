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

scenarioinsertquery = f'''
INSERT INTO scenario (
    name, 
    desc, 
    year, 
    month
) VALUES ({",".join(["?"]*4)})'''

forcesinsertquery = f'''
INSERT INTO forces (
    id,
    ruler,
    desc,
    colour,
    district_number,
    difficulty,
    behaviour
) VALUES ({",".join(["?"]*7)})'''

officerinsertquery = f"""
INSERT INTO officers (
    id,
    family_name,
    given_name,
    portrait,
    sex,
    available_date,
    birth_date,
    death_date,
    father,
    mother,
    spouse,
    sworn_brother,
    compatibility,
    liked_officer_1,
    liked_officer_2,
    liked_officer_3,
    liked_officer_4,
    liked_officer_5,
    disliked_officer_1,
    disliked_officer_2,
    disliked_officer_3,
    disliked_officer_4,
    disliked_officer_5,
    allegiance,
    location,
    service,
    status,
    rank,
    loyalty,
    deeds,
    spear_affinity,
    pike_affinity,
    bow_affinity,
    cavalry_affinity,
    weaponry_affinity,
    navy_affinity,
    ldr,
    war,
    int,
    pol,
    chr,
    ldr_growth,
    war_growth,
    int_growth,
    pol_growth,
    chr_growth,
    skill,
    debatestyle,
    loyaltylevel,
    ambition,
    use,
    character,
    voice,
    tone,
    court_importance,
    strategy,
    campaign_style,
    model_sex,
    model,
    weapon_model,
    horse_model,
    portrait_age,
    action,
    debate_ability
) VALUES ({",".join(["?"]*64)})"""

itemsinsertquery = f'''
INSERT INTO items (
    id,
    name,
    type,
    loyalty,
    picture,
    owner,
    city,
    owned
) VALUES ({",".join(["?"]*8)})'''