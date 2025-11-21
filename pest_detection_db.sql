/*
 Navicat MySQL Data Transfer

 Source Server         : Localhost
 Source Server Type    : MySQL
 Source Server Version : 8.0.0
 Source Host           : localhost:3306
 Source Schema         : pest_detection_db

 Target Server Type    : MySQL
 Target Server Version : 8.0.0
 File Encoding         : 65001

 Date: 20/11/2025
*/

CREATE DATABASE IF NOT EXISTS `pest_detection_db`;
USE `pest_detection_db`;

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `hashed_password` varchar(255) NOT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `is_admin` tinyint(1) DEFAULT '0',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_users_username` (`username`),
  UNIQUE KEY `ix_users_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for pest_info
-- ----------------------------
DROP TABLE IF EXISTS `pest_info`;
CREATE TABLE `pest_info` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` text,
  `control_methods` text,
  `image_url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_pest_info_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for detections
-- ----------------------------
DROP TABLE IF EXISTS `detections`;
CREATE TABLE `detections` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `image_path` varchar(255) DEFAULT NULL,
  `video_path` varchar(255) DEFAULT NULL,
  `result_json` json DEFAULT NULL,
  `detection_type` varchar(20) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `detections_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for posts
-- ----------------------------
DROP TABLE IF EXISTS `posts`;
CREATE TABLE `posts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `content` text NOT NULL,
  `user_id` int DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `posts_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for comments
-- ----------------------------
DROP TABLE IF EXISTS `comments`;
CREATE TABLE `comments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `content` text NOT NULL,
  `post_id` int DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `post_id` (`post_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `posts` (`id`),
  CONSTRAINT `comments_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for likes
-- ----------------------------
DROP TABLE IF EXISTS `likes`;
CREATE TABLE `likes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `post_id` int DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `post_id` (`post_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `likes_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `posts` (`id`),
  CONSTRAINT `likes_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of pest_info
-- ----------------------------
INSERT INTO `pest_info` (`name`, `description`, `control_methods`, `image_url`) VALUES 
('Ants', 'Ants are eusocial insects of the family Formicidae.', 'Use ant baits, keep areas clean, seal entry points.', NULL),
('Bees', 'Bees are flying insects closely related to wasps and ants.', 'Relocation by professionals if necessary. Generally beneficial.', NULL),
('Beetles', 'Beetles are a group of insects that form the order Coleoptera.', 'Identify species first. Use insecticides or traps.', NULL),
('Caterpillars', 'Caterpillars are the larval stage of members of the order Lepidoptera.', 'Hand picking, Bacillus thuringiensis (Bt), neem oil.', NULL),
('Earthworms', 'An earthworm is a tube-shaped, segmented worm found in the phylum Annelida.', 'Beneficial for soil. No control usually needed.', NULL),
('Earwigs', 'Earwigs make up the insect order Dermaptera.', 'Traps (rolled newspaper), diatomaceous earth.', NULL),
('Grasshoppers', 'Grasshoppers are a group of insects belonging to the suborder Caelifera.', 'Nolo Bait, neem oil, floating row covers.', NULL),
('Moths', 'Moths are a paraphyletic group of insects that includes all members of the order Lepidoptera that are not butterflies.', 'Pheromone traps, light traps, proper storage of clothes/food.', NULL),
('Slugs', 'Slug is a common name for an apparently shell-less terrestrial gastropod mollusc.', 'Iron phosphate bait, copper tape, beer traps.', NULL),
('Snails', 'A snail is, in loose terms, a shelled gastropod.', 'Hand picking, copper barriers, slug/snail bait.', NULL),
('Wasps', 'A wasp is any insect of the narrow-waisted suborder Apocrita of the order Hymenoptera.', 'Wasp sprays, hanging traps. Professional removal for nests.', NULL),
('Weevils', 'Weevils are a type of beetle from the superfamily Curculionoidea.', 'Discard infested food, clean shelves, freeze grains.', NULL);

-- ----------------------------
-- Table structure for verification_codes
-- ----------------------------
DROP TABLE IF EXISTS `verification_codes`;
CREATE TABLE `verification_codes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(100) NOT NULL,
  `code` varchar(10) NOT NULL,
  `expires_at` datetime NOT NULL,
  `used` tinyint(1) DEFAULT '0',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `ix_verification_codes_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

SET FOREIGN_KEY_CHECKS = 1;

