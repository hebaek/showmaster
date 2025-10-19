import re



def hack_text_pre(text):
    if not text: return None

    if re.search('MUSIKK',           text): return None
    if re.search('UNDERSCORE',       text): return None
    if re.search('ELSK MENS DU KAN', text): return None
    if re.search('SLUTT.',           text): return None

    text = text.replace('''(cont'd)''', '').strip()
    text = text.replace('VERS 4', '\nVERS 4')
    text = text.replace('  ', ' ')

    return text


def hack_text_post(text, text_type):
    if not text: return None

    if text_type == 'dialogue':
        text = text.replace('Sira Lars kommer bort til Jon. Holder han.', 'Sira Lars kommer bort til Jon. Holder ham.')
        text = text.replace(' OG ', ' og ')

    if text_type == 'parenthetical':
        text = text.removeprefix('(').removesuffix(')')

    return text



def fix_text_case(text, text_type, characters):
    if not text: return None

    text = text.lower()

    # Swap random case character names with proper casing
    for name in sorted(characters, key=len, reverse=True):
        regex = re.compile(rf'(?<!\w){name}(?!\w)', flags = re.UNICODE | re.IGNORECASE)
        text = regex.sub(name, text)

    text = text.replace('magnus eriksson', 'Magnus Eriksson')
    text = text.replace('maridalsvannet',  'Maridalsvannet')
    text = text.replace('margaretadalen',  'Margaretadalen')
    text = text.replace('st. Margaretha',  'St. Margaretha')
    text = text.replace('sigrunnsdatter',  'Sigrunnsdatter')
    text = text.replace('ogmundsdatter',   'Ogmundsdatter')
    text = text.replace('kolbjørnsson',    'Kolbjørnsson')
    text = text.replace('jomfru maria',    'jomfru Maria')
    text = text.replace('sveinsdatter',    'Sveinsdatter')
    text = text.replace('mariakirken',     'Mariakirken')
    text = text.replace('Kristendom',      'kristendom')
    text = text.replace('margaretha',      'Margaretha')
    text = text.replace('ogmunds...',      'Ogmunds...')
    text = text.replace('margareta',       'Margareta')
    text = text.replace('kolbjørn',        'Kolbjørn')
    text = text.replace('ivarsson',        'Ivarsson')
    text = text.replace('antiokia',        'Antiokia')
    text = text.replace('kirkeby',         'Kirkeby')
    text = text.replace('kjelsås',         'Kjelsås')
    text = text.replace('brekke',          'Brekke')
    text = text.replace('storo',           'Storo')
    text = text.replace('tømte',           'Tømte')
    text = text.replace('jesus',           'Jesus')
    text = text.replace('krist',           'Krist')
    text = text.replace('amors',           'Amors')
    text = text.replace('norge',           'Norge')
    text = text.replace('roma',            'Roma')
    text = text.replace('oslo',            'Oslo')
    text = text.replace('jesu',            'Jesu')
    text = text.replace('gud',             'Gud')
    text = text.replace('“', '"')

    # Hacks for å fikse følgefeil...
    text = text.replace('uGudelig',         'ugudelig')
    text = text.replace('Kristen',          'kristen')

    # Capitalize first letter and after periods, and after some punctuation and other stuff
    text = re.sub(r'(^|(?<=^")|(?<=\s")|(?<=[.?!]\s))(\w)', lambda m: m.group(2).upper(), text, re.UNICODE)

    return text



def get_text_type(text, content_type):
    if not text: return None

    text_type = '<unknown>'

    # Basic types
    if content_type == 'Scene Heading': text_type = 'scene'
    if content_type == 'Action':        text_type = 'action'
    if content_type == 'Character':     text_type = 'character'
    if content_type == 'Dialogue':      text_type = 'dialogue'
    if content_type == 'Parenthetical': text_type = 'parenthetical'
    if content_type == 'Cue':           text_type = 'cue'

    # Type variants
    if text_type == 'dialogue' and text.upper() == text: text_type = 'song'

    # Fix known errors
    if text_type == 'dialogue' and text[0] == '(':    text_type = 'parenthetical'
    if text_type == 'song' and text == 'HEI, JA!':    text_type = 'dialogue'
    if text_type == 'song' and text == 'NEI! MARIT!': text_type = 'dialogue'

    if text_type == 'song' and re.search('^VERS ', text): text_type = 'comment'

    return text_type
