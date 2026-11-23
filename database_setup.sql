-- Smart Plant Monitor database (MySQL).
-- The app also makes these tables itself when it starts, so this file is
-- only needed to set the database up by hand.

CREATE DATABASE IF NOT EXISTS plantmonitor CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE plantmonitor;

CREATE TABLE IF NOT EXISTS `reading` (
    `readingID` INT NOT NULL AUTO_INCREMENT,
    `moisture` INT NOT NULL,
    `simulated` BOOLEAN NOT NULL DEFAULT TRUE,
    `recordedAt` DATETIME NOT NULL,
    PRIMARY KEY (`readingID`),
    INDEX `ix_reading_recordedAt` (`recordedAt`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `setting` (
    `settingID` INT NOT NULL,
    `dryThreshold` INT NOT NULL DEFAULT 30,
    `wetThreshold` INT NOT NULL DEFAULT 70,
    PRIMARY KEY (`settingID`)
) ENGINE=InnoDB;

-- The one settings row
INSERT IGNORE INTO `setting` (`settingID`, `dryThreshold`, `wetThreshold`) VALUES (1, 30, 70);
