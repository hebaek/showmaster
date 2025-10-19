DROP PROCEDURE IF EXISTS `maridalsspillet_2025`.`create_and_expire_scenes`;
DROP PROCEDURE IF EXISTS `maridalsspillet_2025`.`insert_content`;



DELIMITER $$



CREATE PROCEDURE `create_and_expire_scenes` (
    IN `current_scenes` JSON,
    IN `version_start`  INT UNSIGNED,
    IN `version_end`    INT UNSIGNED
)
BEGIN
    -- Temporary table for input scenes
    CREATE TEMPORARY TABLE `temp_scenes` (
        `id`                                VARCHAR(15)  NOT NULL,
        `name`                              VARCHAR(255) NOT NULL,
        `scene_order`                       INT UNSIGNED NOT NULL
    );

    -- Populate the temporary table with the JSON data
    INSERT INTO `temp_scenes` (id, name, scene_order)
    SELECT
        JSON_UNQUOTE(JSON_EXTRACT(scenes.value, '$.id')),
        JSON_UNQUOTE(JSON_EXTRACT(scenes.value, '$.name')),
        JSON_UNQUOTE(JSON_EXTRACT(scenes.value, '$.scene_order'))
    FROM JSON_TABLE(`current_scenes`, '$[*]' COLUMNS (
        `value` JSON PATH '$'
    )) AS `scenes`;

    -- Expire scenes that no longer match the input list
    UPDATE `scenes`
    SET `version_end` = `version_end`
    WHERE
        `version_end` IS NULL
        AND NOT EXISTS (
            SELECT 1
            FROM `temp_scenes`
            WHERE
                `temp_scenes`.`id` = `scenes`.`id`
                AND `temp_scenes`.`name`        = `scenes`.`name`
                AND `temp_scenes`.`scene_order` = `scenes`.`scene_order`
        );

    -- Insert new scenes or update existing ones
    INSERT INTO `scenes` (`version_start`, `scene_order`, `id`, `name`)
    SELECT
        `version_start`,
        `scene_order`,
        `id`,
        `name`
    FROM `temp_scenes`
    ON DUPLICATE KEY UPDATE
        `scene_id` = LAST_INSERT_ID(`scene_id`);

    -- Clean up the temporary table
    DROP TEMPORARY TABLE `temp_scenes`;
END$$



CREATE PROCEDURE `insert_content` (
    IN `_version_start`      INT UNSIGNED,
    IN `_scene_id`           INT UNSIGNED,
    IN `_block_order`        INT UNSIGNED,
    IN `_division_order`     INT UNSIGNED,
    IN `_paragraph_order`    INT UNSIGNED,
    IN `_content_order`      INT UNSIGNED,
    IN `_character_alias_id` INT UNSIGNED,
    IN `_text_type`          VARCHAR(32),
    IN `_text`               TEXT
)
BEGIN
    DECLARE `_block_id`      INT;
    DECLARE `_division_id`   INT;
    DECLARE `_paragraph_id`  INT;
    DECLARE `_content_id`    INT;
    DECLARE `_text_id`       INT;


    -- Insert or retrieve text
    INSERT INTO `texts`
        (`text_type`, `text`)
    VALUES
        (`_text_type`, `_text`)
    ON DUPLICATE KEY UPDATE `text_type` = `text_type`;

    SELECT `text_id` INTO `_text_id` FROM `texts`
    WHERE `texts`.`text_type`     = `_text_type`
      AND `texts`.`text`          = `_text`
    LIMIT 1;


    -- Insert or retrieve block
    INSERT INTO `blocks`
        (`version_start`, `block_order`, `scene_id`)
    VALUES
        (`_version_start`, `_block_order`, `_scene_id`)
    ON DUPLICATE KEY UPDATE `block_order` = `block_order`;

    SELECT `block_id` INTO `_block_id` FROM `blocks`
    WHERE `blocks`.`version_start` = `_version_start`
      AND `blocks`.`block_order`   = `_block_order`
      AND `blocks`.`scene_id`      = `_scene_id`
    LIMIT 1;


    -- Insert or retrieve division
    INSERT INTO `divisions`
        (`version_start`, `division_order`, `block_id`)
    VALUES
        (`_version_start`, `_division_order`, `_block_id`)
    ON DUPLICATE KEY UPDATE `division_order` = `division_order`;

    SELECT `division_id` INTO `_division_id` FROM `divisions`
    WHERE `divisions`.`version_start`  = `_version_start`
      AND `divisions`.`division_order` = `_division_order`
      AND `divisions`.`block_id`       = `_block_id`
    LIMIT 1;


    -- Insert or retrieve paragraph
    INSERT INTO `paragraphs`
        (`version_start`, `paragraph_order`, `division_id`)
    VALUES
        (`_version_start`, `_paragraph_order`, `_division_id`)
    ON DUPLICATE KEY UPDATE `paragraph_order` = `paragraph_order`;

    SELECT `paragraph_id` INTO `_paragraph_id` FROM `paragraphs`
    WHERE `paragraphs`.`version_start`   = `_version_start`
      AND `paragraphs`.`paragraph_order` = `_paragraph_order`
      AND `paragraphs`.`division_id`     = `_division_id`
    LIMIT 1;


    -- Insert or retrieve content
    INSERT INTO `content`
        (`version_start`, `content_order`, `paragraph_id`, `character_alias_id`, `text_id`)
    VALUES
        (`_version_start`, `_content_order`, `_paragraph_id`, `_character_alias_id`, `_text_id`)
    ON DUPLICATE KEY UPDATE `content_order` = `content_order`;
END$$



DELIMITER ;



GRANT EXECUTE ON PROCEDURE `maridalsspillet_2025`.`create_and_expire_scenes` TO 'showmaster'@'%';
GRANT EXECUTE ON PROCEDURE `maridalsspillet_2025`.`insert_content`           TO 'showmaster'@'%';