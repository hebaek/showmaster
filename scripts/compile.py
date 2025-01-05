import fitz  # PyMuPDF
import json
import copy

from datetime import datetime
from collections import defaultdict

import pprint



def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)



def calculate_pagemap(lastpage, acts, scenes, lines, music, data_manus):
    pagemap = []

    for page in range(1, lastpage + 1):
        name = str(page)
        pagemap.append({ 'target': page, 'source': name })

    pages = data_manus.get("extra_pages")
    offset = 0
    for p in pages:
        pagemap.insert(p['after'] + offset, { 'source': p['name'], 'target': p['after'] + offset })
        for p in pagemap[p['after'] + offset:]:
            p['target'] += 1

        offset += 1


    for p in pagemap:
        for named in data_manus.get("named_pages"):
            if named['page'] == p['source']:
                p['name'] = named['name']


    return pagemap



def calculate_ensemblemap(ecdl):
    result = {}

    for key in list(ecdl.keys()):
        result[key] = [{ 'page': '1', 'y': 0.0, 'roles': [], 'extras': [] }]

        for ecd in ecdl[key]:
            popped = False

            if str(ecd['page']) == str(result[key][-1]['page']) and ecd['y'] == result[key][-1]['y']:
                newline = result[key].pop()
                popped = True
            else:
                newline = copy.deepcopy(result[key][-1])
                newline['page'  ] = ecd['page']
                newline['y'     ] = ecd['y']

            if popped or set(ecd.get('roles', [])) != set(newline['roles']) or set(ecd.get('extras', [])) != set(newline['extras']):
                result[key].append(ecd)

    for ensemble in result:
        print(ensemble)

        for line in result[ensemble]:
            print(line)

    return result



def calculate_micmap(mcdl):
    result = []

    allmics = sorted(set([mic['mic'] for mic in mcdl]))

    result.append({ 'page': '1', 'y': 0.0, 'mics': { m: { 'role': None, 'actor': None} for m in allmics } })

    for mcd in mcdl:
        if str(mcd['page']) == str(result[-1]['page']) and mcd['y'] == result[-1]['y']:
            newline = result.pop()
        else:
            newline = copy.deepcopy(result[-1])
            newline['page'] = mcd['page']
            newline['y'   ] = mcd['y']

        newline['mics'][mcd['mic']]['role' ] = mcd['role' ]
        newline['mics'][mcd['mic']]['actor'] = mcd['actor']

        result.append(newline)

    return result



def compile(data_manus, data_music, ecdl, mcdl):
    lastpage = data_manus.get('lastpage')
    acts     = data_manus.get('acts')
    scenes   = data_manus.get('scenes')
    lines    = data_manus.get('lines')
    music    = data_music.get('music')

    pagemap     = calculate_pagemap(lastpage, acts, scenes, lines, music, data_manus)
    ensemblemap = calculate_ensemblemap(ecdl)
    micmap      = calculate_micmap(mcdl)

    def get_target_page(source):
        hits = (p for p in pagemap if p.get('source') == str(source))
        return next(hits)['target']



    result = {
        'showtime':     '2025-01-02 02:00:00Z',

        'pagemap':      [{ 'target': p['target'], 'source': p['source'], 'name': p.get('name', None) } for p in pagemap],

        'ensemblemap':  { ensemble: [
                            {
                                'location': {
                                    'page':   get_target_page(x.get('page', 0)),
                                    'y':      float(x.get('y', 0.0)),
                                },
                                'roles':  x.get('roles', []),
                                'extras': x.get('extras', [])
                            } for x in ensemblemap[ensemble]
                        ] for ensemble in ensemblemap },

        'micmap':       [{  'location': {
                                'page': get_target_page(x.get('page', 0)),
                                'y':    float(x.get('y', 0.0)),
                            },
                            'mics': x.get('mics'),
                        } for x in micmap],

        'acts':         [{  'id':   x.get('id'),
                            'name': x.get('name'),
                            'start': {
                                'page': get_target_page(x.get('start', {}).get('page', 0)),
                                'y':    float(x.get('start', {}).get('y', 0.0)),
                            },
                            'end': {
                                'page': get_target_page(x.get('end', {}).get('page', 0)),
                                'y':    float(x.get('end', {}).get('y', 0.0)),
                            },
                        } for x in acts],

        'scenes':       [{  'id':   x.get('id'),
                            'name': x.get('name'),
                            'start': {
                                'page': get_target_page(x.get('start', {}).get('page', 0)),
                                'y':    float(x.get('start', {}).get('y', 0.0)),
                            },
                            'end': {
                                'page': get_target_page(x.get('end', {}).get('page', 0)),
                                'y':    float(x.get('end', {}).get('y', 0.0)),
                            },
                        } for x in scenes],

        'lines':        [{  'location': {
                                'page': get_target_page(x.get('page', 0)),
                                'y':    float(x.get('y', 0.0)),
                            },
                            'roles':     x.get('roles', []),        # + mic + actor, based on ecdl
                            'ensembles': x.get('ensembles', []),    # + mic + actor, based on ecdl
                         } for x in lines],

        'music':        [{  'id':   x.get('id'),
                            'name': x.get('name'),
                            'type': x.get('type'),
                            'start': {
                                'page': get_target_page(x.get('start', {}).get('page', 0)),
                                'y':    float(x.get('start', {}).get('y', 0.0)),
                            },
                            'end': {
                                'page': get_target_page(x.get('end', {}).get('page', 0)),
                                'y':    float(x.get('end', {}).get('y', 0.0)),
                            },
                        } for x in music]
    }


    return result



def create_pdf(original, output, data_manus, data):
    doc = fitz.open(original)


    def add_text(page, y, texts):
        y = 200
        for text in texts:
            page.insert_textbox(
                (page.rect.width / 2 - 200, y, page.rect.width / 2 + 200, y + 28),
                text,
                fontsize=16,
                align=1,
                color=(0, 0, 0),
                fontname="Times-Bold"
            )
            y = y + 28

    pages = data_manus.get("extra_pages")
    offset = 0
    for p in pages:
        page = doc[p['after'] + offset]
        page_width, page_height = page.rect.width, page.rect.height
        page = doc.new_page(pno = p['after'] + offset, width=page_width, height=page_height)

        page.insert_textbox((page.rect.width / 2, 779, page.rect.width / 2 + 218, 810), 'Side ' + p['name'], fontsize=12, align=2, color=(0, 0, 0), fontname="Times-Bold")
        offset += 1

    texts = data_manus.get("page_texts")
    for t in texts:
        pagenumber = [page['target'] for page in data['pagemap'] if page['source'] == t['page']][0]
        page = doc[pagenumber - 1]

        x1, x2 = page.rect.width / 2 - 200, page.rect.width / 2 + 200
        y1, y2 = float(t['y']) * page_height, float(t['y']) * page_height + 28
        page.insert_textbox(
            (x1, y1, x2, y2),
            t['heading'],
            fontsize=16,
            align=1,
            color=(0, 0, 0),
            fontname="Times-Bold"
        )

        y1 += 30
        y2 += 30
        for line in t['lines']:
            y1 += 20
            y2 += 20
            page.insert_textbox(
                (x1, y1, x2, y2),
                line,
                fontsize=12,
                align=1,
                color=(0, 0, 0),
                fontname="Times-Roman"
            )


    doc.save(output)
    print(f"Annotated PDF saved to: {output}")




if __name__ == "__main__":
    pdf_original = "data/originals/manus.pdf"
    pdf_output   = "data/compiled/manus-expanded.pdf"

    data_manus = load_json('data/sources/manus.json')
    data_music = load_json('data/sources/music.json')
    data_ecdl  = load_json('data/sources/ecdl.json')
    data_mcdl  = load_json('data/sources/mcdl.json')

    data = compile(data_manus, data_music, data_ecdl, data_mcdl)

    # Print the result
    pprint.pprint(data)

    with open('data/compiled/compiled.json', "w") as outfile:
        pprint.pprint(json.dump(data, outfile))
        print(f"JSON data saved to: {'compiled.json'}")

    create_pdf(pdf_original, pdf_output, data_manus, data)
