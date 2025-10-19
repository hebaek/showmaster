DROP DATABASE `Maridalsspillet_2025`;
CREATE DATABASE `Maridalsspillet_2025`;



/****************************************************************************************
*
*   Versions and parts
*
*****************************************************************************************/

CREATE TABLE `Maridalsspillet_2025`.`versions` (
    `version_id`                        INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `person_id`                         INT UNSIGNED DEFAULT NULL,
    `timestamp`                         DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `name`                              VARCHAR (255) DEFAULT NULL,
    `comment`                           VARCHAR (255) DEFAULT NULL,
    PRIMARY KEY (`version_id`),
    FOREIGN KEY (`person_id`)           REFERENCES `showmaster`.`persons`(`person_id`)
) ENGINE = InnoDB;



CREATE TABLE `Maridalsspillet_2025`.`parts` (
    `part_id`                           INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `version_start`                     INT UNSIGNED NOT NULL,
    `version_end`                       INT UNSIGNED DEFAULT NULL,
    `order`                             INT UNSIGNED NOT NULL,
    `comment`                           VARCHAR(255) DEFAULT NULL,
    PRIMARY KEY (`part_id`),
    FOREIGN KEY (`version_start`)       REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    FOREIGN KEY (`version_end`)         REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    INDEX `order` (`order`)
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
    PRIMARY KEY (`character_id`),
    FOREIGN KEY (`version_start`)       REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    FOREIGN KEY (`version_end`)         REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    UNIQUE (`name`)
) ENGINE = InnoDB;



CREATE TABLE `Maridalsspillet_2025`.`character_aliases` (
    `character_alias_id`                INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `version_start`                     INT UNSIGNED NOT NULL,
    `version_end`                       INT UNSIGNED DEFAULT NULL,
    `part_start`                        INT UNSIGNED NOT NULL,
    `part_end`                          INT UNSIGNED DEFAULT NULL,
    `name`                              VARCHAR(255) NOT NULL,
    `character_id`                      INT UNSIGNED DEFAULT NULL,
    PRIMARY KEY (`character_alias_id`),
    FOREIGN KEY (`version_start`)       REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    FOREIGN KEY (`version_end`)         REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    FOREIGN KEY (`part_start`)          REFERENCES `Maridalsspillet_2025`.`parts`(`part_id`),
    FOREIGN KEY (`part_end`)            REFERENCES `Maridalsspillet_2025`.`parts`(`part_id`),
    FOREIGN KEY (`character_id`)        REFERENCES `Maridalsspillet_2025`.`characters`(`character_id`)
) ENGINE = InnoDB;



/****************************************************************************************
*
*   Scenes
*
*****************************************************************************************/

CREATE TABLE `Maridalsspillet_2025`.`scenes` (
    `scene_id`                          INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `version_start`                     INT UNSIGNED NOT NULL,
    `version_end`                       INT UNSIGNED DEFAULT NULL,
    `order`                             INT UNSIGNED NOT NULL,
    `id`                                VARCHAR(15) NOT NULL,
    `name`                              VARCHAR(255) NOT NULL,
    PRIMARY KEY (`scene_id`),
    FOREIGN KEY (`version_start`)       REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    FOREIGN KEY (`version_end`)         REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    INDEX `order` (`order`)
) ENGINE = InnoDB;



/****************************************************************************************
*
*   Texts
*
*****************************************************************************************/

CREATE TABLE `Maridalsspillet_2025`.`texts` (
    `text_id`                           INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `version_start`                     INT UNSIGNED NOT NULL,
    `version_end`                       INT UNSIGNED DEFAULT NULL,
    `order`                             INT UNSIGNED NOT NULL,
    `text_type`                         ENUM(
                                            'dialogue',
                                            'song',
                                            'parenthetical',
                                            'action',
                                            'cue',
                                            'comment') NOT NULL,
    `text`                              TEXT NOT NULL,
    `person_id`                         INT UNSIGNED DEFAULT NULL COMMENT 'Author',
    PRIMARY KEY (`text_id`),
    FOREIGN KEY (`version_start`)       REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    FOREIGN KEY (`version_end`)         REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    INDEX `order` (`order`)
) ENGINE = InnoDB;



CREATE TABLE `Maridalsspillet_2025`.`text_metadata` (
    `text_metadata_id`                  INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `text_id`                           INT UNSIGNED NOT NULL,
    `key`                               VARCHAR(255) NOT NULL,
    `value`                             VARCHAR(255) NOT NULL,
    PRIMARY KEY (`text_metadata_id`),
    FOREIGN KEY (`text_id`)             REFERENCES `Maridalsspillet_2025`.`texts`(`text_id`)
) ENGINE = InnoDB;
