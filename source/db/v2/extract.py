#!/usr/bin/python3

import xml.etree.ElementTree as ET
import mysql.connector

import sys
import re

from pprint import pprint



db = None
version = { 'current': None, 'previous': None }

characters = {}
scenes = []
texts  = []




def fix_text_case(text):
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

    # Hacks for å fikse følgefeil...
    text = text.replace('uGudelig',         'ugudelig')
    text = text.replace('Kristen',          'kristen')

    # Capitalize first letter and after periods, and after some punctuation and other stuff
    text = re.sub(r'(^|(?<=^")|(?<=\s")|(?<=[.?!]\s))(\w)', lambda m: m.group(2).upper(), text, re.UNICODE)

    return text



def hack_action_texts(text):
    if re.search('MUSIKK',           text): return None
    if re.search('UNDERSCORE',       text): return None
    if re.search('ELSK MENS DU KAN', text): return None
    if re.search('SLUTT.',           text): return None

    text = text.replace('Sira Lars kommer bort til Jon. Holder han.', 'Sira Lars kommer bort til Jon. Holder ham.')
    text = text.replace(' OG ', ' og ')

    return text



def hack_character_texts(text):
    text = text.replace('''(cont'd)''', '').strip()

    return text



def hack_dialogue_texts(text):
    text = text.replace('VERS 1', 'VERS 1\n')
    text = text.replace('VERS 4', 'VERS 4\n')

    return text



def getversion():
    mycursor = db.cursor(dictionary=True)

    sql = """SELECT MAX(`version_id`) as `version` FROM `versions`"""
    mycursor.execute(sql)
    result = mycursor.fetchone()
    version['previous'] = result['version']

    sql = """INSERT INTO `versions` (`person_id`, `name`, `comment`) VALUES (1, NULL, %s)"""
    mycursor.execute(sql, ('Created by Fadein Importer',))
    version['current'] = mycursor.lastrowid

    db.commit()



def fetch_characters():
    mycursor = db.cursor(dictionary=True)

    sql = """SELECT `alias`, `character`, `character_id` FROM `view_character_aliases` WHERE `version_end` IS NULL"""
    mycursor.execute(sql)
    for row in mycursor.fetchall():
        alias = row['alias']
        if not alias in characters: characters[alias] = []
        characters[alias].append({ 'id': row['character_id'], 'name': row['character'] })



def remove_scenes():
    mycursor = db.cursor(dictionary=True)

    sql = """SELECT `id` FROM `scenes` WHERE `version_end` IS NULL"""
    mycursor.execute(sql)
    existing_scene_ids = { row['id'] for row in mycursor.fetchall() }
    imported_scene_ids = { scene['id'] for scene in scenes }
    missing_scene_ids  = existing_scene_ids - imported_scene_ids

    if missing_scene_ids:
        sql = """UPDATE `scenes` SET `version_end` = %s WHERE `id` IN (%s)"""
        placeholders = ', '.join(['%s'] * len(missing_scene_ids))
        sql = sql % (version['previous'], placeholders)
        mycursor.execute(sql, tuple(missing_scene_ids))
        print(f'Updated version_end for scenes with IDs: {missing_scene_ids}')

    db.commit()



def remove_texts():
    mycursor = db.cursor(dictionary=True)

    sql = """SELECT `text_id`, `text` FROM `texts` WHERE `version_end` IS NULL"""
    mycursor.execute(sql)

    expired = set()
    for row in mycursor.fetchall():
        if row['text'] not in texts: expired.add(row['text_id'])

    for id in expired:
        sql = """UPDATE `texts` SET `version_end` = %s WHERE `text_id` = %s"""
        mycursor.execute(sql, (version['previous'], id))
        print(f'Updated version_end for text with ID: {id}')

    db.commit()



def sql_insert_scene(scene, index):
    mycursor = db.cursor(dictionary=True)

    def test_if_scene_exists(id):
        sql = """SELECT `scene_id`, `order`, `id`, `name` FROM `scenes` WHERE `id` = %s AND (`version_end` IS NULL)"""
        values = (id,)
        mycursor.execute(sql, values)
        return mycursor.fetchone()


    def expire_old_scene_version(id):
        sql = """UPDATE `scenes` SET `version_end` = %s WHERE `scene_id` = %s AND (`version_end` IS NULL)"""
        values = (version['previous'], id)
        mycursor.execute(sql, values)


    def insert_new_scene_version(id, name):
        sql = """INSERT INTO `scenes` (`version_start`, `order`, `id`, `name`) VALUES (%s, %s, %s, %s)"""
        values = (version['current'], index, scene['id'], scene['name'])
        mycursor.execute(sql, values)
        return mycursor.lastrowid


    existing_scene = test_if_scene_exists(scene['id'])

    if existing_scene:
        if existing_scene['name'] == scene['name'] and existing_scene['order'] == index:
            return existing_scene['scene_id']

        else:
            expire_old_scene_version(existing_scene['scene_id'])
            print(f'Expired existing scene')

    scene_id = insert_new_scene_version(scene['id'], scene['name'])
    db.commit()

    print(f'Inserted scene into SQL at scene_id {scene_id}: {scene}')
    return scene_id



def sql_insert_text(text, type, index):
    mycursor = db.cursor(dictionary=True)

    text_id = None

    sql = """SELECT * FROM `texts` WHERE `text` = %s AND (`version_end` IS NULL)"""
    mycursor.execute(sql, (text,))
    existing_text = mycursor.fetchone()

    if existing_text:
        text_id = existing_text['text_id']
    else:
        sql = """INSERT INTO `texts` (`version_start`, `order`, `text_type`, `text`) VALUES (%s, %s, %s, %s)"""
        values = (version['current'], index, type, text)
        mycursor.execute(sql, values)
        text_id = mycursor.lastrowid

        db.commit()

        print(f'''Inserted text into SQL at text_id {text_id}: {text}''')

    return text_id




def parse_scene(text):
    text = text.upper().strip()
    if not text:                       return None
    if not re.search('^SCENE ', text): return None

    [id, name] = text.split(' - ')

    return {
        'id': id.replace('SCENE ', '').strip(),
        'name': fix_text_case(name)
    }



def parse_action(text):
    text = text.strip()
    if not text: return None

    # TEXT HACK
    # This is only to fix obvious mistakes and remove stuff
    text = hack_action_texts(text)
    if not text: return None
    # END OF TEXT HACK

    text = fix_text_case(text)
    texts.append(text)

    return text



def parse_character(text):
    text = text.strip()
    if not text: return None

    text = fix_text_case(text)

    # TEXT HACK
    # This is only to fix obvious mistakes and remove stuff
    text = hack_character_texts(text)
    if not text: return None
    # END OF TEXT HACK

    return text



def parse_dialogue(text):
    text = text.strip()

    # TEXT HACK
    # This is only to fix obvious mistakes and remove stuff
    text = hack_dialogue_texts(text)
    if not text: return None
    # END OF TEXT HACK

    return text



def join_dialogue(texts):
    paragraphs = []
    text_lines = []

    if get_dialogue_type(texts) == 'dialogue':
        texts = [' '.join(texts)]

    for rawtext in texts:
        lines = rawtext.split('\n')

        for line in lines:
            if line.strip():
                text_lines.append(line.strip())
            else:
                if text_lines:
                    paragraphs.append(text_lines)
                    text_lines = []

        if text_lines:
            paragraphs.append(text_lines)
            text_lines = []


    return paragraphs



def get_dialogue_type(texts):
    if texts == ['HEI, JA!']:                    return 'dialogue'
    if texts == ['NEI! MARIT!']:                 return 'dialogue'
    if ''.join(texts)[0] == '(':                 return 'parenthetical'
    if re.search('VERS ', ''.join(texts)):       return 'comment'
    if ''.join(texts).upper() == ''.join(texts): return 'song'

    return 'dialogue'



def commit_dialogue(current_characters, text_buffer, text_index):
    if len(current_characters) == 0: return text_index
    if len(text_buffer       ) == 0: return text_index

    print('')
    print(current_characters)

    paras = join_dialogue(text_buffer)

    for para in paras:
        type = get_dialogue_type(para)
        for text in para:
            text = fix_text_case(text)

            texts.append(text)

            print(type, [text])
            text_index += 1
            sql_insert_text(text, type, text_index)


    current_characters.clear()
    text_buffer.clear()
    return text_index



def parse_content(paragraphs):
    scene_index = 0
    scene_id = None

    block_index = 0
    text_index = 0

    current_characters = []
    text_buffer = []



    for para in paragraphs:
        style = para.find('.//style').get('basestyle', '')
        text = para.find('.//text').text or ''

        if style == 'Scene Heading':
            scene = parse_scene(text)
            if scene:
                text_index = commit_dialogue(current_characters, text_buffer, text_index)
                current_characters.clear()
                scenes.append(scene)
                scene_index += 1
                scene_id = sql_insert_scene(scene, scene_index)
                block_index = 0


        if style == 'Action':
            text = parse_action(text)
            if text:
                text_index = commit_dialogue(current_characters, text_buffer, text_index)
                current_characters.clear()
                text_index += 1
                sql_insert_text(text, 'action', text_index)


        if style == 'Character':
            character = parse_character(text)
            if character:
                text_index = commit_dialogue(current_characters, text_buffer, text_index)
                current_characters.append(character)
                block_index += 1


        if style == 'Dialogue':
            text = parse_dialogue(text)
            if text:
                text_buffer.append(text)

    commit_dialogue(current_characters, text_buffer, text_index)



def parse_xml(input):
    tree = ET.parse(input)
    root = tree.getroot()

    paragraphs = root.findall('.//paragraphs/para')

    fetch_characters()
    pprint(characters)

    parse_content(paragraphs)

    remove_scenes()
    remove_texts()



if __name__ == '__main__':
    db = mysql.connector.connect(
        host='localhost',
        port='8889',
        user='showmaster',
        password='showmaster',
        database='Maridalsspillet_2025',
    )

    getversion()
    print(version)

    parse_xml(sys.stdin)
