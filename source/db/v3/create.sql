DROP DATABASE IF EXISTS `Maridalsspillet_2025`;
CREATE DATABASE `Maridalsspillet_2025`;

USE `Maridalsspillet_2025`;


/****************************************************************************************
*
*   Versions and parts
*
*****************************************************************************************/

CREATE TABLE `Maridalsspillet_2025`.`versions` (
    `version_id`                        INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `person_id`                         INT UNSIGNED DEFAULT NULL,
    `timestamp`                         DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `name`                              VARCHAR (255) UNIQUE DEFAULT NULL,
    `comment`                           VARCHAR (255) DEFAULT NULL,

    PRIMARY KEY (`version_id`),
    FOREIGN KEY (`person_id`)           REFERENCES `showmaster`.`persons`(`person_id`)
) ENGINE = InnoDB;



CREATE TABLE `Maridalsspillet_2025`.`parts` (
    `part_id`                           INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `version_start`                     INT UNSIGNED NOT NULL,
    `version_end`                       INT UNSIGNED DEFAULT NULL,
    `part_order`                        INT UNSIGNED NOT NULL,
    `comment`                           VARCHAR(255) DEFAULT NULL,

    PRIMARY KEY (`part_id`),
    FOREIGN KEY (`version_start`)       REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    FOREIGN KEY (`version_end`)         REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),

    INDEX `part_order` (`part_order`)
) ENGINE = InnoDB;



/****************************************************************************************
*
*   Texts
*
*****************************************************************************************/

CREATE TABLE `Maridalsspillet_2025`.`texts` (
    `text_id`                           INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `text_type`                         ENUM(
                                            'dialogue',
                                            'song',
                                            'parenthetical',
                                            'action',
                                            'cue',
                                            'comment') NOT NULL,
    `text`                              TEXT NOT NULL,
    `person_id`                         INT UNSIGNED DEFAULT NULL COMMENT 'Author',
    `unique_key` BINARY(32)             AS (UNHEX(SHA2(CONCAT(`text_type`, `text`), 256))) STORED,

    PRIMARY KEY (`text_id`),
    UNIQUE  KEY (`unique_key`)
) ENGINE = InnoDB;



/****************************************************************************************
*
*   Characters
*
*****************************************************************************************/

CREATE TABLE `Maridalsspillet_2025`.`characters` (
    `character_id`                      INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `version_start`                     INT UNSIGNED NOT NULL,
    `version_end`                       INT UNSIGNED DEFAULT NULL,
    `name`                              VARCHAR(255) NOT NULL,
    `description`                       VARCHAR(255) DEFAULT NULL,
    `comment`                           VARCHAR(255) DEFAULT NULL,
    `unique_key` BINARY(32)             AS (UNHEX(SHA2(CONCAT(COALESCE(`version_end`, 0), `name`), 256))) STORED,

    PRIMARY KEY (`character_id`),
    FOREIGN KEY (`version_start`)       REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    FOREIGN KEY (`version_end`)         REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    UNIQUE  KEY (`unique_key`)
) ENGINE = InnoDB;



CREATE TABLE `Maridalsspillet_2025`.`character_aliases` (
    `character_alias_id`                INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `version_start`                     INT UNSIGNED NOT NULL,
    `version_end`                       INT UNSIGNED DEFAULT NULL,
    `name`                              VARCHAR(255) NOT NULL,
    `description`                       VARCHAR(255) DEFAULT NULL,
    `comment`                           VARCHAR(255) DEFAULT NULL,
    `unique_key` BINARY(32)             AS (UNHEX(SHA2(CONCAT(COALESCE(`version_end`, 0), `name`), 256))) STORED,

    PRIMARY KEY (`character_alias_id`),
    FOREIGN KEY (`version_start`)       REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    FOREIGN KEY (`version_end`)         REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    UNIQUE  KEY (`unique_key`)
) ENGINE = InnoDB;



CREATE TABLE `Maridalsspillet_2025`.`character_alias_characters` (
    `character_alias_characters_id`     INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `version_start`                     INT UNSIGNED NOT NULL,
    `version_end`                       INT UNSIGNED DEFAULT NULL,
    `part_start`                        INT UNSIGNED NOT NULL,
    `part_end`                          INT UNSIGNED DEFAULT NULL,
    `character_alias_id`                INT UNSIGNED DEFAULT NULL,
    `character_id`                      INT UNSIGNED DEFAULT NULL,

    PRIMARY KEY (`character_alias_characters_id`),
    FOREIGN KEY (`version_start`)       REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    FOREIGN KEY (`version_end`)         REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    FOREIGN KEY (`part_start`)          REFERENCES `Maridalsspillet_2025`.`parts`(`part_id`),
    FOREIGN KEY (`part_end`)            REFERENCES `Maridalsspillet_2025`.`parts`(`part_id`),
    FOREIGN KEY (`character_alias_id`)  REFERENCES `Maridalsspillet_2025`.`character_aliases`(`character_alias_id`),
    FOREIGN KEY (`character_id`)        REFERENCES `Maridalsspillet_2025`.`characters`(`character_id`)
) ENGINE = InnoDB;



/****************************************************************************************
*
*   Scenes, blocks and paragraphs
*
*****************************************************************************************/

CREATE TABLE `Maridalsspillet_2025`.`scenes` (
    `scene_id`                          INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `version_start`                     INT UNSIGNED NOT NULL,
    `version_end`                       INT UNSIGNED DEFAULT NULL,
    `scene_order`                       INT UNSIGNED NOT NULL,
    `id`                                VARCHAR(15) NOT NULL,
    `name`                              VARCHAR(255) NOT NULL,
    `unique_key` BINARY(32)             AS (UNHEX(SHA2(CONCAT(COALESCE(`version_end`, 0), `scene_order`, `id`, `name`), 256))) STORED,

    PRIMARY KEY (`scene_id`),
    FOREIGN KEY (`version_start`)       REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    FOREIGN KEY (`version_end`)         REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    UNIQUE  KEY (`unique_key`),

    INDEX `scene_order` (`scene_order`)
) ENGINE = InnoDB;



CREATE TABLE `Maridalsspillet_2025`.`blocks` (
    `block_id`                          INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `version_start`                     INT UNSIGNED NOT NULL,
    `version_end`                       INT UNSIGNED DEFAULT NULL,
    `block_order`                       INT UNSIGNED NOT NULL,
    `scene_id`                          INT UNSIGNED NOT NULL,
    `unique_key` BINARY(32)             AS (UNHEX(SHA2(CONCAT(COALESCE(`version_end`, 0), `block_order`, `scene_id`), 256))) STORED,

    PRIMARY KEY (`block_id`),
    FOREIGN KEY (`version_start`)       REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    FOREIGN KEY (`version_end`)         REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    FOREIGN KEY (`scene_id`)            REFERENCES `Maridalsspillet_2025`.`scenes`(`scene_id`),
    UNIQUE  KEY (`unique_key`),

    INDEX `block_order` (`block_order`)
) ENGINE = InnoDB;



CREATE TABLE `Maridalsspillet_2025`.`divisions` (
    `division_id`                       INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `version_start`                     INT UNSIGNED NOT NULL,
    `version_end`                       INT UNSIGNED DEFAULT NULL,
    `division_order`                    INT UNSIGNED NOT NULL,
    `block_id`                          INT UNSIGNED NOT NULL,
    `unique_key` BINARY(32)             AS (UNHEX(SHA2(CONCAT(COALESCE(`version_end`, 0), `division_order`, `block_id`), 256))) STORED,

    PRIMARY KEY (`division_id`),
    FOREIGN KEY (`version_start`)       REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    FOREIGN KEY (`version_end`)         REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    FOREIGN KEY (`block_id`)            REFERENCES `Maridalsspillet_2025`.`blocks`(`block_id`),
    UNIQUE  KEY (`unique_key`),

    INDEX `division_order` (`division_order`)
) ENGINE = InnoDB;



CREATE TABLE `Maridalsspillet_2025`.`paragraphs` (
    `paragraph_id`                      INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `version_start`                     INT UNSIGNED NOT NULL,
    `version_end`                       INT UNSIGNED DEFAULT NULL,
    `paragraph_order`                   INT UNSIGNED NOT NULL,
    `division_id`                       INT UNSIGNED NOT NULL,
    `unique_key` BINARY(32)             AS (UNHEX(SHA2(CONCAT(COALESCE(`version_end`, 0), `paragraph_order`, `division_id`), 256))) STORED,

    PRIMARY KEY (`paragraph_id`),
    FOREIGN KEY (`version_start`)       REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    FOREIGN KEY (`version_end`)         REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    FOREIGN KEY (`division_id`)         REFERENCES `Maridalsspillet_2025`.`divisions`(`division_id`),
    UNIQUE  KEY (`unique_key`),

    INDEX `paragraph_order` (`paragraph_order`)
) ENGINE = InnoDB;



/****************************************************************************************
*
*   Content
*
*****************************************************************************************/

CREATE TABLE `Maridalsspillet_2025`.`content` (
    `content_id`                        INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `version_start`                     INT UNSIGNED NOT NULL,
    `version_end`                       INT UNSIGNED DEFAULT NULL,
    `content_order`                     INT UNSIGNED NOT NULL,
    `content_type`                      ENUM(
                                            'dialogue',
                                            'action',
                                            'cue') NOT NULL,
    `paragraph_id`                      INT UNSIGNED NOT NULL,
    `character_alias_id`                INT UNSIGNED DEFAULT NULL,
    `text_id`                           INT UNSIGNED NOT NULL,
    `unique_key` BINARY(32)             AS (UNHEX(SHA2(CONCAT(COALESCE(`version_end`, 0), `content_order`, `content_type`, `paragraph_id`, COALESCE(`character_alias_id`, 0), `text_id`), 256))) STORED,

    PRIMARY KEY (`content_id`),
    FOREIGN KEY (`version_start`)       REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    FOREIGN KEY (`version_end`)         REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    FOREIGN KEY (`paragraph_id`)        REFERENCES `Maridalsspillet_2025`.`paragraphs`(`paragraph_id`),
    FOREIGN KEY (`character_alias_id`)  REFERENCES `Maridalsspillet_2025`.`character_aliases`(`character_alias_id`),
    FOREIGN KEY (`text_id`)             REFERENCES `Maridalsspillet_2025`.`texts`(`text_id`),
    UNIQUE  KEY (`unique_key`)
) ENGINE = InnoDB;



/****************************************************************************************
*
*   Views
*
*****************************************************************************************/

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



CREATE OR REPLACE VIEW `view_content` AS
SELECT
    `scenes`.`scene_id`,
    `blocks`.`block_id`,
    `divisions`.`division_id`,
    `paragraphs`.`paragraph_id`,
    `content`.`content_id`,
    `scenes`.`id`,
    `scenes`.`name` AS `scene_name`,
    `texts`.`text_type`,
    `character_aliases`.`name`,
    `texts`.`text`
FROM
              `content`
    LEFT JOIN `paragraphs`        USING (`paragraph_id`)
    LEFT JOIN `divisions`         USING (`division_id`)
    LEFT JOIN `blocks`            USING (`block_id`)
    LEFT JOIN `scenes`            USING (`scene_id`)
    LEFT JOIN `character_aliases` USING (`character_alias_id`)
    LEFT JOIN `texts`             USING (`text_id`)
WHERE
    `content`.`version_end` IS NULL
ORDER BY
    `scene_order`,
    `block_order`,
    `division_order`,
    `paragraph_order`,
    `content_order`
;
