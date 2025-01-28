import argparse
import json
import copy
import pathlib

from ordered_set import OrderedSet
from pprint import pprint






def load_data(file_path, show=None):
    result = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        result = json.load(f)

    if show:
        show = result.get(show, {})
        result = result.get('static', {})

        for key in show:
            result[key] = show[key]

    return result



def save_json(path, filename, data):
    fullpath = pathlib.Path(path)
    fullname = fullpath / filename

    fullpath.mkdir(parents=True, exist_ok=True)

    with open(fullname, "w") as outfile:
        json.dump(data, outfile, ensure_ascii=False)
        print(f'JSON data saved to: {fullname}')



def get_target_page(source):
    for page in pages:
        if page['source'] == str(source):
            return page['target']

    return None



def test_removed_location(page, y):
    removed_parts = manus.get('remove_parts', [])

    if not str(page).isnumeric(): return True
    if get_target_page(page) == None: return True

    location = get_location(page, y)

    for row in removed_parts:
        start_location = get_location(row['start']['page']['source'], row['start']['y'])
        end_location   = get_location(row['end'  ]['page']['source'], row['end'  ]['y'])

        if not start_location['target'] or not end_location['target']:
            return True

        if location['target'] >= start_location['target'] and location['target'] <= end_location['target']:
            return True

    return False



def get_location(source, y):
    if y == 1.000: y = 0.9999

    target = get_target_page(source)
    if target: target = round(int(target) + y, 4)

    if str(source).isnumeric(): source = round(int(source) + y, 4)
    else: source = None

    return {
        'source': source,
        'target': target,
    }



def get_current(location, data):
    result = {}

    for row in data:
        if not location['target'] or not row['location']['target']: continue

        if row['location']['target'] <= location['target']:
            result = row

    return result






def generate_pagemap(manus):
    result = []

    last_page    = manus.get('last_page', 1)
    extra_pages  = manus.get('extra_pages', [])
    named_pages  = manus.get('named_pages', [])
    remove_pages = manus.get('remove_pages', [])


    # Create a simple one to one map for all pages from 1 to last_page
    for page in range(1, int(last_page) + 1):
        result.append({ 'target': page, 'source': str(page) })


    # Remove pages
    # For each page after the removal, decrease the target page number
    for page_range in remove_pages:
        for remove_page in range(int(page_range['start']['page']), int(page_range['end']['page']) + 1):
            for page in result:
                if page['source'] == str(remove_page):
                    index = result.index(page)
                    result.remove(page)

                    for laterpage in range(index, len(result)):
                        result[laterpage]['target'] -= 1


    # Add extra pages
    # For each page after the addition, increase the target page number
    offset = 0
    for page in extra_pages:
        after_page = int(page['after']) + offset
        offset += 1

        result.insert(after_page, { 'source': page['name'], 'target': after_page })
        for laterpage in result[after_page:]:
            laterpage['target'] += 1


    # Name all pages in named_pages
    for page in result:
       for named in named_pages:
            if named['page'] == page['source']:
                page['name'] = named['name']


    return result






def generate_pagetext(manus):
    result = []

    for text in manus.get('page_text', []):
        text['location'] = get_location(text['page'], text['y'])
        text['page'] = { 'source': text['page'], 'target': get_target_page(text['page']) }
        text['lines'] = text.get('lines', [])

        result.append(text)

    return result






def generate_extra_pages(manus):
    result = []

    for page in manus.get('extra_pages', []):
        result.append(page)

    return result






def generate_remove_pages(manus):
    result = OrderedSet()

    for page_range in manus.get('remove_pages', []):
        start = int(page_range['start']['page'])
        end   = int(page_range['end'  ]['page'])

        for page in range(start, end + 1):
            result.append(page)

    return reversed(list(result))






def generate_remove_parts(manus):
    result = []

    for part in manus.get('remove_parts', []):
        part['start']['location'] = get_location(part['start']['page'], part['start']['y'])
        part['end'  ]['location'] = get_location(part['end'  ]['page'], part['end'  ]['y'])

        part['start']['page'] = { 'source': part['start']['page'], 'target': get_target_page(part['start']['page']) }
        part['end'  ]['page'] = { 'source': part['end'  ]['page'], 'target': get_target_page(part['end'  ]['page']) }

        result.append(part)

    return result






def generate_extra_lines(manus):
    result = []

    for line in manus.get('extra_lines', []):
        line = copy.deepcopy(line)
        line['location'] = get_location(line['page'], line['y'])
        line['page'] = { 'source': line['page'], 'target': get_target_page(line['page']) }

        result.append(line)

    return result






def generate_actmap(manus):
    result = []

    for act in manus.get('acts'):
        act['start']['location'] = get_location(act['start']['page'], act['start']['y'])
        act['end'  ]['location'] = get_location(act['end'  ]['page'], act['end'  ]['y'])

        act['start']['page'] = { 'source': act['start']['page'], 'target': get_target_page(act['start']['page']) }
        act['end'  ]['page'] = { 'source': act['end'  ]['page'], 'target': get_target_page(act['end'  ]['page']) }

        result.append(act)

    return result





def generate_musicmap(manus):
    result = []

    for music in manus.get('music', []):
        music['start']['location'] = get_location(music['start']['page'], music['start']['y'])
        music['end'  ]['location'] = get_location(music['end'  ]['page'], music['end'  ]['y'])

        music['start']['page'] = { 'source': music['start']['page'], 'target': get_target_page(music['start']['page']) }
        music['end'  ]['page'] = { 'source': music['end'  ]['page'], 'target': get_target_page(music['end'  ]['page']) }

        result.append(music)

    return result






def generate_acdl_map(acdl):
    result = {}

    for role in acdl:
        result[role] = []

        for location in acdl[role]:
            location['location'] = get_location(location['page'], location['y'])
            location['page'] = { 'source': location['page'], 'target': get_target_page(location['page']) }

            result[role].append(location)

    return result






def generate_ecdl_map(ecdl):
    result = {}

    for role in ecdl:
        result[role] = []

        for location in ecdl[role]:
            location['location'] = get_location(location['page'], location['y'])
            location['page'] = { 'source': location['page'], 'target': get_target_page(location['page']) }

            result[role].append(location)


    return result






def generate_scdl_map(scdl):
    result = {}

    for scene in scdl:
        result[scene] = {}

        for role in scdl[scene]:
            result[scene][role] = []

            for location in scdl[scene][role]:
                location['location'] = get_location(location['page'], location['y'])
                location['page'] = { 'source': location['page'], 'target': get_target_page(location['page']) }

                result[scene][role].append(location)


    return result






def generate_lines(manus):
    result = []
    all_lines = []


    for line in manus.get('lines', []):
        if test_removed_location(line['page'], line['y']):
            print('REMOVING LINE at', line['page'], line['y'])
            continue

        all_lines.append(line)


    all_lines += manus.get('extra_lines', [])
    for line in all_lines:
        line['location'] = get_location(line['page'], line['y'])
        line['page'] = { 'source': line['page'], 'target': get_target_page(line['page']) }

        if 'ensembles' in line:
            line['ensemble'] = OrderedSet()

            for ensemble in line['ensembles']:
                current = get_current(line['location'], ensembles[ensemble])

                if 'roles' in current:
                    line['ensemble'].update(current['roles'])

            line['ensemble'] = list(line['ensemble'])

        result.append(line)

    return result






def generate_scenes(manus, lines):
    result = []

    for scene in manus.get('scenes', []):
        scene['start']['location'] = get_location(scene['start']['page'], scene['start']['y'])
        scene['end'  ]['location'] = get_location(scene['end'  ]['page'], scene['end'  ]['y'])

        scene['start']['page'] = { 'source': scene['start']['page'], 'target': get_target_page(scene['start']['page']) }
        scene['end'  ]['page'] = { 'source': scene['end'  ]['page'], 'target': get_target_page(scene['end'  ]['page']) }

        scene['roles'   ] = OrderedSet()
        scene['ensemble'] = OrderedSet()

        for line in lines:
            if line['location']['target'] >= scene['start']['location']['target'] and line['location']['target'] <= scene['end']['location']['target']:
                scene['roles'].update(line.get('roles', []))
                scene['ensemble'].update(line.get('ensemble', []))

        scene['roles'   ] = list(scene['roles'   ])
        scene['ensemble'] = list(scene['ensemble'])

        result.append(scene)


    return result






def generate_staging(scdl, scenes, music, lines):
    result = {
        'scenes': {},
        'music':  {},
    }

    for scene in scenes:
        result['scenes'][scene['id']] = {}

        scene_start = scene['start']['location']['target']
        scene_end   = scene['end'  ]['location']['target']


        for line in [line for line in lines if line['location']['target'] >= scene_start and line['location']['target'] <= scene_end]:
            for role in line.get('roles', []) + line.get('ensemble', []):
                if role == 'Backstage-kor': continue

                result['scenes'][scene['id']][role] = [
                    { 'location': scene['start']['location'], 'page': scene['start']['page'], 'y': scene['start']['y'], 'action': 'enter' },
                    { 'location': scene['end'  ]['location'], 'page': scene['end'  ]['page'], 'y': scene['end'  ]['y'], 'action': 'exit'  }
                ]

    for scene in scdl:
        for role in scdl[scene]:
            if role == 'Backstage-kor': continue

            cdl = scdl[scene][role]

            if cdl[0]['action'] == 'enter' and cdl[len(cdl) - 1]['action'] == 'exit':
                result['scenes'][scene][role] = cdl
            elif cdl[0]['action'] == 'enter':
                result['scenes'][scene][role][0:1] = cdl
            elif cdl[0]['action'] == 'exit':
                result['scenes'][scene][role][1:] = cdl


    for song in music:
        result['music'][song['id']] = {}

        song_start = song['start']['location']['target']
        song_end   = song['end'  ]['location']['target']

        for line in [line for line in lines if line['location']['target'] >= song_start and line['location']['target'] <= song_end]:
            for role in line.get('roles', []) + line.get('ensemble', []):
                if role != 'Backstage-kor': continue

                result['music'][song['id']][role] = [
                    { 'location': song['start']['location'], 'page': song['start']['page'], 'y': song['start']['y'], 'action': 'enter' },
                    { 'location': song['end'  ]['location'], 'page': song['end'  ]['page'], 'y': song['end'  ]['y'], 'action': 'exit'  }
                ]


    return result






def generate_mcdl(lines, ensembles, actors, staging, mics):
    result = {}

    for role in mics['exclusive_assignments']:
        if not role in result: result[role] = []

    for role in mics['fixed_assignments']:
        if not role in result: result[role] = []


    for scene in staging['scenes']:
        for role in staging['scenes'][scene]:
            mic, actor = None, None

            if role in mics['exclusive_assignments']: mic = mics['exclusive_assignments'][role]
            if role in mics['fixed_assignments'    ]: mic = mics['fixed_assignments'    ][role]

            for action in staging['scenes'][scene][role]:
                current = list(filter(lambda x: x['location']['target'] <= action['location']['target'], actors[role])).pop()
                actor = current['actor']

                if action['action'] == 'enter':
                    if len(result[role]) == 0:
                        result[role].append({ 'start': { 'location': action['location'], 'page': action['page'], 'y': action['y'] }, 'end': None, 'actor': actor, 'mic': mic })

                    else:
                        prev_end = result[role][len(result[role]) - 1]['end']['location'].get('target', 0)
                        this_start = action['location']['target']

                        if (this_start - prev_end) > 0.5:
                            result[role].append({ 'start': { 'location': action['location'], 'page': action['page'], 'y': action['y'] }, 'end': None, 'actor': actor, 'mic': mic })

                elif action['action'] == 'exit':
                    result[role][len(result[role]) - 1]['end'] = { 'location': action['location'], 'page': action['page'], 'y': action['y'] }


    for music in staging['music']:
        for role in staging['music'][music]:
            mic, actor = None, None

            if role in mics['exclusive_assignments']: mic = mics['exclusive_assignments'][role]
            if role in mics['fixed_assignments'    ]: mic = mics['fixed_assignments'    ][role]

            for action in staging['music'][music][role]:
                current = list(filter(lambda x: x['location']['target'] <= action['location']['target'], actors[role])).pop()
                actor = current['actor']

                if action['action'] == 'enter':
                    if len(result[role]) == 0:
                        result[role].append({ 'start': { 'location': action['location'], 'page': action['page'], 'y': action['y'] }, 'end': None, 'actor': actor, 'mic': mic })

                    else:
                        prev_end = result[role][len(result[role]) - 1]['end']['location'].get('target', 0)
                        this_start = action['location']['target']

                        if (this_start - prev_end) > 0.5:
                            result[role].append({ 'start': { 'location': action['location'], 'page': action['page'], 'y': action['y'] }, 'end': None, 'actor': actor, 'mic': mic })

                elif action['action'] == 'exit':
                    result[role][len(result[role]) - 1]['end'] = { 'location': action['location'], 'page': action['page'], 'y': action['y'] }


    return result






def generate_micmap(mcdl):
    result = [{ 'location': { 'source': 1.0, 'target': 1.0 }, 'page': { 'source': '1', 'target': 1 }, 'y': 0.0, 'mics': { mic: { 'role': None, 'actor': None } for mic in mics.get('mics') } }]

    temp_cdl = []
    for role in mcdl:
        for mcd in mcdl[role]:
            temp_cdl.append({
                'location': mcd['start']['location'],
                'page':     mcd['start']['page'],
                'y':        mcd['start']['y'],
                'mic':      mcd['mic'],
                'actor':    mcd['actor'],
                'role':     role,
            })
            temp_cdl.append({
                'location': mcd['end']['location'],
                'page':     mcd['end']['page'],
                'y':        mcd['end']['y'],
                'mic':      mcd['mic'],
                'actor':    None,
                'role':     None,
            })

    def location(x): return x['location']['target']
    temp_cdl.sort(key=location)


    for cdl in temp_cdl:
        if abs(cdl['location']['target'] - result[len(result) - 1]['location']['target']) < 0.1:
            row = result.pop()
        else:
            row = copy.deepcopy(result[len(result) - 1])
            row['location'] = cdl['location']
            row['page']     = cdl['page']
            row['y']        = cdl['y']

        row['mics'][str(cdl['mic'])]['role' ] = cdl['role']
        row['mics'][str(cdl['mic'])]['actor'] = cdl['actor']

        result.append(row)


    return result






def compile_commondata(shows):
    result = {
        'showdata': {},
        'pdf':      {},
    }

    for show in shows:
        result['pdf']['empty'] = { 'url': f'pdf/manus-empty.pdf', 'name': 'original'   }
        result['pdf']['music'] = { 'url': f'pdf/manus-music.pdf', 'name': 'musikk'     }
        result['pdf']['mics' ] = { 'url': f'pdf/manus-mics.pdf',  'name': 'mikrofoner' }

        result['pdf']['actor:mic/role' ] = { 'url': f'pdf/actor-mic-role.pdf',  'name': 'skuespiller: mikrofon/rolle' }
        result['pdf']['role:mic/actor' ] = { 'url': f'pdf/role-mic-actor.pdf',  'name': 'rolle: mikrofon/skuespiller' }
        result['pdf']['mic:actor/role' ] = { 'url': f'pdf/mic-actor-role.pdf',  'name': 'mikrofon: skuespiller/rolle' }
        result['pdf']['mic:role/actor' ] = { 'url': f'pdf/mic-role-actor.pdf',  'name': 'mikrofon: rolle/skuespiller' }

        result['showdata'][show] = {
            'url':    f'data/{show}/showdata.json',
            'name':   shows[show]['name'  ],
            'date':   shows[show]['date'  ],
            'time':   shows[show]['time'  ],
            'durata': shows[show]['durata'],
        }

    return result






def compile_showdata(shows, pages, micmap, acts):
    result = {
        'showinfo':     shows.get(show, {}),

        'pagemap':      [{ 'target': p['target'], 'source': p['source'], 'name': p.get('name', None) } for p in pages],

        'miclist':      [ x for x in mics.get('mics') ],

        'micmap':       [{  'location': x.get('location', 0.0),
                            'page':     x.get('page', 0),
                            'y':        x.get('y', 0.0),
                            'mics':     x.get('mics'),
                        } for x in micmap],

        'rolemic':      { role: [{
                            'start': {
                                'location': x.get('start', {}).get('location', {}),
                                'page':     x.get('start', {}).get('page', 0),
                                'y':        x.get('start', {}).get('y', 0.0),
                            },
                            'end': {
                                'location': x.get('end', {}).get('location', {}),
                                'page':     x.get('end', {}).get('page', 0),
                                'y':        x.get('end', {}).get('y', 0.0),
                            },
                            'actor': x.get('actor', None),
                            'mic':   x.get('mic', None),
                        } for x in mcdl[role]] for role in mcdl},

        'acts':         [{  'id':   x.get('id'),
                            'name': x.get('name'),
                            'start': {
                                'location': x.get('start', {}).get('location', {}),
                                'page':     x.get('start', {}).get('page', 0),
                                'y':        x.get('start', {}).get('y', 0.0),
                            },
                            'end': {
                                'location': x.get('end', {}).get('location', {}),
                                'page':     x.get('end', {}).get('page', 0),
                                'y':        x.get('end', {}).get('y', 0.0),
                            },
                        } for x in acts],

        'scenes':       [{  'id':   x.get('id'),
                            'name': x.get('name'),
                            'start': {
                                'location': x.get('start', {}).get('location'),
                                'page':     x.get('start', {}).get('page', 0),
                                'y':        x.get('start', {}).get('y', 0.0),
                            },
                            'end': {
                                'location': x.get('end', {}).get('location', {}),
                                'page':     x.get('end', {}).get('page', 0),
                                'y':        x.get('end', {}).get('y', 0.0),
                            },
                            'roles':    x.get('roles', []),
                            'ensemble': x.get('ensemble', []),
                        } for x in scenes],

        'lines':        [{  'location':  x.get('location', 0.0),
                            'page':      x.get('page', 0),
                            'y':         x.get('y', 0.0),
                            'roles':     x.get('roles', []),
                            'ensemble' : x.get('ensemble', []),
                            'ensembles': x.get('ensembles', []),
                         } for x in lines],

        'music':        [{  'id':   x.get('id'),
                            'name': x.get('name'),
                            'type': x.get('type'),
                            'start': {
                                'location': x.get('start', {}).get('location'),
                                'page':     x.get('start', {}).get('page', 0),
                                'y':        x.get('start', {}).get('y', 0.0),
                            },
                            'end': {
                                'location': x.get('end', {}).get('location', {}),
                                'page':     x.get('end', {}).get('page', 0),
                                'y':        x.get('end', {}).get('y', 0.0),
                            },
                        } for x in music],

        'pagetext':     [{  'location':  x.get('location', 0.0),
                            'page':      x.get('page', 0),
                            'y':         x.get('y', 0.0),
                            'heading':   x.get('heading'),
                            'lines':     x.get('lines'),
                        } for x in pagetext],

        'remove_pages': [ x for x in remove_pages ],

        'remove_parts': [{  'start': {
                                'location': x.get('start', {}).get('location'),
                                'page':     x.get('start', {}).get('page', 0),
                                'y':        x.get('start', {}).get('y', 0.0),
                            },
                            'end': {
                                'location': x.get('end', {}).get('location', {}),
                                'page':     x.get('end', {}).get('page', 0),
                                'y':        x.get('end', {}).get('y', 0.0),
                            },
                        } for x in remove_parts ],

        'extra_pages':  [{  'name':  x.get('name'),
                            'after': x.get('after'),
                        } for x in extra_pages],

        'extra_lines':  [{  'location':  x.get('location', 0.0),
                            'page':      x.get('page', 0),
                            'y':         x.get('y', 0.0),
                            'roles':     x.get('roles', []),
                            'ensembles': x.get('ensembles', []),
                            'lines':     x.get('lines'),
                        } for x in extra_lines],
    }


    return result






if __name__ == "__main__":
    # Common data
    shows = load_data('data/sources/shows.json')
    manus = load_data('data/sources/manus.json')
    mics  = load_data('data/sources/mics.json')

    pages    = generate_pagemap(manus)
    pagetext = generate_pagetext(manus)
    acts     = generate_actmap(manus)
    music    = generate_musicmap(manus)

    commondata = compile_commondata(shows)
    save_json('data/compiled/showdata/', 'shows.json', commondata)


    # Per-show data
    for show in shows:
        manus = load_data('data/sources/manus.json')
        mics  = load_data('data/sources/mics.json')

        pages        = generate_pagemap(manus)
        pagetext     = generate_pagetext(manus)
        extra_pages  = generate_extra_pages(manus)
        remove_pages = generate_remove_pages(manus)
        remove_parts = generate_remove_parts(manus)
        extra_lines  = generate_extra_lines(manus)
        acts         = generate_actmap(manus)
        music        = generate_musicmap(manus)

        acdl = load_data('data/sources/acdl.json', show)
        ecdl = load_data('data/sources/ecdl.json', show)
        scdl = load_data('data/sources/scdl.json', show)

        ensembles = generate_ecdl_map(ecdl)
        actors    = generate_acdl_map(acdl)
        scdl      = generate_scdl_map(scdl)

        lines   = generate_lines(manus)
        scenes  = generate_scenes(manus, lines)
        staging = generate_staging(scdl, scenes, music, lines)

        mcdl   = generate_mcdl(lines, ensembles, actors, staging, mics)
        micmap = generate_micmap(mcdl)

        showdata = compile_showdata(shows, pages, micmap, acts)
        save_json(f'data/compiled/showdata/{show}/', 'showdata.json', showdata)


    print(f'All done!')
#    pprint(showdata)
