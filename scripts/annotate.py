import fitz  # PyMuPDF
import json



def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)



def annotate_pdf(pdf_original, pdf_output, data_compiled):
    doc = fitz.open(pdf_original)

    lastpage    = data_compiled.get('pagemap')[-1]['source']
    acts        = data_compiled.get('acts')
    scenes      = data_compiled.get('scenes')
    lines       = data_compiled.get('lines')
    music       = data_compiled.get('music')

    pagemap     = data_compiled.get('pagemap')
    ensemblemap = data_compiled.get('ensemblemap')
    micmap      = data_compiled.get('micmap')

    mics        = list(micmap[0]['mics'].keys())



    def mark_mic(pdfpage, x, y, type, text):
        if type == 'role':     color = (0,    0,    0   ); fill = (0.8, 1.0, 0.8)
        if type == 'ensemble': color = (0,    0,    0   ); fill = (0.8, 0.8, 1.0)
        if type == 'off':      color = (0.70, 0.70, 0.70); fill = (1.0, 1.0, 1.0)

        page_width, page_height = pdfpage.rect.width, pdfpage.rect.height

        shape = pdfpage.new_shape()
        shape.draw_circle((x, y), 9)
        shape.finish(color=color, fill=fill)
        shape.commit()

        pdfpage.insert_textbox((x-14.9, y-8.5, x+15, y+25), text, fontsize=12, align=1, color=(0, 0, 0), fontname="Helvetica-Bold")



    def annotate_music(doc):
        for song in music:
            page  = song['start']['page']
            y     = song['start']['y']

            pdfpage = doc[page - 1]
            page_width, page_height = pdfpage.rect.width, pdfpage.rect.height

            text = ''
            if song['type'] == 'song':         text += 'Sang: '
            if song['type'] == 'instrumental': text += 'Instrumental: '

            text += song['id'] + ' - ' + song['name']

            pdfpage.draw_line((0, y * page_height), (page_width, y * page_height), color=(0, 0, .5))
            pdfpage.insert_textbox((page_width / 2 - 200, y * page_height - 15, page_width / 2 + 200, y * page_height + 10), text, fontsize=12, align=1, color=(0, 0, .5), fontname="Helvetica-Bold")



    def annotate_roles(doc, page, y, mics):
        pdfpage = doc[page - 1]
        page_width, page_height = pdfpage.rect.width, pdfpage.rect.height

        x1, x2 = 0.010, 0.111
        fill = (0.8, 1, 0.8)

        offset_x = 0
        offset_y = 0

        for mic in mics:
            mark_mic(pdfpage, x1 * page_width + offset_x + 5, y * page_height + offset_y + 4, 'role', str(mic))

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
            mark_mic(pdfpage, x1 * page_width + offset_x + 5, y * page_height + offset_y + 4, mics[mic], str(mic))

            offset_x += 20
            if (offset_x == 8 * 20): offset_x += 10

            if (x1 * page_width + offset_x + 20) > x2 * page_width:
               offset_x = 0
               offset_y += 20




    def annotate_mics(doc):
        for line in lines:
            page  = line['location']['page']
            y     = line['location']['y']

            miclist = { mic: 'off' for mic in mics }
            current_micmap = list(filter(lambda x: x['location']['page'] <= line['location']['page'] and x['location']['y'] <= line['location']['y'], micmap))[-1]['mics']
            role_mics = []



            if 'ensembles' in line:
                for ensemble in line['ensembles']:
                    current_ensemblemap = list(filter(lambda x: x['location']['page'] <= line['location']['page'] and x['location']['y'] <= line['location']['y'], ensemblemap[ensemble]))[-1]

                    roles  = current_ensemblemap['roles']
                    extras = current_ensemblemap['extras']

                    for role in roles:
                        for mic in current_micmap:
                            if current_micmap[mic]['role'] == role:
                                miclist[mic] = 'ensemble'

                    for actor in extras:
                        for mic in current_micmap:
                            if current_micmap[mic]['actor'] == actor:
                                miclist[mic] = 'ensemble'



            if 'roles' in line:
                for role in line['roles']:
                    for mic in current_micmap:
                        if current_micmap[mic]['role'] == role:
                            miclist[mic] = 'role'

                for m in miclist:
                    if miclist[m] == 'role':
                        role_mics.append(m)



            if len(line['roles']) > 0: annotate_roles(doc, page, y, role_mics)
            if len(line['ensembles']) > 0: annotate_ensembles(doc, page, y, miclist)



    annotate_music(doc)
    annotate_mics(doc)



    doc.save(pdf_output)
    print(f"Annotated PDF saved to: {pdf_output}")



if __name__ == "__main__":
    pdf_original = "data/compiled/manus-expanded.pdf"
    pdf_output   = "data/compiled/manus-mics.pdf"

    data_compiled = load_json('data/compiled/compiled.json')

    annotate_pdf(pdf_original, pdf_output, data_compiled)
