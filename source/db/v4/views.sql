CREATE OR REPLACE VIEW `view_character_aliases` AS
SELECT
    `character_alias_characters`.`version_start`,
    `character_alias_characters`.`version_end`,
    `versions`.`name`                           AS 'version_name',
    `character_alias_characters`.`part_start`,
    `character_alias_characters`.`part_end`,
    `parts`.`part_order`                        AS 'part_order',
    `character_aliases`.`character_alias_id`    AS 'character_alias_id',
    `character_aliases`.`name`                  AS 'character_alias_name',
    `characters`.`character_id`                 AS 'character_id',
    `characters`.`name`                         AS 'character_name'
FROM
              `character_alias_characters`
    LEFT JOIN `character_aliases`   USING (`character_alias_id`)
    LEFT JOIN `characters`          USING (`character_id`)
    LEFT JOIN `versions`            ON (`character_alias_characters`.`version_start` = `versions`.`version_id`)
    LEFT JOIN `parts`               ON (`character_alias_characters`.`part_start`    = `parts`.`part_id`)
;
