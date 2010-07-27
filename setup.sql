DROP TABLE IF EXISTS `users`;
DROP TABLE IF EXISTS `registrations`;
DROP TABLE IF EXISTS `quits`;
DROP TABLE IF EXISTS `letter_chains`;
DROP TABLE IF EXISTS `attempted_links`;
DROP TABLE IF EXISTS `letters`;
DROP TABLE IF EXISTS `letter_sends`;
DROP TABLE IF EXISTS `vulgar_logs`;
DROP TABLE IF EXISTS `spam_logs`;

/*
	A user is a user is a user.
*/
CREATE TABLE `users` (
	`id` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
	`joined` DATETIME  NOT NULL COMMENT 'Date of registration.',
	`email` VARCHAR(255)  NOT NULL COMMENT 'Canonical e-mail address. All lowercased.',
	`letters_sent` INTEGER UNSIGNED NOT NULL DEFAULT 0 COMMENT 'Just a counter of total letters initiated.',
	`replys_completed` INTEGER UNSIGNED NOT NULL DEFAULT 0 COMMENT 'A counter of chains completed.',
	`replys_dropped` INTEGER UNSIGNED NOT NULL DEFAULT 0 COMMENT 'A counter of chains dropped.',
	`status` ENUM( 'PENDING', 'CONFIRMED', 'DORMANT', 'BAD_ADDRESS' ) COMMENT 'Their current registration status.',
	`spam_threshold` INTEGER NOT NULL DEFAULT 25 COMMENT 'Their taste for spam.',
	`vulgarity_threshold` INTEGER NOT NULL DEFAULT 25 COMMENT 'Their taste for vulgarity.',
	PRIMARY KEY (`id`),
	UNIQUE INDEX `unique_emails`(`email`)
);

/*
	When a user is registered, they are stored here.
*/
CREATE TABLE `registrations` (
	`id` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
	`user_id` INTEGER UNSIGNED NOT NULL,
	`recieved` DATETIME NOT NULL,
	`hash` VARCHAR(40) NOT NULL,
	PRIMARY KEY ( `id` )
);

/*
	When a user quits, that is stored here.
*/
CREATE TABLE `quits` (
	`id` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
	`user_id` INTEGER UNSIGNED NOT NULL,
	`recieved` DATETIME NOT NULL,
	`hash` VARCHAR(40) NOT NULL,
	PRIMARY KEY ( `id` )
);

/*
	Letters are always bound to chains. Chains are just a way of linking meta data about messages and replys.
*/
CREATE TABLE `letter_chains` (
	`id` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
	`slug` VARCHAR(40) NOT NULL COMMENT 'A unique slug for each email chain. A sha1 hash.',
	`origin_id` INTEGER UNSIGNED NOT NULL COMMENT 'The users.id of the chain initator.',
	`replier_id` INTEGER UNSIGNED DEFAULT NULL COMMENT 'The users.id of the chain replier.',
	`started` DATETIME NOT NULL COMMENT 'When the chain was initiated.',
	`linked` DATETIME DEFAULT NULL COMMENT 'When the chain was linked.',
	`drop_count` INTEGER UNSIGNED NOT NULL DEFAULT 0 COMMENT 'How many times this chain has been dropped.',
	`state` ENUM( 'PENDING', 'LINKED', 'FAILED', 'SPAM' ) COMMENT 'The state of this chain.',
	PRIMARY KEY (`id`),
	UNIQUE INDEX `unique_slugs`(`slug`)
);

/*
	This is a table to track when un-linked chains are sent out to users
	as well as wether they complete them or drop them.
*/
CREATE TABLE `attempted_links` (
	`letter_chain_id` INTEGER UNSIGNED NOT NULL COMMENT 'The ID of the chain we try to link.',
	`user_id` INTEGER UNSIGNED NOT NULL COMMENT 'The users.id of the user we are trying to link with.',
	`link_sent` DATETIME NOT NULL COMMENT 'When the link was sent.',
	`link_expires` DATETIME NOT NULL COMMENT 'When the link will expire.',
	`link_result` ENUM( 'PENDING', 'LINKED', 'DROPPED', 'FAILED', 'VULGARED', 'SPAMMED' ) COMMENT 'The end result of the link attempt.',
	`result_time` DATETIME DEFAULT NULL COMMENT 'When the result occurred.',
	PRIMARY KEY (`letter_chain_id`, `user_id` ),
	INDEX `expires_search` ( `link_expires`, `link_result` )
);

/*
	A single letter sent to or from a stranger.
	We store the text of emails in two places, file names driven by the file hash of the FULL email.
		1. Original, full text of the email (with headers) is stored in mail/full/[hash path]
		2. Parsed, clean text of the email (that we send out) is stored in mail/clean/[hash path]
*/
CREATE TABLE `letters` (
	`id` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
	`letter_chain_id` INTEGER UNSIGNED NOT NULL COMMENT 'The chain this letter belongs to.',
	`user_id` INTEGER UNSIGNED NOT NULL COMMENT 'Who sent this letter.',
	`hash` VARCHAR(40) NOT NULL COMMENT 'The hash of this letter. Determines file storage.',
	`recieved` DATETIME NOT NULL COMMENT 'When the letter was recieved. For sorting.',
	`spam_weight` INTEGER NOT NULL DEFAULT 0 COMMENT 'The likeliness that this letter is spam.',
	`vulgarity_weight` INTEGER NOT NULL DEFAULT 0 COMMENT 'The amount of vulgarity in this letter.',
	PRIMARY KEY ( `id` ),
	INDEX `chain_index` ( `letter_chain_id` ),
	INDEX `user_index` ( `user_id` )
);

/*
	This table documents all outbound stranger mail.
*/
CREATE TABLE `letter_sends` (
	`id` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
	`letter_id` INTEGER UNSIGNED NOT NULL COMMENT 'The ID of the letter.',
	`sender_id` INTEGER UNSIGNED NOT NULL COMMENT 'Who sent the letter.',
	`recipient_id` INTEGER UNSIGNED NOT NULL COMMENT 'Who recieved the letter.',
	`sent` DATETIME NOT NULL COMMENT 'The time it was sent.',
	`failure` ENUM( 'NONE', 'BAD_ADDRESS' ) COMMENT 'If it fails, how does it fail?',
	`failure_time` DATETIME DEFAULT NULL COMMENT 'The time it fails, if at all.',
	PRIMARY KEY ( `id` )
);

/*
	This logs all mail counted as too vulgar by users
*/
CREATE TABLE `vulgar_logs` (
	`id` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
	`letter_id` INTEGER UNSIGNED NOT NULL COMMENT 'The letter id.',
	`marker_id` INTEGER UNSIGNED NOT NULL COMMENT 'The users.id that marked it as vulgar.',
	`marked_at` DATETIME NOT NULL COMMENT 'When it was marked.',
	PRIMARY KEY ( `id` ),
	INDEX ( `letter_id` )
);

/*
	This logs all mail counted as spam by users.
*/
CREATE TABLE `spam_logs` (
	`id` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
	`letter_id` INTEGER UNSIGNED NOT NULL COMMENT 'The letter id.',
	`marker_id` INTEGER UNSIGNED NOT NULL COMMENT 'The users.id that marked it as spam.',
	`marked_at` DATETIME NOT NULL COMMENT 'When it was marked.',
	PRIMARY KEY ( `id` ),
	INDEX ( `letter_id` )
);