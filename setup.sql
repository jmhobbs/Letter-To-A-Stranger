CREATE TABLE `users` (
	`id` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
	`joined` DATETIME  NOT NULL,
	`email` VARCHAR(255)  NOT NULL,
	`letters_sent` INTEGER UNSIGNED NOT NULL DEFAULT 0,
	`replys_completed` INTEGER UNSIGNED NOT NULL DEFAULT 0,
	`replys_dropped` INTEGER UNSIGNED NOT NULL DEFAULT 0,
	`status` ENUM( 'CONFIRMED', 'DORMANT', 'BAD_ADDRESS' ),
	PRIMARY KEY (`id`),
	UNIQUE INDEX `unique_emails`(`email`)
) ENGINE = MyISAM;

'''
Letters are always bound to chains. Chains are just a way of linking meta data about messages and replys.
'''
CREATE TABLE `letter_chains` (
	`id` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
	`slug` VARCHAR(40) NOT NULL,
	`origin_id` INTEGER UNSIGNED NOT NULL,
	`replier_id` INTEGER UNSIGNED DEFAULT NULL,
	`started` DATETIME NOT NULL,
	`linked` DA
	PRIMARY KEY (`id`),
	UNIQUE INDEX `unique_slugs`(`slug`)
) ENGINE = MyISAM;

CREATE TABLE `letters` (

) ENGINE = MyISAM;


'''
This is a table to track when un-linked chains are sent out to users
as well as wether they complete them or drop them.
'''
CREATE TABLE `attempted_links` (
	`letter_id` INTEGER UNSIGNED NOT NULL,
	`user_id` INTEGER UNSIGNED NOT NULL,
	`link_sent` DATETIME NOT NULL,
	`link_expires` DATETIME NOT NULL,
	`link_result` ENUM( 'PENDING', 'LINKED', 'DROPPED', 'FAILED', 'VULGARED', 'SPAMMED' ),
	`result_time` DATETIME DEFAULT NULL,
	PRIMARY KEY (`letter_id`, `user_id` ),
	INDEX `expires_search` ( `link_expires`, `link_result` )
) ENGINE = MyISAM;

'''
A single letter sent to or from a stranger.
We store the text of emails in two places, file names driven by the file hash of the FULL email.
  1. Original, full text of the email (with headers) is stored in mail/full/[hash path]
	2. Parsed, clean text of the email (that we send out) is stored in mail/clean/[hash path]
'''
CREATE TABLE `letters` (
	`id` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
	`letter_chain_id` INTEGER UNSIGNED NOT NULL,
	`user_id` INTEGER UNSIGNED NOT NULL,
	`hash` VARCHAR(40) NOT NULL,
	`recieved` DATETIME NOT NULL,
	PRIMARY KEY ( `id` ),
	INDEX `chain_index` ( `letter_chain_id` ),
	INDEX `user_index` ( `user_id` )
) ENGINE = MyISAM;

'''
This table documents all outbound stranger mail.
'''
CREATE TABLE `letter_sends` (
	`id` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
	`letter_id` INTEGER UNSIGNED NOT NULL,
	`user_id` INTEGER UNSIGNED NOT NULL,
	`sent` DATETIME NOT NULL,
	`failure` ENUM( 'NONE', 'BAD_ADDRESS' ),
	`failure_time` DATETIME DEFAULT NULL,
	PRIMARY KEY ( `id` )
) ENGINE = MyISAM;
