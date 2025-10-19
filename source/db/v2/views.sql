CREATE OR REPLACE VIEW `view_character_aliases` AS
SELECT
    `character_aliases`.`version_start`,
    `character_aliases`.`version_end`,
    `versions`.`name`                       AS 'version_name',
    `character_aliases`.`part_start`,
    `character_aliases`.`part_end`,
    `parts`.`order`                         AS 'part_order',
    `character_aliases`.`name`              AS 'alias',
    `characters`.`name`                     AS 'character',
    `characters`.`character_id`             AS 'character_id'
FROM
              `character_aliases`
    LEFT JOIN `characters`     USING (`character_id`)
    LEFT JOIN `versions`       ON (`character_aliases`.`version_start` = `versions`.`version_id`)
    LEFT JOIN `parts`          ON (`character_aliases`.`part_start`    = `parts`.`part_id`)
;
