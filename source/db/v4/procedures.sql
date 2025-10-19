DROP PROCEDURE IF EXISTS `maridalsspillet_2025`.`insert_text`;

DELIMITER $$
CREATE PROCEDURE `insert_text` (
    IN `_version_start`      INT UNSIGNED,
    IN `_scene_order`        INT UNSIGNED,
    IN `_scene_name_id`      VARCHAR(15),
    IN `_scene_name`         VARCHAR(255),
    IN `_section_order`      INT UNSIGNED,
    IN `_division_order`     INT UNSIGNED,
    IN `_block_order`        INT UNSIGNED,
    IN `_block_type`         VARCHAR(32),
    IN `_paragraph_order`    INT UNSIGNED,
    IN `_line_order`         INT UNSIGNED,
    IN `_line_type`          VARCHAR(32),
    IN `_text`               TEXT
)
BEGIN
    DECLARE `_scene_id`      INT;
    DECLARE `_section_id`    INT;
    DECLARE `_division_id`   INT;
    DECLARE `_block_id`      INT;
    DECLARE `_paragraph_id`  INT;
    DECLARE `_text_id`       INT;


    -- Insert or retrieve scene
    INSERT INTO `scenes` (`version_start`, `scene_order`, `id`, `name`)
    VALUES (`_version_start`, `_scene_order`, `_scene_name_id`, `_scene_name`)
    ON DUPLICATE KEY UPDATE `scene_order` = `scene_order`;

    SELECT `scene_id` INTO `_scene_id` FROM `scenes`
    WHERE `scenes`.`version_end` IS NULL
      AND `scenes`.`id`          = `_scene_name_id`
      AND `scenes`.`name`        = `_scene_name`
    LIMIT 1;


    -- Insert or retrieve section
    INSERT INTO `sections` (`version_start`, `scene_id`, `section_order`)
    VALUES (`_version_start`, `_scene_id`, `_section_order`)
    ON DUPLICATE KEY UPDATE `section_order` = `section_order`;

    SELECT `section_id` INTO `_section_id` FROM `sections`
    WHERE `sections`.`version_end`   IS NULL
      AND `sections`.`scene_id`      = `_scene_id`
      AND `sections`.`section_order` = `_section_order`
    LIMIT 1;


    -- Insert or retrieve division
    INSERT INTO `divisions` (`version_start`, `division_order`, `section_id`)
    VALUES (`_version_start`, `_division_order`, `_section_id`)
    ON DUPLICATE KEY UPDATE `division_order` = `division_order`;

    SELECT `division_id` INTO `_division_id` FROM `divisions`
    WHERE `divisions`.`version_end`    IS NULL
      AND `divisions`.`division_order` = `_division_order`
      AND `divisions`.`section_id`     = `_section_id`
    LIMIT 1;


    -- Insert or retrieve block
    INSERT INTO `blocks` (`version_start`, `block_order`, `division_id`, `block_type`)
    VALUES (`_version_start`, `_block_order`, `_division_id`, `_block_type`)
    ON DUPLICATE KEY UPDATE `block_order` = `block_order`;

    SELECT `block_id` INTO `_block_id` FROM `blocks`
    WHERE `blocks`.`version_end` IS NULL
      AND `blocks`.`block_order` = `_block_order`
      AND `blocks`.`division_id` = `_division_id`
    LIMIT 1;


    -- Insert or retrieve paragraph
    INSERT INTO `paragraphs` (`version_start`, `paragraph_order`, `block_id`)
    VALUES (`_version_start`, `_paragraph_order`, `_block_id`)
    ON DUPLICATE KEY UPDATE `paragraph_order` = `paragraph_order`;

    SELECT `paragraph_id` INTO `_paragraph_id` FROM `paragraphs`
    WHERE `paragraphs`.`version_end`     IS NULL
      AND `paragraphs`.`paragraph_order` = `_paragraph_order`
      AND `paragraphs`.`block_id`        = `_block_id`
    LIMIT 1;


    -- Insert or retrieve text
    INSERT INTO `texts` (`text`)
    VALUES (`_text`)
    ON DUPLICATE KEY UPDATE `text` = `text`;

    SELECT `text_id` INTO `_text_id` FROM `texts`
    WHERE `texts`.`text` = `_text`
    LIMIT 1;


    -- Insert or retrieve line
    INSERT INTO `lines` (`version_start`, `line_order`, `paragraph_id`, `line_type`, `text_id`)
    VALUES (`_version_start`, `_line_order`, `_paragraph_id`, `_line_type`, `_text_id`)
    ON DUPLICATE KEY UPDATE `line_order` = `line_order`;

END$$

DELIMITER ;
