SELECT * FROM `manus`
WHERE `version_id` = (SELECT MAX(`version_id`) FROM `versions`);


SELECT * FROM `cues`
WHERE `version_id` = (SELECT MAX(`version_id`) FROM `versions`);




WITH paragraph_level AS (
    SELECT
        scene_id,
        block_order AS block_id,
        paragraph_order AS paragraph_id,
        JSON_ARRAYAGG(
            JSON_OBJECT(
                'text_id', text_order,
                'type', text_type,
                'character', character_group,
                'content', text
            )
        ) AS paragraph_content
    FROM manus
    WHERE version_id = (SELECT MAX(version_id) FROM versions)
    GROUP BY scene_id, block_order, paragraph_order
),
block_level AS (
    SELECT
        scene_id,
        block_id,
        JSON_OBJECT(
            'paragraph_id', paragraph_id,
            'contents', paragraph_content
        ) AS block_content
    FROM paragraph_level
    GROUP BY scene_id, block_id, paragraph_id
),
scene_level AS (
    SELECT
        scene_id,
        JSON_OBJECT(
            'block_id', block_id,
            'contents', JSON_ARRAYAGG(block_content)
        ) AS scene_content
    FROM block_level
    GROUP BY scene_id, block_id
)
SELECT JSON_OBJECT(
    'title', 'Svartedauden',
    'content', JSON_ARRAYAGG(
        JSON_OBJECT(
            'scene_id', scene_id,
            'contents', scene_content
        )
    )
) AS result
FROM scene_level;







CREATE OR REPLACE VIEW `JSON_texts` AS
SELECT
    JSON_OBJECT(
        'text_id',   `texts`.`text_id`,
        'text_type', `text_types`.`name`,
        'text',      `texts`.`text`
    ) AS `JSON_texts`
FROM
              `texts`
    LEFT JOIN `text_types` USING (`text_type_id`)
ORDER BY
    `texts`.`text_id`
;

CREATE OR REPLACE VIEW `JSON_paragraphs` AS
SELECT
    JSON_OBJECT(
        'paragraph_id', `paragraphs`.`paragraph_id`,
        'contents', JSON_ARRAYAGG(
            JSON_OBJECT(
                'p_order', `paragraphs`.`order`,
                't_order', `paragraph_texts`.`order`,
                't_id', `paragraph_texts`.`text_id`,
                'text', `texts`.`text`
            )
        )
    ) AS `JSON_paragraphs`
FROM
              `paragraphs`
    LEFT JOIN `paragraph_texts`  USING (`paragraph_id`)
    LEFT JOIN `texts`            USING (`text_id`)
GROUP BY
    `paragraphs`.`paragraph_id`
;

SELECT
    JSON_OBJECT(
        'block_id', `blocks`.`block_id`,
        'contents', JSON_ARRAYAGG(
            (SELECT
                `paragraphs`.`paragraph_id`,
                JSON_OBJECT(
                    'paragraph_id', `paragraphs`.`paragraph_id`,
                    'contents', JSON_ARRAYAGG(
                        JSON_OBJECT(
                            'p_order', `paragraphs`.`order`,
                            't_order', `paragraph_texts`.`order`,
                            't_id', `paragraph_texts`.`text_id`,
                            'text', `texts`.`text`
                        )
                    )
                ) AS `JSON_paragraphs`
            FROM
                          `paragraphs`
                LEFT JOIN `paragraph_texts`  USING (`paragraph_id`)
                LEFT JOIN `texts`            USING (`text_id`)
            GROUP BY
                `paragraphs`.`paragraph_id`
            )
        )
    ) AS `JSON_blocks`
FROM
              `blocks`
    LEFT JOIN `paragraphs`       USING (`block_id`)
    LEFT JOIN `paragraph_texts`  USING (`paragraph_id`)
    LEFT JOIN `texts`            USING (`text_id`)
GROUP BY
    `blocks`.`block_id`
;
