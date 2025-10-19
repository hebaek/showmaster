INSERT INTO `Maridalsspillet_2025`.`versions` (`person_id`, `name`, `comment`) VALUES
    (NULL, NULL, NULL)
;



INSERT INTO `Maridalsspillet_2025`.`parts` (`version_start`, `part_order`, `comment`) VALUES
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



INSERT INTO `Maridalsspillet_2025`.`character_aliases` (`version_start`, `name`, `description`, `comment`) VALUES
    (1, 'Sigrunn',           NULL, NULL),
    (1, 'Ogmund',            NULL, NULL),
    (1, 'Marit',             NULL, NULL),
    (1, 'unge Marit',        NULL, NULL),
    (1, 'Jon',               NULL, NULL),
    (1, 'unge Jon',          NULL, NULL),
    (1, 'Sira Lars',         NULL, NULL),
    (1, 'Tordis',            NULL, NULL),
    (1, 'Knut Rask',         NULL, NULL),
    (1, 'Rask',              NULL, NULL),
    (1, 'Arne Aslaksson',    NULL, NULL),
    (1, 'Aslaksson',         NULL, NULL),
    (1, 'bonde 1',           NULL, NULL),
    (1, 'bonde 2',           NULL, NULL),
    (1, 'bonde 3',           NULL, NULL),
    (1, 'bøndene',           NULL, NULL),
    (1, 'bønder',            NULL, NULL),
    (1, 'knekt 1',           NULL, NULL),
    (1, 'knekt 2',           NULL, NULL),
    (1, 'knektene',          NULL, NULL),
    (1, 'knekter',           NULL, NULL),
    (1, 'Marit og Jon',      NULL, NULL),
    (1, 'Sigrunn og bønder', NULL, NULL),
    (1, 'jente 1',           NULL, NULL),
    (1, 'jente 2',           NULL, NULL),
    (1, 'jente 1 + 2',       NULL, NULL),
    (1, 'jentene',           NULL, NULL),
    (1, 'budbringer',        NULL, NULL),
    (1, 'alle',              NULL, 'Not linked to any character')
;



INSERT INTO `Maridalsspillet_2025`.`character_alias_characters` (`version_start`, `part_start`, `character_alias_id`, `character_id`) VALUES
    (1, 1, (SELECT `character_alias_id` FROM `character_aliases` WHERE `name` = 'Sigrunn'          ), (SELECT `character_id` FROM `characters` WHERE `name` = 'Sigrunn'       )),
    (1, 1, (SELECT `character_alias_id` FROM `character_aliases` WHERE `name` = 'Ogmund'           ), (SELECT `character_id` FROM `characters` WHERE `name` = 'Ogmund'        )),
    (1, 1, (SELECT `character_alias_id` FROM `character_aliases` WHERE `name` = 'Marit'            ), (SELECT `character_id` FROM `characters` WHERE `name` = 'Marit'         )),
    (1, 1, (SELECT `character_alias_id` FROM `character_aliases` WHERE `name` = 'unge Marit'       ), (SELECT `character_id` FROM `characters` WHERE `name` = 'Marit'         )),
    (1, 1, (SELECT `character_alias_id` FROM `character_aliases` WHERE `name` = 'Jon'              ), (SELECT `character_id` FROM `characters` WHERE `name` = 'Jon'           )),
    (1, 1, (SELECT `character_alias_id` FROM `character_aliases` WHERE `name` = 'unge Jon'         ), (SELECT `character_id` FROM `characters` WHERE `name` = 'Jon'           )),
    (1, 1, (SELECT `character_alias_id` FROM `character_aliases` WHERE `name` = 'Sira Lars'        ), (SELECT `character_id` FROM `characters` WHERE `name` = 'Sira Lars'     )),
    (1, 1, (SELECT `character_alias_id` FROM `character_aliases` WHERE `name` = 'Tordis'           ), (SELECT `character_id` FROM `characters` WHERE `name` = 'Tordis'        )),
    (1, 1, (SELECT `character_alias_id` FROM `character_aliases` WHERE `name` = 'Knut Rask'        ), (SELECT `character_id` FROM `characters` WHERE `name` = 'Knut Rask'     )),
    (1, 1, (SELECT `character_alias_id` FROM `character_aliases` WHERE `name` = 'Rask'             ), (SELECT `character_id` FROM `characters` WHERE `name` = 'Knut Rask'     )),
    (1, 1, (SELECT `character_alias_id` FROM `character_aliases` WHERE `name` = 'Arne Aslaksson'   ), (SELECT `character_id` FROM `characters` WHERE `name` = 'Arne Aslaksson')),
    (1, 1, (SELECT `character_alias_id` FROM `character_aliases` WHERE `name` = 'Aslaksson'        ), (SELECT `character_id` FROM `characters` WHERE `name` = 'Arne Aslaksson')),
    (1, 1, (SELECT `character_alias_id` FROM `character_aliases` WHERE `name` = 'bonde 1'          ), (SELECT `character_id` FROM `characters` WHERE `name` = 'bonde 1'       )),
    (1, 1, (SELECT `character_alias_id` FROM `character_aliases` WHERE `name` = 'bonde 2'          ), (SELECT `character_id` FROM `characters` WHERE `name` = 'bonde 2'       )),
    (1, 1, (SELECT `character_alias_id` FROM `character_aliases` WHERE `name` = 'bonde 3'          ), (SELECT `character_id` FROM `characters` WHERE `name` = 'bonde 3'       )),
    (1, 1, (SELECT `character_alias_id` FROM `character_aliases` WHERE `name` = 'bøndene'          ), (SELECT `character_id` FROM `characters` WHERE `name` = 'bonde 1'       )),
    (1, 1, (SELECT `character_alias_id` FROM `character_aliases` WHERE `name` = 'bøndene'          ), (SELECT `character_id` FROM `characters` WHERE `name` = 'bonde 2'       )),
    (1, 1, (SELECT `character_alias_id` FROM `character_aliases` WHERE `name` = 'bøndene'          ), (SELECT `character_id` FROM `characters` WHERE `name` = 'bonde 3'       )),
    (1, 1, (SELECT `character_alias_id` FROM `character_aliases` WHERE `name` = 'bønder'           ), (SELECT `character_id` FROM `characters` WHERE `name` = 'bonde 1'       )),
    (1, 1, (SELECT `character_alias_id` FROM `character_aliases` WHERE `name` = 'bønder'           ), (SELECT `character_id` FROM `characters` WHERE `name` = 'bonde 2'       )),
    (1, 1, (SELECT `character_alias_id` FROM `character_aliases` WHERE `name` = 'bønder'           ), (SELECT `character_id` FROM `characters` WHERE `name` = 'bonde 3'       )),
    (1, 1, (SELECT `character_alias_id` FROM `character_aliases` WHERE `name` = 'knekt 1'          ), (SELECT `character_id` FROM `characters` WHERE `name` = 'knekt 1'       )),
    (1, 1, (SELECT `character_alias_id` FROM `character_aliases` WHERE `name` = 'knekt 2'          ), (SELECT `character_id` FROM `characters` WHERE `name` = 'knekt 2'       )),
    (1, 1, (SELECT `character_alias_id` FROM `character_aliases` WHERE `name` = 'knektene'         ), (SELECT `character_id` FROM `characters` WHERE `name` = 'knekt 1'       )),
    (1, 1, (SELECT `character_alias_id` FROM `character_aliases` WHERE `name` = 'knektene'         ), (SELECT `character_id` FROM `characters` WHERE `name` = 'knekt 2'       )),
    (1, 1, (SELECT `character_alias_id` FROM `character_aliases` WHERE `name` = 'knekter'          ), (SELECT `character_id` FROM `characters` WHERE `name` = 'knekt 1'       )),
    (1, 1, (SELECT `character_alias_id` FROM `character_aliases` WHERE `name` = 'knekter'          ), (SELECT `character_id` FROM `characters` WHERE `name` = 'knekt 2'       )),
    (1, 1, (SELECT `character_alias_id` FROM `character_aliases` WHERE `name` = 'Marit og Jon'     ), (SELECT `character_id` FROM `characters` WHERE `name` = 'Marit'         )),
    (1, 1, (SELECT `character_alias_id` FROM `character_aliases` WHERE `name` = 'Marit og Jon'     ), (SELECT `character_id` FROM `characters` WHERE `name` = 'Jon'           )),
    (1, 1, (SELECT `character_alias_id` FROM `character_aliases` WHERE `name` = 'Sigrunn og bønder'), (SELECT `character_id` FROM `characters` WHERE `name` = 'Sigrunn'       )),
    (1, 1, (SELECT `character_alias_id` FROM `character_aliases` WHERE `name` = 'Sigrunn og bønder'), (SELECT `character_id` FROM `characters` WHERE `name` = 'bonde 1'       )),
    (1, 1, (SELECT `character_alias_id` FROM `character_aliases` WHERE `name` = 'Sigrunn og bønder'), (SELECT `character_id` FROM `characters` WHERE `name` = 'bonde 2'       )),
    (1, 1, (SELECT `character_alias_id` FROM `character_aliases` WHERE `name` = 'Sigrunn og bønder'), (SELECT `character_id` FROM `characters` WHERE `name` = 'bonde 3'       )),
    (1, 1, (SELECT `character_alias_id` FROM `character_aliases` WHERE `name` = 'jente 1'          ), (SELECT `character_id` FROM `characters` WHERE `name` = 'jente 1'       )),
    (1, 1, (SELECT `character_alias_id` FROM `character_aliases` WHERE `name` = 'jente 2'          ), (SELECT `character_id` FROM `characters` WHERE `name` = 'jente 2'       )),
    (1, 1, (SELECT `character_alias_id` FROM `character_aliases` WHERE `name` = 'jente 1 + 2'      ), (SELECT `character_id` FROM `characters` WHERE `name` = 'jente 1'       )),
    (1, 1, (SELECT `character_alias_id` FROM `character_aliases` WHERE `name` = 'jente 1 + 2'      ), (SELECT `character_id` FROM `characters` WHERE `name` = 'jente 2'       )),
    (1, 1, (SELECT `character_alias_id` FROM `character_aliases` WHERE `name` = 'jentene'          ), (SELECT `character_id` FROM `characters` WHERE `name` = 'jente 1'       )),
    (1, 1, (SELECT `character_alias_id` FROM `character_aliases` WHERE `name` = 'jentene'          ), (SELECT `character_id` FROM `characters` WHERE `name` = 'jente 2'       )),
    (1, 1, (SELECT `character_alias_id` FROM `character_aliases` WHERE `name` = 'budbringer'       ), (SELECT `character_id` FROM `characters` WHERE `name` = 'budbringer'    ))
;
