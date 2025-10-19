#!/usr/bin/python3

import sys

from sql    import DB
from parser import Parser

from pprint import pprint
from copy   import deepcopy



if __name__ == '__main__':
    db = DB()
    db.connect()

    data = {
        'characters': db.get_characters(),
    }

    parser = Parser(sys.stdin)
    parser.add_db_data(data)

    content = parser.parse()

    # Extract all scenes, then create all new and expire all missing or changed
    scene_list = [{ 'id': scene['id'], 'scene_order': index+1, 'name': ''.join(scene['name'])} for index, scene in enumerate([element for element in content if element['content_type'] == 'scene'])]
    db.create_and_expire_scenes(scene_list)

    content_list = []

    current = {
        'content_type':       None,

        'scene_order':        0,
        'block_order':        0,
        'division_order':     0,
        'paragraph_order':    0,
        'content_order':      0,

        'scene_id':           None,
        'block_id':           None,
        'division_id':        None,
        'paragraph_id':       None,
        'character_alias_id': None,
        'text_type':          None,
        'text':               None,
    }

    for element in content:
        current['content_type'] = element['content_type']
        if current['content_type'] == 'scene':
            current['scene_order']    += 1
            current['block_order']     = 0
            current['division_order']  = 0
            current['paragraph_order'] = 0
            current['content_order']   = 0
            current['character_alias_id'] = None

            current['scene_id'] = db.get_scene_id(element['id'])


        if current['content_type'] in ['character', 'dialogue', 'action']:
            current['block_order']    += 1
            current['division_order']  = 0
            current['paragraph_order'] = 0
            current['content_order']   = 0
            current['character_alias_id'] = None


        if current['content_type'] == 'character':
            current['division_order']  += 1
            current['paragraph_order'] += 1

            character_alias_id = db.get_character_alias_id(element['name'])
            current['character_alias_id'] = character_alias_id['character_alias_id']


        if current['content_type'] in ['dialogue', 'action']:
            if current['content_type'] == 'action': current['character_alias_id'] = None

            current['division_order']  += 1
            current['paragraph_order'] += 1

            for lines in element['lines']:
                text_type = lines['text_type']
                for text in lines['line']:
                    current['content_order'] += 1
                    current['text_type'    ]  = text_type
                    current['text'         ]  = text
#                    current['text_id'] = db.get_text_id_or_insert(text_type, text)

                    content_list.append(deepcopy(current))


#    pprint(content_list)
#    db.create_and_expire_content(content_list)



    for content in content_list:
        db.create_content({
            'scene_id':           content['scene_id'          ],
            'block_order':        content['block_order'       ],
            'division_order':     content['division_order'    ],
            'paragraph_order':    content['paragraph_order'   ],
            'content_order':      content['content_order'     ],
            'character_alias_id': content['character_alias_id'],
            'text_type':          content['text_type'         ],
            'text':               content['text'              ],
        })