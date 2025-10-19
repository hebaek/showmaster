INSERT INTO `Maridalsspillet_2025`.`versions` (`person_id`, `name`, `comment`) VALUES
    (NULL, NULL, NULL)
;



INSERT INTO `Maridalsspillet_2025`.`parts` (`version_start`, `order`, `comment`) VALUES
    (1, 1, NULL)
;



INSERT INTO `Maridalsspillet_2025`.`characters` (`version_start`, `name`, `description`, `comment`) VALUES
    (1, 'Sigrunn',        'Bonde på Tømte gård.', NULL),
    (1, 'Ogmund',         '', NULL),
    (1, 'Marit',          'Sigrunn sin datter.', NULL),
    (1, 'Jon',            'Bonde på Brekke gård. Søskenbarnet til Marit.', NULL),
    (1, 'Sira Lars',      'Prest i Margaretadalen.', NULL),
    (1, 'Tordis',         'Styrer huset for presten.', NULL),
    (1, 'Knut Rask',      'Prostens årmann.', NULL),
    (1, 'Arne Aslaksson', 'Prost til Mariakirken og rikets kansler.', NULL),
    (1, 'bonde 1',        '', NULL),
    (1, 'bonde 2',        '', NULL),
    (1, 'bonde 3',        '', NULL),
    (1, 'knekt 1',        '', NULL),
    (1, 'knekt 2',        '', NULL),
    (1, 'jente 1',        '', NULL),
    (1, 'jente 2',        '', NULL),
    (1, 'budbringer',     '', NULL)
;



INSERT INTO `Maridalsspillet_2025`.`character_aliases` (`version_start`, `part_start`, `name`, `character_id`) VALUES
    (1, 1, 'Sigrunn',           (SELECT `character_id` FROM `characters` WHERE `name` = 'Sigrunn'          )),
    (1, 1, 'Ogmund',            (SELECT `character_id` FROM `characters` WHERE `name` = 'Ogmund'           )),
    (1, 1, 'Marit',             (SELECT `character_id` FROM `characters` WHERE `name` = 'Marit'            )),
    (1, 1, 'unge Marit',        (SELECT `character_id` FROM `characters` WHERE `name` = 'Marit'            )),
    (1, 1, 'Jon',               (SELECT `character_id` FROM `characters` WHERE `name` = 'Jon'              )),
    (1, 1, 'unge Jon',          (SELECT `character_id` FROM `characters` WHERE `name` = 'Jon'              )),
    (1, 1, 'Sira Lars',         (SELECT `character_id` FROM `characters` WHERE `name` = 'Sira Lars'        )),
    (1, 1, 'Tordis',            (SELECT `character_id` FROM `characters` WHERE `name` = 'Tordis'           )),
    (1, 1, 'Knut Rask',         (SELECT `character_id` FROM `characters` WHERE `name` = 'Knut Rask'        )),
    (1, 1, 'Rask',              (SELECT `character_id` FROM `characters` WHERE `name` = 'Knut Rask'        )),
    (1, 1, 'Arne Aslaksson',    (SELECT `character_id` FROM `characters` WHERE `name` = 'Arne Aslaksson'   )),
    (1, 1, 'Aslaksson',         (SELECT `character_id` FROM `characters` WHERE `name` = 'Arne Aslaksson'   )),
    (1, 1, 'bonde 1',           (SELECT `character_id` FROM `characters` WHERE `name` = 'bonde 1'          )),
    (1, 1, 'bonde 2',           (SELECT `character_id` FROM `characters` WHERE `name` = 'bonde 2'          )),
    (1, 1, 'bonde 3',           (SELECT `character_id` FROM `characters` WHERE `name` = 'bonde 3'          )),
    (1, 1, 'bøndene',           (SELECT `character_id` FROM `characters` WHERE `name` = 'bonde 1'          )),
    (1, 1, 'bøndene',           (SELECT `character_id` FROM `characters` WHERE `name` = 'bonde 2'          )),
    (1, 1, 'bøndene',           (SELECT `character_id` FROM `characters` WHERE `name` = 'bonde 3'          )),
    (1, 1, 'bønder',            (SELECT `character_id` FROM `characters` WHERE `name` = 'bonde 1'          )),
    (1, 1, 'bønder',            (SELECT `character_id` FROM `characters` WHERE `name` = 'bonde 2'          )),
    (1, 1, 'bønder',            (SELECT `character_id` FROM `characters` WHERE `name` = 'bonde 3'          )),
    (1, 1, 'knekt 1',           (SELECT `character_id` FROM `characters` WHERE `name` = 'knekt 1'          )),
    (1, 1, 'knekt 2',           (SELECT `character_id` FROM `characters` WHERE `name` = 'knekt 2'          )),
    (1, 1, 'knektene',          (SELECT `character_id` FROM `characters` WHERE `name` = 'knekt 1'          )),
    (1, 1, 'knektene',          (SELECT `character_id` FROM `characters` WHERE `name` = 'knekt 2'          )),
    (1, 1, 'knekter',           (SELECT `character_id` FROM `characters` WHERE `name` = 'knekt 1'          )),
    (1, 1, 'knekter',           (SELECT `character_id` FROM `characters` WHERE `name` = 'knekt 2'          )),
    (1, 1, 'Marit og Jon',      (SELECT `character_id` FROM `characters` WHERE `name` = 'Marit'            )),
    (1, 1, 'Marit og Jon',      (SELECT `character_id` FROM `characters` WHERE `name` = 'Jon'              )),
    (1, 1, 'Sigrunn og bønder', (SELECT `character_id` FROM `characters` WHERE `name` = 'Sigrunn'          )),
    (1, 1, 'Sigrunn og bønder', (SELECT `character_id` FROM `characters` WHERE `name` = 'bonde 1'          )),
    (1, 1, 'Sigrunn og bønder', (SELECT `character_id` FROM `characters` WHERE `name` = 'bonde 2'          )),
    (1, 1, 'Sigrunn og bønder', (SELECT `character_id` FROM `characters` WHERE `name` = 'bonde 3'          )),
    (1, 1, 'jente 1',           (SELECT `character_id` FROM `characters` WHERE `name` = 'jente 1'          )),
    (1, 1, 'jente 2',           (SELECT `character_id` FROM `characters` WHERE `name` = 'jente 2'          )),
    (1, 1, 'jente 1 + 2',       (SELECT `character_id` FROM `characters` WHERE `name` = 'jente 1'          )),
    (1, 1, 'jente 1 + 2',       (SELECT `character_id` FROM `characters` WHERE `name` = 'jente 2'          )),
    (1, 1, 'jentene',           (SELECT `character_id` FROM `characters` WHERE `name` = 'jente 1'          )),
    (1, 1, 'jentene',           (SELECT `character_id` FROM `characters` WHERE `name` = 'jente 2'          )),
    (1, 1, 'budbringer',        (SELECT `character_id` FROM `characters` WHERE `name` = 'budbringer'       )),
    (1, 1, 'alle',              NULL)
;
