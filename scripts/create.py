import argparse
import json
import pymupdf
import pathlib

import locale

from datetime import datetime
from pprint   import pprint



mm = None






def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)



def save_pdf(path, filename, doc):
    fullpath = pathlib.Path(path)
    fullname = fullpath / filename

    fullpath.mkdir(parents=True, exist_ok=True)

    doc.save(fullname, garbage=4, deflate=True, use_objstms=True)
    doc.close()

    print(f'PDF saved to: {fullname}')






def setup(w, h):
    global mm
    mm = 420 / w

    p = {
        'page':    { 'top':     0/mm, 'bottom': 297/mm, 'left':  0/mm, 'right': 420/mm },
        'margins': { 'top':    10/mm, 'bottom':  10/mm, 'left': 10/mm, 'right':  10/mm },
        'header':  { 'height':  6/mm, 'padding':  2/mm },
        'footer':  { 'height':  5/mm, 'padding':  0/mm },
        'scenes':  { 'height': 13/mm, 'padding':  2/mm },
        'music':   { 'height': 13/mm, 'padding':  2/mm },
        'leader':  { 'width':  40/mm, 'padding':  2/mm }
    }

    result = {}
    result['header'] = {
        'left':   p['page']['left' ] + p['margins']['left' ],
        'right':  p['page']['right'] - p['margins']['right'],
        'top':    p['page']['top'  ] + p['margins']['top'  ],
        'bottom': p['page']['top'  ] + p['margins']['top'  ] + p['header']['height'],
    }

    result['footer'] = {
        'left':   p['page']['left'  ] + p['margins']['left'  ],
        'right':  p['page']['right' ] - p['margins']['right' ],
        'top':    p['page']['bottom'] - p['margins']['bottom'] - p['footer']['height'],
        'bottom': p['page']['bottom'] - p['margins']['bottom'],
    }

    result['info'] = {
        'left':   p['page']['left'] + p['margins']['left'],
        'right':  p['page']['left'] + p['margins']['left'] + p['leader']['width'],
        'top':    result['header']['bottom'] + p['header']['padding'],
        'bottom': result['header']['bottom'] + p['header']['padding'] + p['scenes']['height'] + p['scenes']['padding'] + p['music']['height'],
    }

    result['scenes'] = {
        'left':   p['page']['left' ] + p['margins']['left' ] + p['leader']['width'] + p['leader']['padding'],
        'right':  p['page']['right'] - p['margins']['right'],
        'top':    result['header']['bottom'] + p['header']['padding'],
        'bottom': result['header']['bottom'] + p['header']['padding'] + p['scenes']['height'],
    }

    result['music'] = {
        'left':   p['page']['left' ] + p['margins']['left' ] + p['leader']['width'] + p['leader']['padding'],
        'right':  p['page']['right'] - p['margins']['right'],
        'top':    result['scenes']['bottom'] + p['scenes']['padding'],
        'bottom': result['scenes']['bottom'] + p['scenes']['padding'] + p['music']['height'],
    }

    result['leader'] = {
        'left':   p['page']['left'] + p['margins']['left'],
        'right':  p['page']['left'] + p['margins']['left'] + p['leader']['width'],
        'top':    result['info']['bottom'] + p['header']['padding'],
        'bottom': result['footer']['top'] - p['footer']['padding'],
    }

    result['content'] = {
        'left':   result['scenes']['left'],
        'right':  p['page']['right'] - p['margins']['right'],
        'top':    result['music']['bottom'] + p['music']['padding'],
        'bottom': result['footer']['top'] - p['footer']['padding'],
    }

    return result






def mockup(page, p):
    for section in p:
        page.draw_rect((p[section]['left'], p[section]['top'], p[section]['right'], p[section]['bottom']), color=(0.0, 0.0, 1.0), width=0.25)






def draw_static(page, p, data, act):
    locale.setlocale(locale.LC_ALL, locale.setlocale(locale.LC_TIME, 'no_NO'))

    '''
    Header
    '''
    f = p['header']
    width  = f['right' ] - f['left']
    height = f['bottom'] - f['top' ]

    css = f'''
    .header {{
        width:          100%;
        height:         {height}px;
        line-height:    {height}px;

        font-family:    serif;
        font-size:      14px;
        font-weight:    bold;
        vertical-align: top;
    }}
    .left   {{ text-align: left;   }}
    .center {{ text-align: center; }}
    .right  {{ text-align: right;  }}
    '''

    text = {
        'left':   f'''<div class='header left'>{data['showinfo']['name']} &ndash; {data['showinfo']['time']}</div>''',
        'center': f'''<div class='header center'></div>''',
        'right':  f'''<div class='header right'></div>''',
    }

    page.insert_htmlbox((f['left'], f['top'], f['right'], f['bottom']), text['left'  ], css=css)
    page.insert_htmlbox((f['left'], f['top'], f['right'], f['bottom']), text['center'], css=css)
    page.insert_htmlbox((f['left'], f['top'], f['right'], f['bottom']), text['right' ], css=css)

#    page.draw_line((f['left'], f['bottom']), (f['right'], f['bottom']))



    '''
    Footer
    '''
    f = p['footer']
    width  = f['right' ] - f['left']
    height = f['bottom'] - f['top' ]

    css = f'''
    .footer {{
        width:          100%;
        height:         {height}px;
        line-height:    {height}px;

        font-family:    sans-serif;
        font-size:      10px;
        font-weight:    normal;
        vertical-align: bottom;
    }}
    .left   {{ text-align: left;   }}
    .center {{ text-align: center; }}
    .right  {{ text-align: right;  }}
    '''

    date = datetime.now().strftime("%d. %B %Y")
    time = datetime.now().strftime("%H:%M:%S")
    text = {
        'left':   f'''<div class='footer left'>Heksene fra Eastwick</div>''',
        'center': f'''<div class='footer center'>{date} &ndash; {time}</div>''',
        'right':  f'''<div class='footer right'>Sandefjord vgs &ndash; MDD</div>''',
    }

    page.insert_htmlbox((f['left'], f['top'], f['right'], f['bottom']), text['left'  ], css=css)
    page.insert_htmlbox((f['left'], f['top'], f['right'], f['bottom']), text['center'], css=css)
    page.insert_htmlbox((f['left'], f['top'], f['right'], f['bottom']), text['right' ], css=css)

#    page.draw_line((f['left'], f['top']), (f['right'], f['top']))



    '''
    Info
    '''
    f = p['info']
    width  = f['right' ] - f['left']
    height = p['scenes']['bottom'] - f['top' ]

    css = f'''
    .info {{
        width:          100%;
        height:         {height}px;
        line-height:    {height}px;

        font-family:    serif;
        font-size:      36px;
        font-weight:    bold;
        text-align:     left;
        vertical-align: middle;
    }}
    '''

    text = {
        'info': f'''<div class='info'>{act['name']}</div>''',
    }

    page.insert_htmlbox((f['left'], f['top'], f['right'], f['bottom']), text['info'], css=css)



    '''
    Lines
    '''
#    page.draw_line((p['scenes']['left' ], p['scenes']['top'   ]), (p['scenes' ]['right'], p['scenes' ]['top'   ]))
    page.draw_line((p['leader']['left' ], p['leader']['top'   ]), (p['content']['right'], p['content']['top'   ]))
    page.draw_line((p['leader']['left' ], p['leader']['bottom']), (p['content']['right'], p['content']['bottom']))

#    page.draw_line((p['leader']['left' ], p['leader' ]['top'   ]), (p['leader' ]['left' ], p['leader' ]['bottom']))
#    page.draw_line((p['scenes']['left' ], p['content']['top'   ]), (p['scenes' ]['left' ], p['content']['bottom']))
#    page.draw_line((p['scenes']['right'], p['content']['top'   ]), (p['scenes' ]['right'], p['content']['bottom']))






def draw_heading(page, p, data, act):
    act_start = act['start']['location']['target']
    act_end   = act['end'  ]['location']['target']

    height = p['scenes']['bottom'] - p['scenes']['top' ]

    css = f'''
    * {{
        width:          100%;
        text-align:     center;
    }}
    .id {{
        height:         {height * 1/3}px;
        line-height:    {height * 1/3}px;
        vertical-align: middle;

        font-family:    sans-serif;
        font-size:      12px;
        font-weight:    bold;
    }}
    .name {{
        font-family:    serif;
        font-size:      9px;
        font-weight:    normal;
    }}
    '''



    '''
    Scenes
    '''
    for scene in data['scenes']:
        scene_start = scene['start']['location']['target']
        scene_end   = scene['end'  ]['location']['target']

        start   = (scene_start - act_start) / (act_end - act_start)
        end     = (scene_end   - act_start) / (act_end - act_start)

        start_x = start * (p['scenes']['right'] - p['scenes']['left']) + p['scenes']['left']
        end_x   = end   * (p['scenes']['right'] - p['scenes']['left']) + p['scenes']['left']

        if start_x < p['scenes']['left'] or end_x > p['scenes']['right']: continue

        text = {
            'id':   f'''<div class='id'>{scene['id']}</div>''',
            'name': f'''<div class='name'>{scene['name']}</div>''',
        }

        page.draw_line((start_x, p['scenes']['top']), (start_x, p['content']['bottom']), width=0.25)
        page.draw_line((end_x,   p['scenes']['top']), (end_x,   p['content']['bottom']), width=0.25)

        page.draw_rect     ((start_x, p['scenes']['top'] + height * 0/3, end_x, p['scenes']['top'] + height * 1/3), fill=(0.9, 1.0, 0.9), width=0.5)
        page.insert_htmlbox((start_x, p['scenes']['top'] + height * 0/3, end_x, p['scenes']['top'] + height * 1/3), text['id'], css=css)

        page.draw_rect     ((start_x, p['scenes']['top'] + height * 1/3, end_x, p['scenes']['top'] + height * 3/3), fill=(0.9, 1.0, 0.9), width=0.5)
        page.insert_htmlbox((start_x, p['scenes']['top'] + height * 1/3, end_x, p['scenes']['top'] + height * 3/3), text['name'], css=css)



    '''
    Music
    '''
    for music in data['music']:
        music_start = music['start']['location']['target']
        music_end   = music['end'  ]['location']['target']

        start   = (music_start - act_start) / (act_end - act_start)
        end     = (music_end   - act_start) / (act_end - act_start)

        start_x = start * (p['music']['right'] - p['music']['left']) + p['music']['left']
        end_x   = end   * (p['music']['right'] - p['music']['left']) + p['music']['left']

        if start_x < p['music']['left'] or end_x > p['music']['right']: continue

        text = {
            'id':   f'''<div class='id'>{music['id']}</div>''',
            'name': f'''<div class='name'>{music['name']}</div>''',
        }

        page.draw_line((start_x, p['music']['top']), (start_x, p['content']['bottom']), color=(0.8, 0.8, 1.0), width=0.25)
        page.draw_line((end_x,   p['music']['top']), (end_x,   p['content']['bottom']), color=(0.8, 0.8, 1.0), width=0.25)

        page.draw_rect     ((start_x, p['music']['top'] + height * 0/3, end_x, p['music']['top'] + height * 1/3), fill=(0.9, 0.9, 1.0), width=0.5)
        page.insert_htmlbox((start_x, p['music']['top'] + height * 0/3, end_x, p['music']['top'] + height * 1/3), text['id'], css=css)

        page.draw_rect     ((start_x, p['music']['top'] + height * 1/3, end_x, p['music']['top'] + height * 3/3), fill=(0.9, 0.9, 1.0), width=0.5)
        page.insert_htmlbox((start_x, p['music']['top'] + height * 1/3, end_x, p['music']['top'] + height * 3/3), text['name'], css=css)








def draw_miclist(page, p, data, act):
    act_start = act['start']['location']['target']
    act_end   = act['end'  ]['location']['target']

    height = (p['content']['bottom'] - p['content']['top']) / len(data)
    offset = 0

    css = f'''
    * {{
        height:         {height}px;
        line-height:    {height}px;
        vertical-align: middle;

        font-family:    sans-serif;
        font-size:      12px;
        font-weight:    bold;
    }}
    .secundo {{
        font-family:    serif;
        font-size:      10px;
        font-weight:    normal;
    }}
    '''

    for row in data:
        text = f'''<div class='leader'>{row}</div>'''
        page.insert_htmlbox((p['leader']['left'], p['leader']['top'] + offset, p['leader']['right'], p['leader']['top'] + offset + height), text, css=css)
        page.draw_line((p['leader']['left' ], p['leader']['top'] + offset), (p['content']['right'], p['content']['top'] + offset), width=0.25)


        for section in data[row]:
            leader  = row
            primo   = section['primo'  ]
            secundo = section['secundo']

            section_start = section['start']['location']['target']
            section_end   = section['end'  ]['location']['target']

            start   = (section_start - act_start) / (act_end - act_start)
            end     = (section_end   - act_start) / (act_end - act_start)

            start_x = start * (p['content']['right'] - p['content']['left']) + p['content']['left']
            end_x   = end   * (p['content']['right'] - p['content']['left']) + p['content']['left']

            if start_x < p['content']['left'] or end_x > p['content']['right']: continue

            try:
                if   int(section['mic']) <  5: color = (0.73, 0.94, 0.71)
                elif int(section['mic']) < 13: color = (0.71, 0.81, 0.94)
                else:                          color = (0.94, 0.90, 0.71)
            except ValueError:
                color = (0.9, 0.8, 1.0)

            text = f'''<span class='primo'>{primo}</span> / <span class='secundo'>{secundo}</span>'''
            page.draw_rect     ((start_x, p['leader']['top'] + offset, end_x, p['leader']['top'] + offset + height), fill=color, width=0.5)
            page.insert_htmlbox((start_x + 1/mm, p['leader']['top'] + offset, end_x + 50/mm, p['leader']['top'] + offset + height), text, css=css)


        offset += height






def create_pdf(data, type):
    doc = pymupdf.open()

    w, h = pymupdf.paper_size('A3-l')
    p = setup(w, h)

    micdata = {}

    if type == 'mic:role/actor':
        for mic in data['miclist']:
            micdata[mic] = []

        for role in data['rolemic']:
            for section in data['rolemic'][role]:
                micdata[section['mic']].append({
                    'mic':     section['mic'],
                    'primo':   role,
                    'secundo': section['actor'],
                    'start':   section['start'],
                    'end':     section['end'],
                })


    elif type == 'mic:actor/role':
        for mic in data['miclist']:
            micdata[mic] = []

        for role in data['rolemic']:
            for section in data['rolemic'][role]:
                micdata[section['mic']].append({
                    'mic':     section['mic'],
                    'primo':   section['actor'],
                    'secundo': role,
                    'start':   section['start'],
                    'end':     section['end'],
                })


    elif type == 'role:mic/actor':
        for role in data['rolemic']:
            if role == 'Backstage-kor': continue
            micdata[role] = []

            for section in data['rolemic'][role]:

                micdata[role].append({
                    'mic':     section['mic'],
                    'primo':   section['mic'],
                    'secundo': section['actor'],
                    'start':   section['start'],
                    'end':     section['end'],
                })


    elif type == 'actor:mic/role':
        actors = set()

        for role in data['rolemic']:
            if role == 'Backstage-kor': continue
            for section in data['rolemic'][role]:
                actors.add(section['actor'])

        for actor in sorted(list(actors)):
            micdata[actor] = []

        for role in data['rolemic']:
            if role == 'Backstage-kor': continue
            for section in data['rolemic'][role]:
                micdata[section['actor']].append({
                    'mic':     section['mic'],
                    'primo':   section['mic'],
                    'secundo': role,
                    'start':   section['start'],
                    'end':     section['end'],
                })






    for act in data['acts']:
        page = doc.new_page(width = w, height = h)
#        mockup(page, p)

        draw_heading(page, p, data, act)
        draw_miclist(page, p, micdata, act)
        draw_static (page, p, data, act)

    return doc






if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("show")
    parser.add_argument("list")

    args = parser.parse_args()
    show = args.show

    shows = load_data('data/sources/shows.json')
    if not show in shows: print('ERROR! No show', show); exit()

    data = load_data(f'data/compiled/showdata/{show}/showdata.json')


    if args.list == 'mic:role/actor':
        pdf = create_pdf(data, 'mic:role/actor')
        save_pdf(f'data/compiled/showdata/{show}/', 'mic-role-actor.pdf', pdf)


    if args.list == 'mic:actor/role':
        pdf = create_pdf(data, 'mic:actor/role')
        save_pdf(f'data/compiled/showdata/{show}/', 'mic-actor-role.pdf', pdf)


    if args.list == 'role:mic/actor':
        pdf = create_pdf(data, 'role:mic/actor')
        save_pdf(f'data/compiled/showdata/{show}/', 'role-mic-actor.pdf', pdf)


    if args.list == 'actor:mic/role':
        pdf = create_pdf(data, 'actor:mic/role')
        save_pdf(f'data/compiled/showdata/{show}/', 'actor-mic-role.pdf', pdf)
