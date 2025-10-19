DROP DATABASE `Maridalsspillet_2025`;
CREATE DATABASE `Maridalsspillet_2025`;


CREATE TABLE `Maridalsspillet_2025`.`versions` (
    `version_id`        INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `person_id`         INT UNSIGNED NOT NULL,
    `comment`           VARCHAR (255) DEFAULT NULL,
    `timestamp`         DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`version_id`),
    FOREIGN KEY (`person_id`) REFERENCES `showmaster`.`persons`(`person_id`)
) ENGINE = InnoDB;


CREATE TABLE `Maridalsspillet_2025`.`block_types` (
    `block_type_id`           INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `name`              VARCHAR(255) NOT NULL,
    PRIMARY KEY (`block_type_id`)
) ENGINE = InnoDB;


CREATE TABLE `Maridalsspillet_2025`.`text_types` (
    `text_type_id`           INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `name`              VARCHAR(255) NOT NULL,
    PRIMARY KEY (`text_type_id`)
) ENGINE = InnoDB;


CREATE TABLE `Maridalsspillet_2025`.`characters` (
    `character_id`      INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `version_start`     INT UNSIGNED NOT NULL,
    `version_end`       INT UNSIGNED DEFAULT NULL,
    `name`              VARCHAR(255) NOT NULL,
    PRIMARY KEY (`character_id`),
    FOREIGN KEY (`version_start`) REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    FOREIGN KEY (`version_end`  ) REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`)
) ENGINE = InnoDB;


CREATE TABLE `Maridalsspillet_2025`.`character_groups` (
    `character_group_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `version_start`     INT UNSIGNED NOT NULL,
    `version_end`       INT UNSIGNED DEFAULT NULL,
    `name`              VARCHAR(255) NOT NULL,
    PRIMARY KEY (`character_group_id`),
    FOREIGN KEY (`version_start`) REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    FOREIGN KEY (`version_end`  ) REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`)
) ENGINE = InnoDB;


CREATE TABLE `Maridalsspillet_2025`.`character_group_characters` (
    `character_group_character_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `version_start`             INT UNSIGNED NOT NULL,
    `version_end`               INT UNSIGNED DEFAULT NULL,
    `character_group_id`        INT UNSIGNED NOT NULL,
    `character_id`              INT UNSIGNED NOT NULL,
    PRIMARY KEY (`character_group_character_id`),
    FOREIGN KEY (`version_start`) REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    FOREIGN KEY (`version_end`  ) REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    FOREIGN KEY (`character_group_id`) REFERENCES `Maridalsspillet_2025`.`character_groups`(`character_group_id`),
    FOREIGN KEY (`character_id`) REFERENCES `Maridalsspillet_2025`.`characters`(`character_id`)
) ENGINE = InnoDB;


CREATE TABLE `Maridalsspillet_2025`.`scenes` (
    `scene_id`          INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `version_start`     INT UNSIGNED NOT NULL,
    `version_end`       INT UNSIGNED DEFAULT NULL,
    `id`                VARCHAR(15) NOT NULL,
    `name`              VARCHAR(255) NOT NULL,
    PRIMARY KEY (`scene_id`),
    FOREIGN KEY (`version_start`) REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    FOREIGN KEY (`version_end`  ) REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`)
) ENGINE = InnoDB;


CREATE TABLE `Maridalsspillet_2025`.`texts` (
    `text_id`           INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `version_start`     INT UNSIGNED NOT NULL,
    `version_end`       INT UNSIGNED DEFAULT NULL,
    `text_type_id`      INT UNSIGNED NOT NULL,
    `text`              TEXT NOT NULL,
    PRIMARY KEY (`text_id`),
    FOREIGN KEY (`version_start`) REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    FOREIGN KEY (`version_end`  ) REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    FOREIGN KEY (`text_type_id` ) REFERENCES `Maridalsspillet_2025`.`text_types`(`text_type_id`)
) ENGINE = InnoDB;


CREATE TABLE `Maridalsspillet_2025`.`blocks` (
    `block_id`       INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `version_start`     INT UNSIGNED NOT NULL,
    `version_end`       INT UNSIGNED DEFAULT NULL,
    `scene_id`          INT UNSIGNED NOT NULL,
    `order`             INT UNSIGNED NOT NULL,
    `block_type_id`     INT UNSIGNED NOT NULL,
    `character_group_id` INT UNSIGNED,
    PRIMARY KEY (`block_id`),
    FOREIGN KEY (`version_start`) REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    FOREIGN KEY (`version_end`  ) REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    FOREIGN KEY (`scene_id`     ) REFERENCES `Maridalsspillet_2025`.`scenes`(`scene_id`),
    FOREIGN KEY (`block_type_id`) REFERENCES `Maridalsspillet_2025`.`block_types`(`block_type_id`),
    FOREIGN KEY (`character_group_id`) REFERENCES `Maridalsspillet_2025`.`character_groups`(`character_group_id`)
) ENGINE = InnoDB;


CREATE TABLE `Maridalsspillet_2025`.`paragraphs` (
    `paragraph_id`       INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `version_start`     INT UNSIGNED NOT NULL,
    `version_end`       INT UNSIGNED DEFAULT NULL,
    `block_id`          INT UNSIGNED NOT NULL,
    `order`             INT UNSIGNED NOT NULL,
    PRIMARY KEY (`paragraph_id`),
    FOREIGN KEY (`version_start`) REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    FOREIGN KEY (`version_end`  ) REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    FOREIGN KEY (`block_id`     ) REFERENCES `Maridalsspillet_2025`.`blocks`(`block_id`)
) ENGINE = InnoDB;


CREATE TABLE `Maridalsspillet_2025`.`paragraph_texts` (
    `paragraph_text_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `version_start`     INT UNSIGNED NOT NULL,
    `version_end`       INT UNSIGNED DEFAULT NULL,
    `paragraph_id`      INT UNSIGNED NOT NULL,
    `order`             INT UNSIGNED NOT NULL,
    `text_id`           INT UNSIGNED NOT NULL,
    PRIMARY KEY (`paragraph_text_id`),
    FOREIGN KEY (`version_start`) REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    FOREIGN KEY (`version_end`  ) REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    FOREIGN KEY (`paragraph_id` ) REFERENCES `Maridalsspillet_2025`.`paragraphs`(`paragraph_id`),
    FOREIGN KEY (`text_id`      ) REFERENCES `Maridalsspillet_2025`.`texts`(`text_id`)
) ENGINE = InnoDB;


CREATE TABLE `Maridalsspillet_2025`.`block_metadata` (
    `block_metadata_id`     INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `version_start`     INT UNSIGNED NOT NULL,
    `version_end`       INT UNSIGNED DEFAULT NULL,
    `block_id`          INT UNSIGNED NOT NULL,
    `key`               VARCHAR(255),
    `value`             TEXT,
    PRIMARY KEY (`block_metadata_id`),
    FOREIGN KEY (`version_start`) REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    FOREIGN KEY (`version_end`  ) REFERENCES `Maridalsspillet_2025`.`versions`(`version_id`),
    FOREIGN KEY (`block_id`     ) REFERENCES `Maridalsspillet_2025`.`blocks`(`block_id`)
) ENGINE = InnoDB;
