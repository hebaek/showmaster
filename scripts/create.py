import argparse
import json
import pymupdf
import pathlib

from pprint import pprint




w, h = 0, 0
mm = 0






def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)



def save_pdf(path, filename, doc):
    fullpath = pathlib.Path(path)
    fullname = fullpath / filename

    fullpath.mkdir(parents=True, exist_ok=True)

    doc.save(fullname)
    doc.close()

    print(f'PDF saved to: {fullname}')



def get_x(start_y, end_y, y):
    min_y, max_y = start_y, end_y
    min_x, max_x = 35/mm, 410/mm

    return min_x + (y - min_y) * (max_x - min_x) / (max_y - min_y)






def create_headers(page, data, act):
    show_name = data['showinfo']['name']
    show_date = data['showinfo']['date']
    show_time = data['showinfo']['time']
    act_name  = data['acts'][act]['name']

    page.insert_textbox(( 10/mm, 10/mm,  60/mm, 18/mm), 'Heksene fra Eastwick', fontsize=12, align=0, color=(0, 0, 0), fontname='Times-Bold' )
    page.insert_textbox(( 70/mm, 10/mm, 120/mm, 18/mm), show_name,              fontsize=12, align=0, color=(0, 0, 0), fontname='Times-Bold' )
    page.insert_textbox((130/mm, 10/mm, 180/mm, 18/mm), act_name,               fontsize=12, align=0, color=(0, 0, 0), fontname='Times-Bold' )

    page.draw_line((10/mm, 16/mm), (410/mm, 16/mm), color=(0, 0, 0))






def create_scene(page, start_y, end_y, data, scene):
    id, name = scene['id'], scene['name']
    start, end = scene['start']['location']['target'], scene['end']['location']['target']
    start_x, end_x = get_x(start_y, end_y, start), get_x(start_y, end_y, end)


    page.insert_htmlbox((start_x, 20/mm, end_x, 28/mm), id, css='* {text-align:center;font-family:serif;font-size:12px;font-weight:bold;}' )
    page.insert_htmlbox((start_x, 25/mm, end_x, 33/mm), name, css='* {text-align:center;font-family:serif;font-size:10px;}' )

    page.draw_line((10/mm, 33/mm), (410/mm, 33/mm), color=(0, 0, 0))

    page.draw_line((start_x, 20/mm), (start_x, 287/mm), color=(0.0, 0.0, 0.0), width=0.50)
    page.draw_line((end_x,   20/mm), (end_x,   287/mm), color=(0.0, 0.0, 0.0), width=0.25)






def create_rolemap(page, start_y, end_y, rolemic):
    current = {}
    y = 23/mm + 4
    for role in rolemic:
        y += 9/mm
        page.insert_htmlbox((10/mm, y, 35/mm, y + 10/mm), role, css='* {text-align:left;vertical-align:middle;font-family:sans-serif;font-size:10px;}' )

        for section in rolemic[role]:
            start = section['start']['location']['target']
            end   = section['end'  ]['location']['target']

            start, end = get_x(start_y, end_y, start), get_x(start_y, end_y, end)

            actor = section['actor']
            mic   = section['mic']

            page.draw_rect((start, y + 1/mm, end, y + 7.2/mm), color=(0, 0, 0), fill=(1, 1, 1), fill_opacity=0.75)

            text = f'{mic} / {actor}'

            if mic:
                page.insert_htmlbox((start, y + 1/mm, end, y + 8/mm), text, css='* {text-align:left;font-family:serif;font-size:10px;}' )


#        if map['location']['target'] < start_y or map['location']['target'] > end_y: return

#        x = get_x(start_y, end_y, map['location']['target'])

#        for (index, mic) in enumerate(map['mics']):
#            print(map['mics'][mic])
#            actor = map['mics'][mic]['actor']
#            if current[mic] != actor:
#               current[mic] = actor

#               if actor is None: actor = '*'







def create_page(doc, data, act):
    w, h = pymupdf.paper_size('A3-l')
    page = doc.new_page(width = w, height = h)
    create_headers(page, data, act)

    for (index, mic) in enumerate(data['miclist']):
#        page.insert_htmlbox((10/mm, 33/mm + index * 9/mm + 4, 20/mm, 42/mm + index * 9/mm), mic, css='* {text-align:left;vertical-align:middle;font-family:sans-serif;font-size:14px;font-weight:bold;}' )
        page.draw_line((10/mm, 42/mm + index * 9/mm), (410/mm, 42/mm + index * 9/mm), color=(0.0, 0.0, 0.0), width=0.25)


    return page






def create_pdf(data):
    doc = pymupdf.open()

    global w, h, mm
    w, h = pymupdf.paper_size('A3-l')
    mm = 420 / w

    for act in range(0, len(data['acts'])):
        page = create_page(doc, data, act)

        start_y = data['acts'][act]['start']['location']['target']
        end_y   = data['acts'][act]['end'  ]['location']['target']

        for scene in [scene for scene in data['scenes'] if scene['start']['location']['target'] >= start_y and scene['end']['location']['target'] <= end_y]:
            create_scene(page, start_y, end_y, data, scene)

        create_rolemap(page, start_y, end_y, data['rolemic'])

    return doc






if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("show")
    args = parser.parse_args()

    show = args.show

    shows = load_data('data/sources/shows.json')
    if not show in shows: print('ERROR! No show', show); exit()

    data  = load_data(f'data/compiled/showdata/{show}/showdata.json')

    # create mics based on music
    pdf = create_pdf(data)
    save_pdf(f'data/compiled/pdf/', 'list.pdf', pdf)
