#!/usr/bin/python3

import argparse
import pymupdf
import json
import re

from copy   import deepcopy
from pprint import pprint



def extract(doc):
    result = []

    for page_number in range(len(doc)):
        page = doc[page_number]
        text_data = page.get_text("dict", sort=True)
        blocks = text_data["blocks"]

        for block in blocks:
            for line in block['lines']:
                x, y = line['spans'][0]['origin']
                textline = {
                    'page': page_number + 1,
                    'x': x,
                    'y': y,
                    'content': [],
                }

                for span in line['spans']:
                    font = {
                        'name':   span.get('font', ''),
                        'size':   span.get('size'),
                        'bold':   'bold'   in span.get('font', '').lower(),
                        'italic': 'italic' in span.get('font', '').lower(),
                    }

                    textline.get('content').append({
                        'font':    font,
                        'text': span.get('text', '')
                    })

                result.append(textline)

    return result



def clean(rawdata):
    result = []

    for line in rawdata:
        content = line.get('content', [])
        print(line)

        if line.get('page') in [1, 2]:
            pass

        elif content[0].get('text').strip() == f'''{line.get('page')}.''':
            pass

        elif content[0].get('text') == '(' or content[0].get('text') == ')':
            pass

        elif content[0].get('text') == '''(cont'd)''':
            pass

        elif content[0].get('text') == '''(MORE)''':
            pass

        elif content[0].get('text') in [
            'tar SIGRUNN til siden',
            'til SIRA LARS',
            'til JON',
            'til Rask',
            'hermer',
            'nølende',
            'henviser til jordet',
            'veldig positiv',
            'viser fram sigden',
            'andpusten',
            'Til knektene',
            'Slår mot Marit.',
            'skriker',
            'til knektene',
            'stillhet',
        ]:
            content[0]['text'] = '(' + content[0].get('text')+ ')'
            result.append(line)

        elif content[0].get('text') == 'SIKA LARS':
            result.append(line)
            content[0]['text'] = 'SIRA LARS'

        elif content[0].get('text') == '#6B - ELSK MENS DU KAN':
            result.append({'page': 31, 'x': 108.13999938964844, 'y': 0, 'content': [{'font': {'name': 'CourierNewPSMT', 'size': 12.0, 'bold': False, 'italic': False}, 'text': '#6B - ELSK MENS DU KAN'}]})

        elif content[0].get('text') == 'SCENE 6B - MARIT BESØKER JON':
            result.append(line)
            result.append({'page': 29, 'x': 252.32000732421875, 'y': 0, 'content': [{'font': {'name': 'CourierNewPSMT', 'size': 12.0, 'bold': False, 'italic': False}, 'text': 'MARIT'}]})

        elif content[0].get('text') == 'SIRA LARS igjen alene.':
            result.append({'page': 46, 'x': 108.13999938964844, 'y': 0, 'content': [{'font': {'name': 'CourierNewPSMT', 'size': 12.0, 'bold': False, 'italic': False}, 'text': 'SIRA LARS igjen alene.'}]})
            result.append({'page': 46, 'x': 252.32000732421875, 'y': 0, 'content': [{'font': {'name': 'CourierNewPSMT', 'size': 12.0, 'bold': False, 'italic': False}, 'text': 'SIRA LARS'}]})

        elif content[0].get('text') == 'Skift stemning: Roligere, lengre linjer i melodien.':
            result.append(line)
            result.append({'page': 46, 'x': 252.32000732421875, 'y': 0, 'content': [{'font': {'name': 'CourierNewPSMT', 'size': 12.0, 'bold': False, 'italic': False}, 'text': 'SIRA LARS (cont\'d)'}]})

        elif content[0].get('text').startswith('VERS '):
            result.append(line)
            result[-1]['x'] = 216.27999877929688

        else:
            result.append(line)

    return result



def parse_roles(data):
    result = []

    roles = [
        'BØNDENE',
        'BØNDER',
        'BONDE 1',
        'BONDE 2',
        'BONDE 3',
        'KNEKTENE',
        'BUDBRINGER',
        'ARNE ASLAKSSON',
        'KNUT RASK',
        'RASK',
        'SIRA LARS',
        'SIGRUNN',
        'OGMUND',
        'UNGE JON',
        'UNGE MARIT',
        'TORDIS',
        'JON',
        'MARIT',
        'BARN 1',
        'BARN',
        'ALLE',
    ]

    roles_regex = r'\b(?:' + '|'.join(re.escape(role) for role in roles) + r')\b'

    for line in data:
        result.append(line)
        oldcontent = deepcopy(line.get('content'))
        line['content'] = []

        for oldelement in oldcontent:
            parts = re.split(f'({roles_regex})', oldelement.get('text'))

            for part in parts:
                if part == '':
                    pass

                elif part in roles:
                    element = {
                        'type': 'role',
                        'text': part,
                        'font': {
                            'size':   oldelement.get('font').get('size'),
                            'bold':   oldelement.get('font').get('bold'),
                            'italic': oldelement.get('font').get('italic'),
                        }
                    }
                    line['content'].append(element)

                else:
                    element = {
                    'type': 'text',
                    'text': part,
                    'font': {
                        'size':   oldelement.get('font').get('size'),
                        'bold':   oldelement.get('font').get('bold'),
                        'italic': oldelement.get('font').get('italic'),
                    }
                }
                    line['content'].append(element)

    return result



def compile(roledata):
    result = []

    structure = None
    dialogue  = None
    last_y    = 0

    for element in roledata:
        if element.get('x') == 108.13999938964844:
            text = ''.join([t.get('text') for t in element.get('content')])

            if text == 'OUVERTURE':
                structure = {
                    'type': 'music',
                    'text': element.get('content'),
                    'content': [],
                }
                result.append(structure)

            elif text == 'SLUTT.':
                structure = {
                    'type': 'end',
                    'text': element.get('content'),
                    'content': [],
                }
                result.append(structure)

            elif text.startswith('SCENE '):
                structure = {
                    'type': 'scene',
                    'text': element.get('content'),
                    'id':   text.removeprefix('SCENE ').split(' - ')[0],
                    'name': text.removeprefix('SCENE ').split(' - ')[1],
                    'content': [],
                }
                result.append(structure)

            else:
                if structure.get('content') and structure.get('content')[-1].get('type') == 'directions' and 0 < (element.get('y') - last_y) < 13:
                    structure.get('content')[-1].get('content').append(element.get('content'))

                else:
                    last_y = element.get('y')
                    structure.get('content').append({
                        'type': 'directions',
                        'mode': 'block',
                        'content': [element.get('content')],
                    })

                last_y = element.get('y')


        elif element.get('x') == 180.22999572753906:
            text = ''.join([t.get('text') for t in element.get('content')])

            if 1 == 2:
                pass

            else:
                mode = 'speech'

                if text.upper() == text:
                    if text == 'HEI, JA!': pass
                    else: mode = 'song'

                if dialogue.get('content') and 0 < (element.get('y') - last_y) < 13:
                    dialogue.get('content')[-1].get('text').append(element.get('content'))

                else:
                    dialogue.get('content').append({
                        'type': 'dialogue',
                        'mode': mode,
                        'text': [element.get('content')],
                    })

            last_y = element.get('y')


        elif element.get('x') == 252.32000732421875:
            text = ''.join([t.get('text') for t in element.get('content')])

            dialogue = {
                'type': 'dialogue',
                'role': text,
                'text': element.get('content'),
                'content': [],
            }
            structure.get('content').append(dialogue)


        elif element.get('x') == 216.27999877929688 or (element.get('content')[0].get('text') in ['(Mumler)', '(parlert)', '(Pause)']):
                dialogue.get('content').append({
                    'type': 'directions',
                    'mode': 'inline',
                    'text': [element.get('content')],
                })

        else:
            print(f'''MISSING CLASSIFICATION: {element}''')

    return result



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("manus")

    args = parser.parse_args()
    manus = args.manus

    doc = pymupdf.open(manus)

    rawdata = extract(doc)
    cleandata = clean(rawdata)
    roledata = parse_roles(cleandata)
    data = compile(roledata)

    with open('manus.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)

    pprint(data)
#    for line in cleandata:
#        print(line.get('content'))
