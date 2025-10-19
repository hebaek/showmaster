CREATE OR REPLACE VIEW `manus` AS
SELECT
    `versions`.`version_id`  AS `version_id`,
    `scenes`.`id`               AS `scene_id`,
    `blocks`.`block_id`         AS `block_id`,
    `paragraphs`.`paragraph_id` AS `paragraph_id`,
    `texts`.`text_id`           AS `text_id`,
    `scenes`.`name`             AS `scene_name`,
    `blocks`.`order`            AS `block_order`,
    `paragraphs`.`order`        AS `paragraph_order`,
    `paragraph_texts`.`order`   AS `text_order`,
    `block_types`.`name`        AS `block_type`,
    `text_types`.`name`         AS `text_type`,
    `character_groups`.`name`   AS `character_group`,
    `texts`.`text`              AS `text`
FROM `versions`
LEFT JOIN `scenes`           ON (                                                                                                                        `scenes`.`version_start` <= `versions`.`version_id` AND (                    `scenes`.`version_end` IS NULL OR                     `scenes`.`version_end` >= `versions`.`version_id`))
LEFT JOIN `blocks`           ON (                              `blocks`.`scene_id` = `scenes`.`scene_id`                         AND                     `blocks`.`version_start` <= `versions`.`version_id` AND (                    `blocks`.`version_end` IS NULL OR                     `blocks`.`version_end` >= `versions`.`version_id`))
LEFT JOIN `paragraphs`       ON (                          `paragraphs`.`block_id` = `blocks`.`block_id`                         AND                 `paragraphs`.`version_start` <= `versions`.`version_id` AND (                `paragraphs`.`version_end` IS NULL OR                 `paragraphs`.`version_end` >= `versions`.`version_id`))
LEFT JOIN `paragraph_texts`  ON (                 `paragraph_texts`.`paragraph_id` = `paragraphs`.`paragraph_id`                 AND            `paragraph_texts`.`version_start` <= `versions`.`version_id` AND (           `paragraph_texts`.`version_end` IS NULL OR            `paragraph_texts`.`version_end` >= `versions`.`version_id`))
LEFT JOIN `texts`            ON (                                `texts`.`text_id` = `paragraph_texts`.`text_id`                 AND                      `texts`.`version_start` <= `versions`.`version_id` AND (                     `texts`.`version_end` IS NULL OR                      `texts`.`version_end` >= `versions`.`version_id`))
LEFT JOIN `character_groups` ON (          `character_groups`.`character_group_id` = `blocks`.`character_group_id`               AND           `character_groups`.`version_start` <= `versions`.`version_id` AND (          `character_groups`.`version_end` IS NULL OR           `character_groups`.`version_end` >= `versions`.`version_id`))
LEFT JOIN `block_types`      ON (                    `block_types`.`block_type_id` = `blocks`.`block_type_id`)
LEFT JOIN `text_types`       ON (                      `text_types`.`text_type_id` = `texts`.`text_type_id`)
ORDER BY
    `versions`.`version_id`,
    `scenes`.`scene_id`,
    `blocks`.`order`,
    `paragraphs`.`order`,
    `paragraph_texts`.`order`
;


CREATE OR REPLACE VIEW `cues` AS
SELECT
    `versions`.`version_id`  AS `version_id`,
    `scenes`.`id`            AS `scene_id`,
    `scenes`.`name`          AS `scene_name`,
    `blocks`.`order`         AS `block_order`,
    `block_metadata`.`key`   AS `data_key`,
    `block_metadata`.`value` AS `data_value`
FROM `versions`
LEFT JOIN `scenes`         ON (                                                              `scenes`.`version_start` <= `versions`.`version_id` AND (        `scenes`.`version_end` IS NULL OR         `scenes`.`version_end` >= `versions`.`version_id`))
LEFT JOIN `blocks`         ON (        `blocks`.`scene_id` = `scenes`.`scene_id` AND         `blocks`.`version_start` <= `versions`.`version_id` AND (        `blocks`.`version_end` IS NULL OR         `blocks`.`version_end` >= `versions`.`version_id`))
LEFT JOIN `block_metadata` ON (`block_metadata`.`block_id` = `blocks`.`block_id` AND `block_metadata`.`version_start` <= `versions`.`version_id` AND (`block_metadata`.`version_end` IS NULL OR `block_metadata`.`version_end` >= `versions`.`version_id`))
WHERE
    `block_metadata`.`key` IS NOT NULL
ORDER BY
    `versions`.`version_id`,
    `scenes`.`scene_id`,
    `blocks`.`order`
;
