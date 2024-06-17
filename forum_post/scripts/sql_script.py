# -- MySQL Workbench Forward Engineering
#
# SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
# SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
# SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
#
# -- -----------------------------------------------------
# -- Schema mydb
# -- -----------------------------------------------------
# -- -----------------------------------------------------
# -- Schema forum_system
# -- -----------------------------------------------------
#
# -- -----------------------------------------------------
# -- Schema forum_system
# -- -----------------------------------------------------
# CREATE SCHEMA IF NOT EXISTS `forum_system` DEFAULT CHARACTER SET latin1 ;
# USE `forum_system` ;
#
# -- -----------------------------------------------------
# -- Table `forum_system`.`category`
# -- -----------------------------------------------------
# CREATE TABLE IF NOT EXISTS `forum_system`.`category` (
#   `id` INT(11) NOT NULL AUTO_INCREMENT,
#   `name` VARCHAR(45) NOT NULL,
#   `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
#   `is_private` TINYINT(4) NULL DEFAULT NULL,
#   `is_locked` TINYINT(4) NULL DEFAULT NULL,
#   PRIMARY KEY (`id`))
# ENGINE = InnoDB
# DEFAULT CHARACTER SET = latin1;
#
#
# -- -----------------------------------------------------
# -- Table `forum_system`.`user`
# -- -----------------------------------------------------
# CREATE TABLE IF NOT EXISTS `forum_system`.`user` (
#   `id` INT(11) NOT NULL AUTO_INCREMENT,
#   `email` VARCHAR(255) NOT NULL,
#   `username` VARCHAR(45) NOT NULL,
#   `password` VARCHAR(255) NOT NULL,
#   `is_admin` TINYINT(4) NOT NULL,
#   `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
#   PRIMARY KEY (`id`))
# ENGINE = InnoDB
# DEFAULT CHARACTER SET = latin1;
#
#
# -- -----------------------------------------------------
# -- Table `forum_system`.`messages`
# -- -----------------------------------------------------
# CREATE TABLE IF NOT EXISTS `forum_system`.`messages` (
#   `id` INT(11) NOT NULL AUTO_INCREMENT,
#   `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
#   `content` TEXT NULL DEFAULT NULL,
#   `receiver_id` INT(11) NULL DEFAULT NULL,
#   `sender_id` INT(11) NULL DEFAULT NULL,
#   PRIMARY KEY (`id`),
#   INDEX `receiver_id` (`receiver_id` ASC) VISIBLE,
#   INDEX `sender_id` (`sender_id` ASC) VISIBLE,
#   CONSTRAINT `messages_ibfk_1`
#     FOREIGN KEY (`receiver_id`)
#     REFERENCES `forum_system`.`user` (`id`)
#     ON DELETE NO ACTION
#     ON UPDATE NO ACTION,
#   CONSTRAINT `messages_ibfk_2`
#     FOREIGN KEY (`sender_id`)
#     REFERENCES `forum_system`.`user` (`id`)
#     ON DELETE NO ACTION
#     ON UPDATE NO ACTION)
# ENGINE = InnoDB
# DEFAULT CHARACTER SET = latin1;
#
#
# -- -----------------------------------------------------
# -- Table `forum_system`.`topic`
# -- -----------------------------------------------------
# CREATE TABLE IF NOT EXISTS `forum_system`.`topic` (
#   `id` INT(11) NOT NULL AUTO_INCREMENT,
#   `topic_name` VARCHAR(45) NOT NULL,
#   `category_id` INT(11) NOT NULL,
#   `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
#   `user_id` INT(11) NOT NULL,
#   `best_reply_id` INT(11) NULL DEFAULT NULL,
#   `is_locked` TINYINT(4) NULL DEFAULT NULL,
#   PRIMARY KEY (`id`),
#   INDEX `category_id` (`category_id` ASC) VISIBLE,
#   INDEX `user_id` (`user_id` ASC) VISIBLE,
#   CONSTRAINT `topic_ibfk_1`
#     FOREIGN KEY (`category_id`)
#     REFERENCES `forum_system`.`category` (`id`)
#     ON DELETE NO ACTION
#     ON UPDATE NO ACTION,
#   CONSTRAINT `topic_ibfk_2`
#     FOREIGN KEY (`user_id`)
#     REFERENCES `forum_system`.`user` (`id`)
#     ON DELETE NO ACTION
#     ON UPDATE NO ACTION)
# ENGINE = InnoDB
# DEFAULT CHARACTER SET = latin1;
#
#
# -- -----------------------------------------------------
# -- Table `forum_system`.`reply`
# -- -----------------------------------------------------
# CREATE TABLE IF NOT EXISTS `forum_system`.`reply` (
#   `id` INT(11) NOT NULL AUTO_INCREMENT,
#   `content` TEXT NULL DEFAULT NULL,
#   `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
#   `topic_id` INT(11) NOT NULL,
#   `topic_id1` INT(11) NOT NULL,
#   PRIMARY KEY (`id`),
#   INDEX `topic_id` (`topic_id` ASC) VISIBLE,
#   INDEX `fk_reply_topic1_idx` (`topic_id1` ASC) VISIBLE,
#   CONSTRAINT `reply_ibfk_2`
#     FOREIGN KEY (`topic_id`)
#     REFERENCES `forum_system`.`topic` (`id`)
#     ON DELETE NO ACTION
#     ON UPDATE NO ACTION,
#   CONSTRAINT `fk_reply_topic1`
#     FOREIGN KEY (`topic_id1`)
#     REFERENCES `forum_system`.`topic` (`id`)
#     ON DELETE NO ACTION
#     ON UPDATE NO ACTION)
# ENGINE = InnoDB
# DEFAULT CHARACTER SET = latin1;
#
#
# -- -----------------------------------------------------
# -- Table `forum_system`.`category_has_user`
# -- -----------------------------------------------------
# CREATE TABLE IF NOT EXISTS `forum_system`.`category_has_user` (
#   `category_id` INT(11) NOT NULL,
#   `user_id` INT(11) NOT NULL,
#   `access_type` ENUM("read access", "write access", "banned") NULL,
#   PRIMARY KEY (`category_id`, `user_id`),
#   INDEX `fk_category_has_user_user1_idx` (`user_id` ASC) VISIBLE,
#   INDEX `fk_category_has_user_category1_idx` (`category_id` ASC) VISIBLE,
#   CONSTRAINT `fk_category_has_user_category1`
#     FOREIGN KEY (`category_id`)
#     REFERENCES `forum_system`.`category` (`id`)
#     ON DELETE NO ACTION
#     ON UPDATE NO ACTION,
#   CONSTRAINT `fk_category_has_user_user1`
#     FOREIGN KEY (`user_id`)
#     REFERENCES `forum_system`.`user` (`id`)
#     ON DELETE NO ACTION
#     ON UPDATE NO ACTION)
# ENGINE = InnoDB
# DEFAULT CHARACTER SET = latin1;
#
#
# -- -----------------------------------------------------
# -- Table `forum_system`.`votes`
# -- -----------------------------------------------------
# CREATE TABLE IF NOT EXISTS `forum_system`.`votes` (
#   `reply_id` INT(11) NOT NULL,
#   `user_id` INT(11) NOT NULL,
#   `status` ENUM("upvote", "downvote") NULL,
#   PRIMARY KEY (`reply_id`, `user_id`),
#   INDEX `fk_reply_has_user_user1_idx` (`user_id` ASC) VISIBLE,
#   INDEX `fk_reply_has_user_reply1_idx` (`reply_id` ASC) VISIBLE,
#   CONSTRAINT `fk_reply_has_user_reply1`
#     FOREIGN KEY (`reply_id`)
#     REFERENCES `forum_system`.`reply` (`id`)
#     ON DELETE NO ACTION
#     ON UPDATE NO ACTION,
#   CONSTRAINT `fk_reply_has_user_user1`
#     FOREIGN KEY (`user_id`)
#     REFERENCES `forum_system`.`user` (`id`)
#     ON DELETE NO ACTION
#     ON UPDATE NO ACTION)
# ENGINE = InnoDB
# DEFAULT CHARACTER SET = latin1;
#
#
# SET SQL_MODE=@OLD_SQL_MODE;
# SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
# SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
#
# !!!! NEW SCRIPT !!!!
#
# -- MySQL Workbench Forward Engineering
#
# SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
# SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
# SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
#
# -- -----------------------------------------------------
# -- Schema mydb
# -- -----------------------------------------------------
# -- -----------------------------------------------------
# -- Schema forum_system_schema
# -- -----------------------------------------------------
#
# -- -----------------------------------------------------
# -- Schema forum_system_schema
# -- -----------------------------------------------------
# CREATE SCHEMA IF NOT EXISTS `forum_system_schema` DEFAULT CHARACTER SET latin1 ;
# USE `forum_system_schema` ;
#
# -- -----------------------------------------------------
# -- Table `forum_system_schema`.`category`
# -- -----------------------------------------------------
# CREATE TABLE IF NOT EXISTS `forum_system_schema`.`category` (
#   `id` INT(11) NOT NULL AUTO_INCREMENT,
#   `name` VARCHAR(45) NOT NULL,
#   `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
#   `is_private` TINYINT(4) NULL DEFAULT NULL,
#   `is_locked` TINYINT(4) NULL DEFAULT NULL,
#   PRIMARY KEY (`id`))
# ENGINE = InnoDB
# AUTO_INCREMENT = 11
# DEFAULT CHARACTER SET = latin1;
#
#
# -- -----------------------------------------------------
# -- Table `forum_system_schema`.`user`
# -- -----------------------------------------------------
# CREATE TABLE IF NOT EXISTS `forum_system_schema`.`user` (
#   `id` INT(11) NOT NULL AUTO_INCREMENT,
#   `email` VARCHAR(255) NOT NULL,
#   `username` VARCHAR(45) NOT NULL,
#   `password` VARCHAR(255) NOT NULL,
#   `is_admin` TINYINT(4) NOT NULL DEFAULT 0,
#   `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
#   PRIMARY KEY (`id`),
#   UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE,
#   UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE)
# ENGINE = InnoDB
# AUTO_INCREMENT = 51
# DEFAULT CHARACTER SET = latin1;
#
#
# -- -----------------------------------------------------
# -- Table `forum_system_schema`.`category_has_user`
# -- -----------------------------------------------------
# CREATE TABLE IF NOT EXISTS `forum_system_schema`.`category_has_user` (
#   `category_id` INT(11) NOT NULL,
#   `user_id` INT(11) NOT NULL,
#   `access_type` ENUM('read access', 'read and write access', 'banned') NULL DEFAULT 'read and write access',
#   PRIMARY KEY (`category_id`, `user_id`),
#   INDEX `fk_category_has_user_user1_idx` (`user_id` ASC) VISIBLE,
#   INDEX `fk_category_has_user_category1_idx` (`category_id` ASC) VISIBLE,
#   CONSTRAINT `fk_category_has_user_category1`
#     FOREIGN KEY (`category_id`)
#     REFERENCES `forum_system_schema`.`category` (`id`)
#     ON DELETE NO ACTION
#     ON UPDATE NO ACTION,
#   CONSTRAINT `fk_category_has_user_user1`
#     FOREIGN KEY (`user_id`)
#     REFERENCES `forum_system_schema`.`user` (`id`)
#     ON DELETE NO ACTION
#     ON UPDATE NO ACTION)
# ENGINE = InnoDB
# DEFAULT CHARACTER SET = latin1;
#
#
# -- -----------------------------------------------------
# -- Table `forum_system_schema`.`messages`
# -- -----------------------------------------------------
# CREATE TABLE IF NOT EXISTS `forum_system_schema`.`messages` (
#   `id` INT(11) NOT NULL AUTO_INCREMENT,
#   `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
#   `content` TEXT NULL DEFAULT NULL,
#   `receiver_id` INT(11) NULL DEFAULT NULL,
#   `sender_id` INT(11) NULL DEFAULT NULL,
#   PRIMARY KEY (`id`),
#   INDEX `receiver_id` (`receiver_id` ASC) VISIBLE,
#   INDEX `sender_id` (`sender_id` ASC) VISIBLE,
#   CONSTRAINT `messages_ibfk_1`
#     FOREIGN KEY (`receiver_id`)
#     REFERENCES `forum_system_schema`.`user` (`id`)
#     ON DELETE NO ACTION
#     ON UPDATE NO ACTION,
#   CONSTRAINT `messages_ibfk_2`
#     FOREIGN KEY (`sender_id`)
#     REFERENCES `forum_system_schema`.`user` (`id`)
#     ON DELETE NO ACTION
#     ON UPDATE NO ACTION)
# ENGINE = InnoDB
# AUTO_INCREMENT = 14
# DEFAULT CHARACTER SET = latin1;
#
#
# -- -----------------------------------------------------
# -- Table `forum_system_schema`.`topic`
# -- -----------------------------------------------------
# CREATE TABLE IF NOT EXISTS `forum_system_schema`.`topic` (
#   `id` INT(11) NOT NULL AUTO_INCREMENT,
#   `topic_name` VARCHAR(45) NOT NULL,
#   `category_id` INT(11) NOT NULL,
#   `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
#   `user_id` INT(11) NOT NULL,
#   `best_reply_id` INT(11) NULL DEFAULT NULL,
#   `is_locked` TINYINT(4) NULL DEFAULT NULL,
#   PRIMARY KEY (`id`),
#   INDEX `category_id` (`category_id` ASC) VISIBLE,
#   INDEX `user_id` (`user_id` ASC) VISIBLE,
#   CONSTRAINT `topic_ibfk_1`
#     FOREIGN KEY (`category_id`)
#     REFERENCES `forum_system_schema`.`category` (`id`)
#     ON DELETE NO ACTION
#     ON UPDATE NO ACTION,
#   CONSTRAINT `topic_ibfk_2`
#     FOREIGN KEY (`user_id`)
#     REFERENCES `forum_system_schema`.`user` (`id`)
#     ON DELETE NO ACTION
#     ON UPDATE NO ACTION)
# ENGINE = InnoDB
# AUTO_INCREMENT = 4
# DEFAULT CHARACTER SET = latin1;
#
#
# -- -----------------------------------------------------
# -- Table `forum_system_schema`.`reply`
# -- -----------------------------------------------------
# CREATE TABLE IF NOT EXISTS `forum_system_schema`.`reply` (
#   `id` INT(11) NOT NULL AUTO_INCREMENT,
#   `content` TEXT NULL DEFAULT NULL,
#   `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
#   `topic_id` INT(11) NOT NULL,
#   PRIMARY KEY (`id`),
#   INDEX `topic_id` (`topic_id` ASC) VISIBLE,
#   CONSTRAINT `reply_ibfk_2`
#     FOREIGN KEY (`topic_id`)
#     REFERENCES `forum_system_schema`.`topic` (`id`)
#     ON DELETE NO ACTION
#     ON UPDATE NO ACTION)
# ENGINE = InnoDB
# AUTO_INCREMENT = 3
# DEFAULT CHARACTER SET = latin1;
#
#
# -- -----------------------------------------------------
# -- Table `forum_system_schema`.`votes`
# -- -----------------------------------------------------
# CREATE TABLE IF NOT EXISTS `forum_system_schema`.`votes` (
#   `reply_id` INT(11) NOT NULL,
#   `user_id` INT(11) NOT NULL,
#   `status` ENUM('upvote', 'downvote') NULL DEFAULT NULL,
#   PRIMARY KEY (`reply_id`, `user_id`),
#   INDEX `fk_reply_has_user_user1_idx` (`user_id` ASC) VISIBLE,
#   INDEX `fk_reply_has_user_reply1_idx` (`reply_id` ASC) VISIBLE,
#   CONSTRAINT `fk_reply_has_user_reply1`
#     FOREIGN KEY (`reply_id`)
#     REFERENCES `forum_system_schema`.`reply` (`id`)
#     ON DELETE NO ACTION
#     ON UPDATE NO ACTION,
#   CONSTRAINT `fk_reply_has_user_user1`
#     FOREIGN KEY (`user_id`)
#     REFERENCES `forum_system_schema`.`user` (`id`)
#     ON DELETE NO ACTION
#     ON UPDATE NO ACTION)
# ENGINE = InnoDB
# DEFAULT CHARACTER SET = latin1;
#
#
# SET SQL_MODE=@OLD_SQL_MODE;
# SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
# SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
#
