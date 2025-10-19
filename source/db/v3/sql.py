import mysql.connector
import json


class DB:
    def __init__(self):
        self.db = None
        self.version = { 'current': None, 'previous': None }

        self.data = {
            'host':      'localhost',
            'port':      '8889',
            'user':      'showmaster',
            'password':  'showmaster',
            'database':  'Maridalsspillet_2025',

            'person_id': '1',
        }



    def __del__(self):
        self.db.close()



    def connect(self):
        try:
            self.db = mysql.connector.connect(
                host     = self.data['host'],
                port     = self.data['port'],
                user     = self.data['user'],
                password = self.data['password'],
                database = self.data['database'],
            )

            self.getversion()


        except mysql.connector.Error as err:
            print(f'Error: {err}')



    def getversion(self):
        cursor = self.db.cursor(dictionary = True)

        query_select = f"""
            SELECT
                MAX(`version_id`) AS `version`
            FROM
                `versions`
            ;
        """

        query_insert = """
            INSERT INTO `versions`
                (`comment`)
            VALUES
                (%s)
            ;
        """
        values = ('Created by Fade In Importer',)

        try:
            cursor.execute(query_select)

            result = cursor.fetchone()
            self.version['previous'] = result['version']

            cursor.execute(query_insert, values)
            self.version['current'] = cursor.lastrowid

            self.db.commit()

        except Exception as error:
            print(f'Error: {error}')

        finally:
            cursor.close()



    def get_characters(self):
        cursor = self.db.cursor(dictionary = True)

        characters = {}

        query_select = """
            SELECT
                `character_alias_name`,
                `character_id`,
                `character_name`
            FROM
                `view_character_aliases`
            WHERE `version_end` IS NULL
            ;
        """

        try:
            cursor.execute(query_select)

            for row in cursor.fetchall():
                alias = row['character_alias_name']
                if not alias in characters:
                    characters[alias] = []

                characters[alias].append({
                    'id': row['character_id'],
                    'name': row['character_name']
                })

            return characters

        except Exception as error:
            print(f'Error: {error}')

        finally:
            cursor.close()



    def get_text_id_or_insert(self, text_type, text):
        cursor = self.db.cursor(dictionary = True)

        query_insert = f"""
            INSERT INTO `texts`
                (`text_type`, `text`)
            VALUES
                (%s, %s)
            ON DUPLICATE KEY UPDATE `text_id` = LAST_INSERT_ID(`text_id`)
            ;
        """
        values = (text_type, text)


        try:
            cursor.execute(query_insert, values)
            self.db.commit()
            return cursor.lastrowid

        except Exception as error:
            print(f'Error: {error}')

        finally:
            cursor.close()



#    def get_content_id_or_insert(self, type, scene_id, content_order, character_alias_id, text_id):
#            cursor = self.db.cursor(dictionary = True)
#
#            query_insert = f"""
#                INSERT INTO `content`
#                    (`version_start`, `type`, `scene_id`, `content_order`, `character_alias_id`, `text_id`)
#                VALUES
#                    (%s, %s, %s, %s, %s, %s)
#                ON DUPLICATE KEY UPDATE `content_id` = LAST_INSERT_ID(`content_id`)
#                ;
#            """
#            values = (self.version['current'], type, scene_id, content_order, character_alias_id, text_id)
#
#
#            try:
#                cursor.execute(query_insert, values)
#                self.db.commit()
#                return cursor.lastrowid
#
#            except Exception as error:
#                print(f'Error: {error}')



    def create_and_expire_scenes(self, current_scenes):
        scenes_json = json.dumps(current_scenes)

        try:
            cursor = self.db.cursor()
            cursor.callproc('create_and_expire_scenes', (scenes_json, self.version['current'], self.version['previous']))
            self.db.commit()

        except Exception as error:
            print(f"Error: {error}")

        finally:
            cursor.close()



#    def create_and_expire_scenes(self, current_scenes):
#        cursor = self.db.cursor(dictionary = True)
#
#        subquery_update_fragments = []
#        for scene in current_scenes:
#            subquery_update_fragments.append(f"""
#                SELECT
#                    '{scene['id']}'          AS id,
#                    '{scene['name']}'        AS scene_name,
#                    '{scene['scene_order']}' AS scene_order
#            """)
#
#        subquery_update = ' UNION ALL '.join(subquery_update_fragments)
#
#        subquery_insert_fragments = []
#        for scene in current_scenes:
#            subquery_insert_fragments.append(f"""
#                (
#                    '{self.version['current']}',
#                    '{scene['scene_order']}',
#                    '{scene['id']}',
#                    '{scene['name']}'
#                )
#            """)
#
#        subquery_insert = ', '.join(subquery_insert_fragments)
#
#        query_update = f"""
#            UPDATE
#                `scenes`
#            SET
#                version_end = '%s'
#            WHERE
#                `version_end` IS NULL
#                AND NOT EXISTS (
#                    SELECT 1 FROM
#                        ({subquery_update}) AS input_list
#                    WHERE
#                            scenes.id          = input_list.id
#                        AND scenes.name        = input_list.scene_name
#                        AND scenes.scene_order = input_list.scene_order
#                )
#            ;
#        """
#        values = (self.version['previous'],)
#
#        query_insert = f"""
#            INSERT INTO `scenes`
#                (`version_start`, `scene_order`, `id`, `name`)
#            VALUES
#                {subquery_insert}
#            ON DUPLICATE KEY UPDATE `scene_id` = LAST_INSERT_ID(`scene_id`)
#            ;
#        """
#
#        try:
#            self.cursor.execute(query_update, values)
#            self.db.commit()
#
#            self.cursor.execute(query_insert)
#            self.db.commit()
#
#        except Exception as error:
#            print(f'Error: {error}')



    def create_content(self, content):
        try:
            cursor = self.db.cursor(dictionary = True)

            cursor.callproc('insert_content', (
                self.version['current'],
                content['scene_id'          ],
                content['block_order'       ],
                content['division_order'    ],
                content['paragraph_order'   ],
                content['content_order'     ],
                content['character_alias_id'],
                content['text_type'         ],
                content['text'              ],
            ))

            self.db.commit()

        except Exception as error:
            print(f"Error: {error}")

        finally:
            cursor.close()



#    def create_and_expire_content(self, current_content):
#        cursor = self.db.cursor(dictionary = True)
#
#        subquery_update_fragments = []
#        subquery_insert_fragments = []
#
#        for content in current_content:
#            type, scene_id, content_order, character_alias_id, text_id = content
#            character_alias_id_sql = 'NULL' if character_alias_id is None else f"'{character_alias_id}'"
#            subquery_update_fragments.append(f"""
#                SELECT
#                    '{type}'                 AS type,
#                    '{scene_id}'             AS scene_id,
#                    '{content_order}'        AS content_order,
#                    {character_alias_id_sql} AS character_alias_id,
#                    '{text_id}'              AS text_id
#                """)
#
#            subquery_insert_fragments.append(f"""
#                ('{self.version['current']}', '{type}', '{scene_id}', '{content_order}', {character_alias_id_sql}, '{text_id}')
#            """)
#
#        subquery_update = ' UNION ALL '.join(subquery_update_fragments)
#        subquery_insert = ', '.join(subquery_insert_fragments)
#
#        query_update = f"""
#            UPDATE
#                `content`
#            SET
#                version_end = '%s'
#            WHERE
#                `version_end` IS NULL
#                AND NOT EXISTS (
#                    SELECT 1 FROM
#                        ({subquery_update}) AS input_list
#                    WHERE
#                            content.type               = input_list.type
#                        AND content.scene_id           = input_list.scene_id
#                        AND content.content_order      = input_list.content_order
#                        AND (
#                            (content.character_alias_id IS NULL AND input_list.character_alias_id IS NULL)
#                            OR (content.character_alias_id = input_list.character_alias_id)
#                        )
#                        AND content.text_id            = input_list.text_id
#                )
#            ;
#        """
#        values = (self.version['previous'],)
#
#        query_insert = f"""
#            INSERT INTO `content`
#                (`version_start`, `type`, `scene_id`, `content_order`, `character_alias_id`, `text_id`)
#            VALUES
#                {subquery_insert}
#            ON DUPLICATE KEY UPDATE `content_id` = LAST_INSERT_ID(`content_id`)
#            ;
#        """
#
#        try:
#            cursor.execute(query_update, values)
#            self.db.commit()
#
#            cursor.execute(query_insert)
#            self.db.commit()
#
#        except Exception as error:
#            print(f'Error: {error}')
#
#        finally:
#            cursor.close()



    def get_scene_id(self, id):
        cursor = self.db.cursor(dictionary = True)

        query_select = f"""
            SELECT
                `scene_id`
            FROM
                `scenes`
            WHERE
                    `version_end` IS NULL
                AND `id` = %s
            ;
        """
        values = (id,)

        try:
            cursor.execute(query_select, values)
            result = cursor.fetchone()
            cursor.close()
            return result['scene_id']

        except Exception as error:
            print(f'Error: {error}')

        finally:
            cursor.close()



    def get_character_alias_id(self, name):
        cursor = self.db.cursor(dictionary = True)

        query_select = f"""
            SELECT
                `character_alias_id`
            FROM
                `character_aliases`
            WHERE
                    `version_end` IS NULL
                AND `name` = %s
            ;
        """
        values = (name,)

        try:
            cursor.execute(query_select, values)
            result = cursor.fetchone()
            cursor.close()
            return result

        except Exception as error:
            print(f'Error: {error}')
