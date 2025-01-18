'''
FIX: Add pages is in conflict with remove pages
Bytt "show" med action: empty, music, mics...

Take in showdata
Create pdfs for show:
manus-empty.pdf
manus-music.pdf
manus-mics.pdf
'''


import argparse
import json
import pymupdf
import pathlib

from pprint import pprint






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






def print_mic(pdfpage, x, y, type, text):
    if type == 'role':     color = (0,    0,    0   ); fill = (0.7, 1.0, 0.7)
    if type == 'ensemble': color = (0,    0,    0   ); fill = (1.0, 1.0, 0.5)
    if type == 'off':      color = (0.70, 0.70, 0.70); fill = (1.0, 1.0, 1.0)

    page_width, page_height = pdfpage.rect.width, pdfpage.rect.height

    shape = pdfpage.new_shape()
    shape.draw_circle((x, y), 9)
    shape.finish(color=color, fill=fill)
    shape.commit()

    pdfpage.insert_textbox((x-14.9, y-8.5, x+15, y+25), text, fontsize=12, align=1, color=(0, 0, 0), fontname="Helvetica-Bold")






def annotate_roles(doc, page, y, mics):
    pdfpage = doc[page - 1]
    page_width, page_height = pdfpage.rect.width, pdfpage.rect.height

    x1, x2 = 0.010, 0.111
    fill = (0.8, 1, 0.8)

    offset_x = 0
    offset_y = 0

    for mic in mics:
        print_mic(pdfpage, x1 * page_width + offset_x + 5, y * page_height + offset_y + 4, 'role', str(mic))

        offset_x += 20
        if (x1 * page_width + offset_x + 20) > x2 * page_width:
           offset_x = 0
           offset_y += 20






def annotate_ensembles(doc, page, y, mics):
    pdfpage = doc[page - 1]
    page_width, page_height = pdfpage.rect.width, pdfpage.rect.height

    x1, x2 = 0.450, 1.006
    color = (0.70, 0.70, 0.70)
    fill  = (1.00, 1.00, 1.00)

    offset_x = 0
    offset_y = 0

    pdfpage.draw_rect((x1 * page_width + offset_x - 6, y * page_height + offset_y - 7, x2 * page_width + offset_x - 5, y * page_height + offset_y + 35), fill=(1, 1, 1), fill_opacity=0.75, width=0)

    for mic in mics:
        print_mic(pdfpage, x1 * page_width + offset_x + 5, y * page_height + offset_y + 4, mics[mic], str(mic))

        offset_x += 20
        if (offset_x == 8 * 20): offset_x += 10

        if (x1 * page_width + offset_x + 20) > x2 * page_width:
           offset_x = 0
           offset_y += 20






def create_empty(base, data):
    doc = pymupdf.open(base)

    # Remove pages
    for page in data.get('remove_pages', []):
        doc.delete_page(page - 1)


    # Add extra pages and add page numbers
    offset = 0
    for page in data.get('extra_pages', []):
        pdfpage = doc[page['after'] + offset]
        page_width, page_height = pdfpage.rect.width, pdfpage.rect.height
        pdfpage = doc.new_page(pno = page['after'] + offset, width=page_width, height=page_height)

        pdfpage.insert_textbox((pdfpage.rect.width / 2, 779, pdfpage.rect.width / 2 + 218, 810), 'Side ' + page['name'], fontsize=12, align=2, color=(0, 0, 0), fontname="Times-Bold")
        offset += 1


    # Add extra page text
    for text in data.get('pagetext'):
        pdfpage = doc[text['page']['target'] - 1]

        x1, x2 = 0, pdfpage.rect.width
        y = text['y'] * page_height

        pdfpage.insert_textbox((x1, y, x2, y + 28), text['heading'], fontsize=16, align=1, color=(0, 0, 0), fontname='Times-Bold' )

        y += 40
        for line in text['lines']:
            pdfpage.insert_textbox((x1, y, x2, y + 28), line, fontsize=12, align=1, color=(0, 0, 0), fontname='Times-Roman' )
            y += 20


    # Remove parts
    for part in data.get('remove_parts'):
        pdfpage = doc[part['start']['page']['target'] - 1]

        x1, x2 = -1, pdfpage.rect.width + 1
        y1, y2 = part['start']['y'] * page_height, part['end']['y'] * page_height

        pdfpage.draw_rect((x1, y1, x2, y2), fill=(1, 1, 1), fill_opacity=0.9)


    # Add extra lines
    for text in data.get('extra_lines'):
        roles = ', '.join(text['roles'])
        pdfpage = doc[text['page']['target'] - 1]

        x1, x2 = 0.109 * pdfpage.rect.width, pdfpage.rect.width
        y = text['y'] * page_height - 3

        pdfpage.insert_textbox((x1, y, x2, y + 28), roles, fontsize=11, align=0, color=(0, 0, 0), fontname='Times-Bold' )

        y += 14.3
        for line in text['lines']:
            pdfpage.insert_textbox((x1, y, x2, y + 28), line, fontsize=11, align=0, color=(0, 0, 0), fontname='Times-Roman' )
            y += 14


    return doc






def create_music(base, data):
    doc = pymupdf.open(base)

    for music in data.get('music'):
        pdfpage = doc[music['start']['page']['target'] - 1]
        page_width, page_height = pdfpage.rect.width, pdfpage.rect.height

        text = ''
        if music['type'] == 'song':         text += 'Sang: '
        if music['type'] == 'instrumental': text += 'Instrumental: '

        text += music['id'] + ' - ' + music['name']

        x1, x2 = 0, pdfpage.rect.width
        y = music['start']['y'] * page_height

        pdfpage.draw_line((x1, y), (x2, y), color=(0, 0, .5))
        pdfpage.insert_textbox((x1, y - 15, x2, y + 10), text, fontsize=12, align=1, color=(0, 0, .5), fontname='Helvetica-Bold')

        pdfpage = doc[music['end']['page']['target'] - 1]
        page_width, page_height = pdfpage.rect.width, pdfpage.rect.height

        x1, x2 = 0, pdfpage.rect.width
        y = music['end']['y'] * page_height

        pdfpage.draw_line((x1, y), (x2, y), color=(0, 0, .5))


    return doc






def create_mics(base, data):
    doc = pymupdf.open(base)

    micmap = data.get('micmap', [])

    for line in data.get('lines', []):
        current_micmap = list(filter(lambda x: x['location']['target'] <= line['location']['target'], micmap))[-1]['mics']

        miclist = { mic: 'off' for mic in data.get('miclist', []) }
        role_mics = []


        # Test roles
        for role in line['roles']:
            for mic in current_micmap:
                if current_micmap[mic]['role'] == role:
                    miclist[mic] = 'role'


        # Test ensemble
        for role in line['ensemble']:
            for mic in current_micmap:
                if current_micmap[mic]['role'] == role:
                    miclist[mic] = 'ensemble'


        for mic in miclist:
            if miclist[mic] == 'role':
                role_mics.append(mic)


        if len(line['roles'   ]) > 0: annotate_roles    (doc, line['page']['target'], line['y'], role_mics)
        if len(line['ensemble']) > 0: annotate_ensembles(doc, line['page']['target'], line['y'], miclist)


    return doc






if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("show")
    args = parser.parse_args()

    show = args.show

    shows = load_data('data/sources/shows.json')
    if not show in shows: print('ERROR! No show', show); exit()

    data  = load_data(f'data/compiled/showdata/{show}/showdata.json')

    manusfile = 'data/originals/manus.pdf'
    emptyfile = 'data/compiled/pdf/manus-empty.pdf'
    musicfile = 'data/compiled/pdf/manus-music.pdf'
    micsfile  = 'data/compiled/pdf/manus-mics.pdf'


    # create empty pdf with removed pages and extra pages
    empty_pdf = create_empty(manusfile, data)
    save_pdf(f'data/compiled/pdf/', 'manus-empty.pdf', empty_pdf)


    # create music based on empty
    music_pdf = create_music(emptyfile, data)
    save_pdf(f'data/compiled/pdf/', 'manus-music.pdf', music_pdf)


    # create mics based on music
    mics_pdf = create_mics(musicfile, data)
    save_pdf(f'data/compiled/pdf/', 'manus-mics.pdf', mics_pdf)
