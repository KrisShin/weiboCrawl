-- MySQL dump 10.13  Distrib 8.0.25, for Linux (x86_64)
--
-- Host: localhost    Database: weibo
-- ------------------------------------------------------
-- Server version	8.0.25-0ubuntu0.20.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comment`
--

DROP TABLE IF EXISTS `comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comment` (
  `id` int NOT NULL AUTO_INCREMENT,
  `feed_id` int DEFAULT NULL,
  `user_avatar` varchar(1024) DEFAULT NULL,
  `user_name` varchar(256) DEFAULT NULL,
  `content` text,
  `image` varchar(1024) DEFAULT NULL,
  `publish_time` datetime DEFAULT NULL,
  `like_count` int DEFAULT NULL,
  `reply_name` varchar(256) DEFAULT NULL,
  `reply_content` text,
  `reply_time` datetime DEFAULT NULL,
  `reply_like` int DEFAULT NULL,
  `reply_count` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `feed_id` (`feed_id`),
  CONSTRAINT `comment_ibfk_1` FOREIGN KEY (`feed_id`) REFERENCES `feed` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment`
--

LOCK TABLES `comment` WRITE;
/*!40000 ALTER TABLE `comment` DISABLE KEYS */;
INSERT INTO `comment` VALUES (1,1,NULL,NULL,'comment 0 of feed 1',NULL,'2021-06-03 00:21:02',802,NULL,NULL,NULL,601,801),(2,1,NULL,NULL,'comment 1 of feed 1',NULL,'2021-06-03 00:21:02',533,NULL,NULL,NULL,303,483),(3,1,NULL,NULL,'comment 2 of feed 1',NULL,'2021-06-03 00:21:02',775,NULL,NULL,NULL,839,816),(4,2,NULL,NULL,'comment 0 of feed 2',NULL,'2021-06-03 00:21:02',103,NULL,NULL,NULL,588,560),(5,2,NULL,NULL,'comment 1 of feed 2',NULL,'2021-06-03 00:21:02',295,NULL,NULL,NULL,320,311),(6,2,NULL,NULL,'comment 2 of feed 2',NULL,'2021-06-03 00:21:02',957,NULL,NULL,NULL,590,293),(7,3,NULL,NULL,'comment 0 of feed 3',NULL,'2021-06-03 00:21:02',956,NULL,NULL,NULL,373,770),(8,3,NULL,NULL,'comment 1 of feed 3',NULL,'2021-06-03 00:21:02',645,NULL,NULL,NULL,711,601),(9,3,NULL,NULL,'comment 2 of feed 3',NULL,'2021-06-03 00:21:02',998,NULL,NULL,NULL,541,820),(10,4,NULL,NULL,'comment 0 of feed 4',NULL,'2021-06-03 00:21:02',179,NULL,NULL,NULL,424,505),(11,4,NULL,NULL,'comment 1 of feed 4',NULL,'2021-06-03 00:21:02',752,NULL,NULL,NULL,340,271),(12,4,NULL,NULL,'comment 2 of feed 4',NULL,'2021-06-03 00:21:02',624,NULL,NULL,NULL,846,664),(13,5,NULL,NULL,'comment 0 of feed 5',NULL,'2021-06-03 00:21:02',775,NULL,NULL,NULL,256,822),(14,5,NULL,NULL,'comment 1 of feed 5',NULL,'2021-06-03 00:21:02',122,NULL,NULL,NULL,881,875),(15,5,NULL,NULL,'comment 2 of feed 5',NULL,'2021-06-03 00:21:02',270,NULL,NULL,NULL,497,262),(16,6,NULL,NULL,'comment 0 of feed 6',NULL,'2021-06-03 00:21:02',911,NULL,NULL,NULL,620,381),(17,6,NULL,NULL,'comment 1 of feed 6',NULL,'2021-06-03 00:21:02',993,NULL,NULL,NULL,885,139),(18,6,NULL,NULL,'comment 2 of feed 6',NULL,'2021-06-03 00:21:02',844,NULL,NULL,NULL,762,719),(19,7,NULL,NULL,'comment 0 of feed 7',NULL,'2021-06-03 00:21:02',451,NULL,NULL,NULL,649,291),(20,7,NULL,NULL,'comment 1 of feed 7',NULL,'2021-06-03 00:21:02',883,NULL,NULL,NULL,738,265),(21,7,NULL,NULL,'comment 2 of feed 7',NULL,'2021-06-03 00:21:02',187,NULL,NULL,NULL,950,213),(22,8,NULL,NULL,'comment 0 of feed 8',NULL,'2021-06-03 00:21:02',934,NULL,NULL,NULL,360,348),(23,8,NULL,NULL,'comment 1 of feed 8',NULL,'2021-06-03 00:21:02',638,NULL,NULL,NULL,342,504),(24,8,NULL,NULL,'comment 2 of feed 8',NULL,'2021-06-03 00:21:02',401,NULL,NULL,NULL,523,510),(25,9,NULL,NULL,'comment 0 of feed 9',NULL,'2021-06-03 00:21:02',304,NULL,NULL,NULL,659,934),(26,9,NULL,NULL,'comment 1 of feed 9',NULL,'2021-06-03 00:21:02',174,NULL,NULL,NULL,443,419),(27,9,NULL,NULL,'comment 2 of feed 9',NULL,'2021-06-03 00:21:02',494,NULL,NULL,NULL,670,647);
/*!40000 ALTER TABLE `comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feed`
--

DROP TABLE IF EXISTS `feed`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feed` (
  `id` int NOT NULL AUTO_INCREMENT,
  `topic_id` int DEFAULT NULL,
  `content` text,
  `user_avatar` varchar(1024) DEFAULT NULL,
  `user_name` varchar(256) DEFAULT NULL,
  `publish_time` datetime DEFAULT NULL,
  `forward_count` int DEFAULT NULL,
  `comment_count` int DEFAULT NULL,
  `like_count` int DEFAULT NULL,
  `image_list` json DEFAULT NULL,
  `vedio_list` json DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `topic_id` (`topic_id`),
  CONSTRAINT `feed_ibfk_1` FOREIGN KEY (`topic_id`) REFERENCES `topic` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feed`
--

LOCK TABLES `feed` WRITE;
/*!40000 ALTER TABLE `feed` DISABLE KEYS */;
INSERT INTO `feed` VALUES (1,1,'feed 0 of topic test0',NULL,NULL,'2021-06-03 00:21:02',868,766,497,NULL,NULL),(2,1,'feed 1 of topic test0',NULL,NULL,'2021-06-03 00:21:02',960,227,173,NULL,NULL),(3,1,'feed 2 of topic test0',NULL,NULL,'2021-06-03 00:21:02',808,184,484,NULL,NULL),(4,2,'feed 0 of topic test1',NULL,NULL,'2021-06-03 00:21:02',677,111,517,NULL,NULL),(5,2,'feed 1 of topic test1',NULL,NULL,'2021-06-03 00:21:02',899,268,467,NULL,NULL),(6,2,'feed 2 of topic test1',NULL,NULL,'2021-06-03 00:21:02',356,385,753,NULL,NULL),(7,3,'feed 0 of topic test2',NULL,NULL,'2021-06-03 00:21:02',223,558,921,NULL,NULL),(8,3,'feed 1 of topic test2',NULL,NULL,'2021-06-03 00:21:02',267,295,418,NULL,NULL),(9,3,'feed 2 of topic test2',NULL,NULL,'2021-06-03 00:21:02',606,135,366,NULL,NULL);
/*!40000 ALTER TABLE `feed` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topic`
--

DROP TABLE IF EXISTS `topic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `topic` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(256) DEFAULT NULL,
  `hot` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topic`
--

LOCK TABLES `topic` WRITE;
/*!40000 ALTER TABLE `topic` DISABLE KEYS */;
INSERT INTO `topic` VALUES (1,'test0',NULL),(2,'test1',NULL),(3,'test2',NULL);
/*!40000 ALTER TABLE `topic` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-06-03  0:21:55
