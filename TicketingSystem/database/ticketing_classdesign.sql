/*
 Navicat Premium Data Transfer

 Source Server         : phpstudy_mysql8.0
 Source Server Type    : MySQL
 Source Server Version : 80012
 Source Host           : localhost:3307
 Source Schema         : ticketing_classdesign

 Target Server Type    : MySQL
 Target Server Version : 80012
 File Encoding         : 65001

 Date: 29/12/2024 11:00:55
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for bookings
-- ----------------------------
DROP TABLE IF EXISTS `bookings`;
CREATE TABLE `bookings`  (
  `id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `ticket_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `scenery_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `start_time` datetime(0) DEFAULT NULL,
  `end_time` datetime(0) DEFAULT NULL,
  `state` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `amount` double(255, 2) DEFAULT 0.00,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_id_bookings`(`user_id`) USING BTREE,
  INDEX `ticket_id`(`ticket_id`) USING BTREE,
  INDEX `scenery_id`(`scenery_id`) USING BTREE,
  CONSTRAINT `scenery_id` FOREIGN KEY (`scenery_id`) REFERENCES `sceneries` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `ticket_id` FOREIGN KEY (`ticket_id`) REFERENCES `tickets` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `user_id_bookings` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of bookings
-- ----------------------------
INSERT INTO `bookings` VALUES ('1', '1', '3', '3', '2024-12-07 20:33:56', '2024-12-07 21:34:08', '已支付', 50.00);
INSERT INTO `bookings` VALUES ('2', '2', '5', '1', '2024-12-02 22:01:18', '2024-12-02 23:01:27', '未支付', 108.00);
INSERT INTO `bookings` VALUES ('3', '3', '3', '2', '2024-12-04 22:41:33', '2024-12-04 22:41:39', '已支付', 59.50);

-- ----------------------------
-- Table structure for list_person
-- ----------------------------
DROP TABLE IF EXISTS `list_person`;
CREATE TABLE `list_person`  (
  `booking_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `person_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`booking_id`, `person_id`) USING BTREE,
  INDEX `person_id_list_person`(`person_id`) USING BTREE,
  CONSTRAINT `booking_id_list_person` FOREIGN KEY (`booking_id`) REFERENCES `bookings` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `person_id_list_person` FOREIGN KEY (`person_id`) REFERENCES `person` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of list_person
-- ----------------------------
INSERT INTO `list_person` VALUES ('1', '1');
INSERT INTO `list_person` VALUES ('2', '4');
INSERT INTO `list_person` VALUES ('2', '5');
INSERT INTO `list_person` VALUES ('2', '6');

-- ----------------------------
-- Table structure for list_ticket
-- ----------------------------
DROP TABLE IF EXISTS `list_ticket`;
CREATE TABLE `list_ticket`  (
  `scenery_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `ticket_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`scenery_id`, `ticket_id`) USING BTREE,
  INDEX `ticket_id_list_ticket`(`ticket_id`) USING BTREE,
  CONSTRAINT `scenery_id_list_ticket` FOREIGN KEY (`scenery_id`) REFERENCES `sceneries` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `ticket_id_list_ticket` FOREIGN KEY (`ticket_id`) REFERENCES `tickets` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of list_ticket
-- ----------------------------
INSERT INTO `list_ticket` VALUES ('1', '1');
INSERT INTO `list_ticket` VALUES ('2', '2');
INSERT INTO `list_ticket` VALUES ('2', '3');
INSERT INTO `list_ticket` VALUES ('1', '4');
INSERT INTO `list_ticket` VALUES ('2', '4');
INSERT INTO `list_ticket` VALUES ('1', '5');
INSERT INTO `list_ticket` VALUES ('3', '6');

-- ----------------------------
-- Table structure for loads
-- ----------------------------
DROP TABLE IF EXISTS `loads`;
CREATE TABLE `loads`  (
  `scenery_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `date` date NOT NULL,
  `sold` int(128) DEFAULT NULL,
  `max` int(128) DEFAULT NULL,
  PRIMARY KEY (`scenery_id`, `date`) USING BTREE,
  CONSTRAINT `scenery_id_loads` FOREIGN KEY (`scenery_id`) REFERENCES `sceneries` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of loads
-- ----------------------------
INSERT INTO `loads` VALUES ('3', '2024-12-01', 100, 500);
INSERT INTO `loads` VALUES ('3', '2024-12-02', 200, 400);

-- ----------------------------
-- Table structure for pays
-- ----------------------------
DROP TABLE IF EXISTS `pays`;
CREATE TABLE `pays`  (
  `id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `amount` double(255, 2) DEFAULT NULL,
  `way` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `state` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `start_time` datetime(0) DEFAULT NULL,
  `end_time` datetime(0) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of pays
-- ----------------------------
INSERT INTO `pays` VALUES ('1', 50.00, '微信支付', '已支付', '2024-12-07 20:33:56', '2024-12-07 21:34:08');
INSERT INTO `pays` VALUES ('2', 108.00, '微信支付', '未支付', '2024-12-02 22:04:42', '2024-12-02 23:03:45');
INSERT INTO `pays` VALUES ('3', 59.50, '微信支付', '已支付', '2024-12-04 22:41:33', '2024-12-04 22:41:39');

-- ----------------------------
-- Table structure for person
-- ----------------------------
DROP TABLE IF EXISTS `person`;
CREATE TABLE `person`  (
  `id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `phone` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `age` int(16) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_id_person`(`user_id`) USING BTREE,
  CONSTRAINT `user_id_person` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of person
-- ----------------------------
INSERT INTO `person` VALUES ('1', '1', '齐浩龙', '13864317069', 21);
INSERT INTO `person` VALUES ('10', '3', '美对象', '12000000000', 20);
INSERT INTO `person` VALUES ('2', '1', '齐爸', '15900000000', NULL);
INSERT INTO `person` VALUES ('3', '1', '齐妈', '1500000000', NULL);
INSERT INTO `person` VALUES ('4', '2', '刘孝宙', '15653303083', 20);
INSERT INTO `person` VALUES ('5', '2', '刘爸', '15600000000', NULL);
INSERT INTO `person` VALUES ('6', '2', '刘妈', '15600000000', NULL);
INSERT INTO `person` VALUES ('7', '3', '小美', '12000000000', 20);
INSERT INTO `person` VALUES ('8', '3', '美爸', '12000000000', NULL);
INSERT INTO `person` VALUES ('9', '3', '美妈', '12000000000', NULL);

-- ----------------------------
-- Table structure for rebates
-- ----------------------------
DROP TABLE IF EXISTS `rebates`;
CREATE TABLE `rebates`  (
  `id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `start_time` datetime(0) DEFAULT NULL,
  `end_time` datetime(0) DEFAULT NULL,
  `state` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of rebates
-- ----------------------------
INSERT INTO `rebates` VALUES ('1', '2024-12-02 22:03:56', '2024-12-03 23:02:59', '已通过');

-- ----------------------------
-- Table structure for relation_booking
-- ----------------------------
DROP TABLE IF EXISTS `relation_booking`;
CREATE TABLE `relation_booking`  (
  `booking_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `pay_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `rebate_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`booking_id`, `pay_id`) USING BTREE,
  INDEX `pay_id_relation`(`pay_id`) USING BTREE,
  INDEX `rebate_id_relation`(`rebate_id`) USING BTREE,
  CONSTRAINT `booking_id_relation` FOREIGN KEY (`booking_id`) REFERENCES `bookings` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `pay_id_relation` FOREIGN KEY (`pay_id`) REFERENCES `pays` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `rebate_id_relation` FOREIGN KEY (`rebate_id`) REFERENCES `rebates` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of relation_booking
-- ----------------------------
INSERT INTO `relation_booking` VALUES ('1', '1', NULL);
INSERT INTO `relation_booking` VALUES ('3', '3', NULL);
INSERT INTO `relation_booking` VALUES ('2', '2', '1');

-- ----------------------------
-- Table structure for sceneries
-- ----------------------------
DROP TABLE IF EXISTS `sceneries`;
CREATE TABLE `sceneries`  (
  `id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `text` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `img` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sceneries
-- ----------------------------
INSERT INTO `sceneries` VALUES ('1', '泰山', '好高', '2024-12-01', '2024-12-31', 'c2625c26-2094-44ed-bbef-2782f0677a38.jpg');
INSERT INTO `sceneries` VALUES ('2', '张家界', '好看', '2024-11-01', '2024-11-30', '31edf237-f6b7-42b2-b595-3af152c4993d.jpg');
INSERT INTO `sceneries` VALUES ('3', '长城', '好爬', '2024-10-01', '2024-10-31', '73ba6d78-8586-44bd-91b5-1f3236a1241d.jpg');
INSERT INTO `sceneries` VALUES ('4', '呼伦贝尔大草原', '好绿', '2024-11-01', '2024-12-31', '4ff368c4-5f7c-483e-b58e-4f77b216f0ea.jpg');
INSERT INTO `sceneries` VALUES ('5', '苏州园林', '好美', '2024-10-01', '2024-12-31', '38e88908-b808-4c02-a24d-0d7b0cb571b4.jpg');

-- ----------------------------
-- Table structure for tickets
-- ----------------------------
DROP TABLE IF EXISTS `tickets`;
CREATE TABLE `tickets`  (
  `id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `price` double(32, 2) NOT NULL,
  `num` int(128) NOT NULL,
  `discount` double(16, 2) DEFAULT NULL,
  `text` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `state` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tickets
-- ----------------------------
INSERT INTO `tickets` VALUES ('1', 29.99, 300, 1.00, '学生票', '在售', '2024-10-01', '2024-11-30');
INSERT INTO `tickets` VALUES ('2', 65.00, 1000, 1.00, '成人票', '在售', '2024-10-01', '2024-11-30');
INSERT INTO `tickets` VALUES ('3', 35.00, 200, 0.85, '限时活动优惠学生票', '在售', '2024-12-01', '2024-12-31');
INSERT INTO `tickets` VALUES ('4', 25.00, 300, 1.00, '老年票', '在售', '2024-10-01', '2024-12-31');
INSERT INTO `tickets` VALUES ('5', 40.00, 200, 0.90, '限时活动优惠成人票', '在售', '2024-12-01', '2024-12-31');
INSERT INTO `tickets` VALUES ('6', 50.00, 300, 1.00, '长城普通票', '在售', '2024-10-01', '2024-12-31');
INSERT INTO `tickets` VALUES ('7', 80.00, 500, 1.00, '成人票', '在售', '2024-10-01', '2024-11-30');

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `pass` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '123',
  `nickname` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `sex` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `phone` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `bank` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `regtime` date NOT NULL,
  `power` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES ('1', '202cb962ac59075b964b07152d234b70', '小齐', '男', '13864317069', '11111111', '2024-12-07', 'admin', 'qhl');
INSERT INTO `user` VALUES ('2', '202cb962ac59075b964b07152d234b70', '小刘', '男', '15653303083', '22222222', '2024-11-30', 'user', 'lxz');
INSERT INTO `user` VALUES ('3', '202cb962ac59075b964b07152d234b70', '小美', '女', '15643351346', '33333333', '2024-11-25', 'user', 'xiaomei');
INSERT INTO `user` VALUES ('4', '202cb962ac59075b964b07152d234b70', '小王', '男', '15500000000', '44444444', '2024-12-04', 'user', 'xiaowang');
INSERT INTO `user` VALUES ('5', '202cb962ac59075b964b07152d234b70', '小张', '男', '15400000000', '55555555', '2024-11-12', 'user', 'xiaozhang');

SET FOREIGN_KEY_CHECKS = 1;
