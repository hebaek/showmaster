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
*   Texts
*
*****************************************************************************************/

CREATE TABLE `Maridalsspillet_2025`.`texts` (
    `text_id`                           INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `text`                              TEXT NOT NULL,
    `unique_key` BINARY(32)             AS (UNHEX(SHA2(`text`, 256))) STORED,

    PRIMARY KEY (`text_id`),
    UNIQUE  KEY (`unique_key`)
) ENGINE = InnoDB;



/****************************************************************************************
*
*   Scenes, sections and divisions
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



CREATE TABLE `Maridalsspillet_2025`.`sections` (
    `section_id`                        INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `version_start`                     INT UNSIGNED NOT NULL,
    `version_end`                       INT UNSIGNED DEFAULT NULL,
    `section_order`                     INT UNSIGNED NOT NULL,
    `scene_id`                          INT UNSIGNED NOT NULL,
    `unique_key` BINARY(32)             AS (UNHEX(SHA2(CONCAT(COALESCE(`version_end`, 0), `section_order`, `scene_id`), 256))) STORED,

    PRIMARY KEY (`section_id`),
    FOREIGN KEY (`version_start`)       REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    FOREIGN KEY (`version_end`)         REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    FOREIGN KEY (`scene_id`)            REFERENCES `Maridalsspillet_2025`.`scenes`(`scene_id`),
    UNIQUE  KEY (`unique_key`),

    INDEX `section_order` (`section_order`)
) ENGINE = InnoDB;



CREATE TABLE `Maridalsspillet_2025`.`divisions` (
    `division_id`                       INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `version_start`                     INT UNSIGNED NOT NULL,
    `version_end`                       INT UNSIGNED DEFAULT NULL,
    `division_order`                    INT UNSIGNED NOT NULL,
    `section_id`                        INT UNSIGNED NOT NULL,
    `unique_key` BINARY(32)             AS (UNHEX(SHA2(CONCAT(COALESCE(`version_end`, 0), `division_order`, `section_id`), 256))) STORED,

    PRIMARY KEY (`division_id`),
    FOREIGN KEY (`version_start`)       REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    FOREIGN KEY (`version_end`)         REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    FOREIGN KEY (`section_id`)          REFERENCES `Maridalsspillet_2025`.`sections`(`section_id`),
    UNIQUE  KEY (`unique_key`),

    INDEX `division_order` (`division_order`)
) ENGINE = InnoDB;



/****************************************************************************************
*
*   Blocks, paragraphs and lines
*
*****************************************************************************************/

CREATE TABLE `Maridalsspillet_2025`.`blocks` (
    `block_id`                          INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `version_start`                     INT UNSIGNED NOT NULL,
    `version_end`                       INT UNSIGNED DEFAULT NULL,
    `block_order`                       INT UNSIGNED NOT NULL,
    `block_type`                        ENUM(
                                            'dialogue',
                                            'action',
                                            'cue',
                                            'comment') NOT NULL,
    `division_id`                       INT UNSIGNED NOT NULL,
    `unique_key` BINARY(32)             AS (UNHEX(SHA2(CONCAT(COALESCE(`version_end`, 0), `block_order`, `block_type`, `division_id`), 256))) STORED,

    PRIMARY KEY (`block_id`),
    FOREIGN KEY (`version_start`)       REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    FOREIGN KEY (`version_end`)         REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    FOREIGN KEY (`division_id`)         REFERENCES `Maridalsspillet_2025`.`divisions`(`division_id`),
    UNIQUE  KEY (`unique_key`),

    INDEX `block_order` (`block_order`)
) ENGINE = InnoDB;



CREATE TABLE `Maridalsspillet_2025`.`paragraphs` (
    `paragraph_id`                      INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `version_start`                     INT UNSIGNED NOT NULL,
    `version_end`                       INT UNSIGNED DEFAULT NULL,
    `paragraph_order`                   INT UNSIGNED NOT NULL,
    `block_id`                          INT UNSIGNED NOT NULL,
    `unique_key` BINARY(32)             AS (UNHEX(SHA2(CONCAT(COALESCE(`version_end`, 0), `paragraph_order`, `block_id`), 256))) STORED,

    PRIMARY KEY (`paragraph_id`),
    FOREIGN KEY (`version_start`)       REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    FOREIGN KEY (`version_end`)         REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    FOREIGN KEY (`block_id`)           REFERENCES `Maridalsspillet_2025`.`blocks`(`block_id`),
    UNIQUE  KEY (`unique_key`),

    INDEX `paragraph_order` (`paragraph_order`)
) ENGINE = InnoDB;



CREATE TABLE `Maridalsspillet_2025`.`lines` (
    `line_id`                           INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `version_start`                     INT UNSIGNED NOT NULL,
    `version_end`                       INT UNSIGNED DEFAULT NULL,
    `line_order`                        INT UNSIGNED NOT NULL,
    `paragraph_id`                      INT UNSIGNED NOT NULL,
    `line_type`                         ENUM(
                                            'dialogue',
                                            'song',
                                            'parenthetical',
                                            'action',
                                            'cue',
                                            'comment') NOT NULL,
    `text_id`                           INT UNSIGNED NOT NULL,
    `unique_key` BINARY(32)             AS (UNHEX(SHA2(CONCAT(COALESCE(`version_end`, 0), `line_order`, `paragraph_id`, `line_type`, `text_id`), 256))) STORED,

    PRIMARY KEY (`line_id`),
    FOREIGN KEY (`version_start`)       REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    FOREIGN KEY (`version_end`)         REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    FOREIGN KEY (`paragraph_id`)        REFERENCES `Maridalsspillet_2025`.`paragraphs`(`paragraph_id`),
    FOREIGN KEY (`text_id`)             REFERENCES `Maridalsspillet_2025`.`texts`(`text_id`),
    UNIQUE  KEY (`unique_key`),

    INDEX `line_order` (`line_order`)
) ENGINE = InnoDB;



/****************************************************************************************
*
*   Dialogue
*
*****************************************************************************************/

CREATE TABLE `Maridalsspillet_2025`.`dialogue_blocks` (
    `dialogue_block_id`                 INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `version_start`                     INT UNSIGNED NOT NULL,
    `version_end`                       INT UNSIGNED DEFAULT NULL,
    `block_id`                          INT UNSIGNED NOT NULL,
    `character_alias_id`                INT UNSIGNED DEFAULT NULL,
    `unique_key` BINARY(32)             AS (UNHEX(SHA2(CONCAT(COALESCE(`version_end`, 0), `block_id`, `character_alias_id`), 256))) STORED,

    PRIMARY KEY (`dialogue_block_id`),
    FOREIGN KEY (`version_start`)       REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    FOREIGN KEY (`version_end`)         REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    FOREIGN KEY (`block_id`)            REFERENCES `Maridalsspillet_2025`.`blocks`(`block_id`),
    FOREIGN KEY (`character_alias_id`)  REFERENCES `Maridalsspillet_2025`.`character_aliases`(`character_alias_id`)
) ENGINE = InnoDB;
