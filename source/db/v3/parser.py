import xml.etree.ElementTree as ET
import text_functions
import re

from copy   import deepcopy


class Parser:
    def __init__(self, input):
        self.tree = ET.parse(input)
        self.root = self.tree.getroot()

        self.paragraphs = self.root.findall('.//paragraphs/para')



    def add_db_data(self, data):
        self.data = data



    def parse(self):
        content = self.parse_step_1()
        content = self.parse_step_2(content)

        return content



    def parse_step_1(self):
        content, lines = [], []
        style, previous_style = None, None

        for element in self.paragraphs:
            style = element.find('.//style').get('basestyle', None)
            text  = element.find('.//text').text or None

            text = text_functions.hack_text_pre(text)

            if not style: continue

            if style != previous_style:
                content.append((previous_style, deepcopy(lines)))
                lines.clear()

            if text: lines.extend(text.splitlines())
            else:    lines.append('')

            previous_style = style

        content.append((previous_style, lines))
        return content



    def parse_step_2(self, content):
        result = []

        for content_type, element in content:
            if content_type == 'Scene Heading':
                text = ''.join(element)
                if not re.search('^SCENE ', text): continue

                id, text = text.split(' - ')
                id = id.removeprefix('SCENE ')

                text_type = text_functions.get_text_type(text, content_type)
                text = text_functions.fix_text_case(text, text_type, self.data['characters'])

                result.append({ 'content_type': 'scene', 'id': id, 'name': text })

            elif content_type == 'Character':
                text = ''.join(element)
                text = text_functions.hack_text_pre(text)
                text_type = text_functions.get_text_type(text, content_type)
                text = text_functions.fix_text_case(text, text_type, self.data['characters'])

                result.append({ 'content_type': 'character', 'name': text })

            elif content_type == 'Dialogue':
                paragraphs = self.parse_text(content_type, element)
                if len(paragraphs) == 0: continue

                result.append({ 'content_type': 'dialogue', 'lines': [{ 'text_type': text_type, 'line': line } for (text_type, line) in paragraphs] })

            elif content_type == 'Action':
                paragraphs = self.parse_text(content_type, element)
                if len(paragraphs) == 0: continue

                result.append({ 'content_type': 'action', 'lines': [{ 'text_type': text_type, 'line': line } for (text_type, line) in paragraphs] })

            elif content_type == 'Parenthetical':
                text = ''.join(element)
                text = text_functions.hack_text_pre(text)
                text_type = text_functions.get_text_type(text, content_type)
                text = text_functions.fix_text_case(text, text_type, self.data['characters'])

                result.append({ 'content_type': 'parenthetical', 'name': text })

            else:
                continue


        return result



    def parse_text(self, content_type, element):
        result_joined = []
        result_final  = []

        paragraphs    = []
        lines         = []

        previous_type = None



        for text in element:
            text_type = text_functions.get_text_type(text, content_type)

            if text_type is None:
                if previous_type:
                    paragraphs.append((previous_type, deepcopy(lines)))
                    lines.clear()
            elif text_type != previous_type:
                if previous_type:
                    paragraphs.append((previous_type, deepcopy(lines)))
                    lines.clear()
                lines.append(text)
            else:
                lines.append(text)

            previous_type = text_type

        if previous_type:
            paragraphs.append((previous_type, lines))



        for (text_type, lines) in paragraphs:
            if text_type == 'dialogue': lines = [' '.join(lines)]
            result_joined.append((text_type, lines))



        for (text_type, lines) in result_joined:
            new_lines = []
            for text in lines:
                text = text_functions.fix_text_case(text, text_type, self.data['characters'])
                text = text_functions.hack_text_post(text, text_type)
                new_lines.append(text)

            result_final.append((text_type, new_lines))



        return result_final
