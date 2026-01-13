-- MySQL dump 10.13  Distrib 8.0.43, for Linux (aarch64)
--
-- Host: localhost    Database: first_ent_v2
-- ------------------------------------------------------
-- Server version	8.0.43

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
-- /*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
-- /*!40103 SET TIME_ZONE='+00:00' */;
-- /*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
-- /*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0; */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

USE first_ent;;

-- Drop tables in reverse dependency order
DROP TABLE IF EXISTS `Songs`;
DROP TABLE IF EXISTS `Albums`;
DROP TABLE IF EXISTS `Artist_Assets`;
DROP TABLE IF EXISTS `Artist_Awards`;
DROP TABLE IF EXISTS `Artist_Managers`;
DROP TABLE IF EXISTS `Artist_Roles`;
DROP TABLE IF EXISTS `Artist_Schedules`;
DROP TABLE IF EXISTS `CareerHistory`;
DROP TABLE IF EXISTS `ContractInfo`;
DROP TABLE IF EXISTS `Recommendation`;
DROP TABLE IF EXISTS `Activities`;
DROP TABLE IF EXISTS `Staff`;
DROP TABLE IF EXISTS `Agencies`;
DROP TABLE IF EXISTS `Boards`;
DROP TABLE IF EXISTS `Users`;
DROP TABLE IF EXISTS `accounts`;
DROP TABLE IF EXISTS `model_categories`;
DROP TABLE IF EXISTS `Role_Types`;
DROP TABLE IF EXISTS `Artists`;

--
-- Table structure for table `Agencies`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Agencies` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` text COLLATE utf8mb4_general_ci NOT NULL,
  `founded_date` date DEFAULT NULL,
  `location` text COLLATE utf8mb4_general_ci,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Agencies`
--

LOCK TABLES `Agencies` WRITE;
/*!40000 ALTER TABLE `Agencies` DISABLE KEYS */;
INSERT INTO `Agencies` VALUES (1,'Test Entertainment','2025-10-19','Seoul');
/*!40000 ALTER TABLE `Agencies` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Staff`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Staff` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` text COLLATE utf8mb4_general_ci NOT NULL,
  `position` text COLLATE utf8mb4_general_ci,
  `contact_phone` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `email` text COLLATE utf8mb4_general_ci,
  `agency_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `agency_id` (`agency_id`),
  CONSTRAINT `Staff_ibfk_1` FOREIGN KEY (`agency_id`) REFERENCES `Agencies` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Staff`
--

LOCK TABLES `Staff` WRITE;
/*!40000 ALTER TABLE `Staff` DISABLE KEYS */;
/*!40000 ALTER TABLE `Staff` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Activities`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Activities` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `activity_name` text COLLATE utf8mb4_general_ci NOT NULL,
  `activity_type` text COLLATE utf8mb4_general_ci,
  `start_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  `location` text COLLATE utf8mb4_general_ci,
  `manager_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `manager_id` (`manager_id`),
  CONSTRAINT `Activities_ibfk_1` FOREIGN KEY (`manager_id`) REFERENCES `Staff` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Activities`
--

LOCK TABLES `Activities` WRITE;
/*!40000 ALTER TABLE `Activities` DISABLE KEYS */;
/*!40000 ALTER TABLE `Activities` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Artists`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Artists` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `birth_date` date NOT NULL,
  `height_cm` int DEFAULT NULL,
  `debut_date` date DEFAULT NULL,
  `genre` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `agency_id` bigint DEFAULT NULL,
  `nationality` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `is_korean` tinyint(1) DEFAULT '1',
  `gender` enum('WOMAN','MEN','EXTRA','FOREIGN') COLLATE utf8mb4_general_ci DEFAULT NULL,
  `status` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `category_id` bigint DEFAULT NULL,
  `platform` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `social_media_url` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `profile_photo` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Artists`
--

LOCK TABLES `Artists` WRITE;
/*!40000 ALTER TABLE `Artists` DISABLE KEYS */;
INSERT INTO `Artists` VALUES (1,'박서준','1988-01-01',185,'2018-01-01','배우',NULL,'대한민국',1,'MEN',NULL,NULL,'Instagram','https://www.instagram.com/bn_sj2013','/images/artists/profile/park_seo_joon_2025.png'),(2,'이정재','1972-01-01',180,'2020-01-01','배우',NULL,'대한민국',1,'MEN',NULL,NULL,'Instagram','https://www.instagram.com/from_jjlee',NULL),(3,'유지태','1976-01-01',188,'2018-01-01','배우',NULL,'대한민국',1,'MEN',NULL,NULL,'Instagram','https://www.instagram.com/jt_db',NULL),(4,'류준열','1986-01-01',183,'2022-01-01','배우',NULL,'대한민국',1,'MEN',NULL,NULL,'Instagram','https://www.instagram.com/ryusdb',NULL),(5,'류승룡','1970-01-01',175,'2020-01-01','배우',NULL,'대한민국',1,'MEN',NULL,NULL,'Instagram','https://www.instagram.com/ryusdb',NULL),(6,'김석훈','1972-01-01',178,'2015-01-01','배우/방송인',NULL,'대한민국',1,'MEN',NULL,NULL,'Youtube','https://www.youtube.com/@mr_kimyoutube',NULL),(7,'이기우','1981-01-01',190,'2022-01-01','배우',NULL,'대한민국',1,'MEN',NULL,NULL,'Instagram','https://www.instagram.com/lee_kiwoo',NULL),(8,'션','1972-01-01',180,'2021-01-01','가수/방송인',NULL,'대한민국',1,'MEN',NULL,NULL,'Instagram','https://www.instagram.com/jinusean3000',NULL),(9,'소지섭','1977-01-01',182,'2018-01-01','배우',NULL,'대한민국',1,'MEN',NULL,NULL,'Instagram','https://www.instagram.com/soganzi_51',NULL),(10,'차승원','1970-01-01',188,'2021-01-01','배우',NULL,'대한민국',1,'MEN',NULL,NULL,'Instagram','https://www.instagram.com/70csw',NULL),(11,'이효리','1979-01-01',167,'2022-01-01','가수/방송인',NULL,'대한민국',1,'WOMAN',NULL,NULL,'Instagram','https://www.instagram.com/lee_hyolee','https://cdn.firstent.com/profiles/lee_hyo_ri.jpg'),(12,'김혜수','1970-01-01',170,'2018-01-01','배우',NULL,'대한민국',1,'WOMAN',NULL,NULL,'Instagram','https://www.instagram.com/hs_kim_95',NULL),(13,'김고은','1991-01-01',167,'2022-01-01','배우',NULL,'대한민국',1,'WOMAN',NULL,NULL,'Instagram','https://www.instagram.com/ggonekim','https://cdn.firstent.com/profiles/kim_go_eun.jpg'),(14,'공효진','1980-01-01',172,'2021-01-01','배우',NULL,'대한민국',1,'WOMAN',NULL,NULL,'Instagram','https://www.instagram.com/rovvxhyo',NULL),(15,'수지','1994-01-01',168,'2022-01-01','가수/배우',NULL,'대한민국',1,'WOMAN',NULL,NULL,'Instagram','https://www.instagram.com/skuukzky',NULL),(16,'아이유','1993-01-01',162,'2020-01-01','가수/배우',NULL,'대한민국',1,'WOMAN',NULL,NULL,'Instagram','https://www.instagram.com/dlwlrma',NULL),(17,'박보영','1990-01-01',158,'2018-01-01','배우',NULL,'대한민국',1,'WOMAN',NULL,NULL,'Instagram','https://www.instagram.com/boyoung0212_official',NULL),(18,'김유정','1999-01-01',164,'2022-01-01','배우',NULL,'대한민국',1,'WOMAN',NULL,NULL,'Instagram','https://www.instagram.com/you_r_love',NULL),(19,'한효주','1987-01-01',172,'2021-01-01','배우',NULL,'대한민국',1,'WOMAN',NULL,NULL,'Instagram','https://www.instagram.com/hanhyojoo222',NULL),(20,'신민아','1984-01-01',168,'2018-01-01','배우',NULL,'대한민국',1,'WOMAN',NULL,NULL,'Instagram','https://www.instagram.com/illusomina',NULL),(21,'제니','1996-01-01',163,'2022-01-01','가수',NULL,'대한민국',1,'WOMAN',NULL,NULL,'Instagram','https://www.instagram.com/jennierubyjane',NULL),(22,'리사','1997-01-01',167,'2022-01-01','가수',NULL,'대한민국',1,'WOMAN',NULL,NULL,'Instagram','https://www.instagram.com/lalalalisa_m',NULL),(23,'로제','1997-01-01',168,'2022-01-01','가수',NULL,'대한민국',1,'WOMAN',NULL,NULL,'Instagram','https://www.instagram.com/roses_are_rosie',NULL),(24,'지수','1995-01-01',162,'2022-01-01','가수/배우',NULL,'대한민국',1,'WOMAN',NULL,NULL,'Instagram','https://www.instagram.com/sooyaaa__',NULL),(25,'김지원','1992-01-01',164,'2020-01-01','배우',NULL,'대한민국',1,'WOMAN',NULL,NULL,'Instagram','https://www.instagram.com/geewonii',NULL),(26,'표예진','1992-01-01',163,'2022-01-01','배우',NULL,'대한민국',1,'WOMAN',NULL,NULL,'Instagram','https://www.instagram.com/pyo_ye_jin',NULL),(27,'고윤정','1996-01-01',167,'2021-01-01','배우',NULL,'대한민국',1,'WOMAN',NULL,NULL,'Instagram','https://www.instagram.com/goyounjung',NULL),(28,'노윤서','2000-01-01',165,'2022-01-01','배우',NULL,'대한민국',1,'WOMAN',NULL,NULL,'Instagram','https://www.instagram.com/rohyoonseo',NULL),(29,'박은빈','1992-01-01',163,'2018-01-01','배우',NULL,'대한민국',1,'WOMAN',NULL,NULL,'Instagram','https://www.instagram.com/eunbining0904',NULL),(30,'이성경','1990-01-01',175,'2020-01-01','배우/모델',NULL,'대한민국',1,'WOMAN',NULL,NULL,'Instagram','https://www.instagram.com/heybiblee',NULL);
/*!40000 ALTER TABLE `Artists` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Albums`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Albums` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` text COLLATE utf8mb4_general_ci NOT NULL,
  `release_date` date DEFAULT NULL,
  `artist_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `artist_id` (`artist_id`),
  CONSTRAINT `Albums_ibfk_1` FOREIGN KEY (`artist_id`) REFERENCES `Artists` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Albums`
--

LOCK TABLES `Albums` WRITE;
/*!40000 ALTER TABLE `Albums` DISABLE KEYS */;
/*!40000 ALTER TABLE `Albums` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Artist_Assets`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Artist_Assets` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `artist_id` bigint DEFAULT NULL,
  `asset_type` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `file_path` text COLLATE utf8mb4_general_ci NOT NULL,
  `description` text COLLATE utf8mb4_general_ci,
  `upload_date` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `artist_id` (`artist_id`),
  CONSTRAINT `Artist_Assets_ibfk_1` FOREIGN KEY (`artist_id`) REFERENCES `Artists` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Artist_Assets`
--

LOCK TABLES `Artist_Assets` WRITE;
/*!40000 ALTER TABLE `Artist_Assets` DISABLE KEYS */;
/*!40000 ALTER TABLE `Artist_Assets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Artist_Awards`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Artist_Awards` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `artist_id` bigint DEFAULT NULL,
  `award_name` text COLLATE utf8mb4_general_ci NOT NULL,
  `award_year` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `artist_id` (`artist_id`),
  CONSTRAINT `Artist_Awards_ibfk_1` FOREIGN KEY (`artist_id`) REFERENCES `Artists` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Artist_Awards`
--

LOCK TABLES `Artist_Awards` WRITE;
/*!40000 ALTER TABLE `Artist_Awards` DISABLE KEYS */;
/*!40000 ALTER TABLE `Artist_Awards` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Artist_Managers`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Artist_Managers` (
  `artist_id` bigint NOT NULL,
  `staff_id` bigint NOT NULL,
  PRIMARY KEY (`artist_id`,`staff_id`),
  KEY `staff_id` (`staff_id`),
  CONSTRAINT `Artist_Managers_ibfk_1` FOREIGN KEY (`artist_id`) REFERENCES `Artists` (`id`),
  CONSTRAINT `Artist_Managers_ibfk_2` FOREIGN KEY (`staff_id`) REFERENCES `Staff` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Artist_Managers`
--

LOCK TABLES `Artist_Managers` WRITE;
/*!40000 ALTER TABLE `Artist_Managers` DISABLE KEYS */;
/*!40000 ALTER TABLE `Artist_Managers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Role_Types`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Role_Types` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `role_name` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `role_name` (`role_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Role_Types`
--

LOCK TABLES `Role_Types` WRITE;
/*!40000 ALTER TABLE `Role_Types` DISABLE KEYS */;
/*!40000 ALTER TABLE `Role_Types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Artist_Roles`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Artist_Roles` (
  `artist_id` bigint NOT NULL,
  `role_type_id` bigint NOT NULL,
  PRIMARY KEY (`artist_id`,`role_type_id`),
  KEY `role_type_id` (`role_type_id`),
  CONSTRAINT `Artist_Roles_ibfk_1` FOREIGN KEY (`artist_id`) REFERENCES `Artists` (`id`),
  CONSTRAINT `Artist_Roles_ibfk_2` FOREIGN KEY (`role_type_id`) REFERENCES `Role_Types` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Artist_Roles`
--

LOCK TABLES `Artist_Roles` WRITE;
/*!40000 ALTER TABLE `Artist_Roles` DISABLE KEYS */;
/*!40000 ALTER TABLE `Artist_Roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Artist_Schedules`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Artist_Schedules` (
  `artist_id` bigint NOT NULL,
  `activity_id` bigint NOT NULL,
  PRIMARY KEY (`artist_id`,`activity_id`),
  KEY `activity_id` (`activity_id`),
  CONSTRAINT `Artist_Schedules_ibfk_1` FOREIGN KEY (`artist_id`) REFERENCES `Artists` (`id`),
  CONSTRAINT `Artist_Schedules_ibfk_2` FOREIGN KEY (`activity_id`) REFERENCES `Activities` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Artist_Schedules`
--

LOCK TABLES `Artist_Schedules` WRITE;
/*!40000 ALTER TABLE `Artist_Schedules` DISABLE KEYS */;
/*!40000 ALTER TABLE `Artist_Schedules` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Users`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Users` (
  `uqid` int NOT NULL AUTO_INCREMENT COMMENT '키값',
  `level` varchar(10) NOT NULL COMMENT '권한',
  `utitle` varchar(20) DEFAULT NULL,
  `uname` varchar(30) NOT NULL COMMENT '이름',
  `uid` varchar(30) NOT NULL COMMENT '아이디',
  `upass` varchar(300) NOT NULL COMMENT '비밀번호',
  `uemail` varchar(100) NOT NULL,
  `utax` varchar(10) DEFAULT NULL,
  `uhead` varchar(10) DEFAULT NULL,
  `udepart` int DEFAULT NULL COMMENT '부서',
  `uphoto` varbinary(500) DEFAULT NULL COMMENT '사진',
  `status` varchar(10) NOT NULL DEFAULT 'Y' COMMENT '상태',
  `regdate` datetime DEFAULT CURRENT_TIMESTAMP,
  `hiredate` date DEFAULT NULL,
  `last_login` datetime DEFAULT CURRENT_TIMESTAMP COMMENT 'zusam.ai 로그인시 업데이트 됨',
  `service_name` varchar(20) DEFAULT NULL COMMENT '이용한  서비스 메뉴(Link)',
  PRIMARY KEY (`uqid`,`uname`,`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=179 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Users`
--

LOCK TABLES `Users` WRITE;
/*!40000 ALTER TABLE `Users` DISABLE KEYS */;
/*!40000 ALTER TABLE `Users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Boards`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Boards` (
  `board_id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(128) COLLATE utf8mb4_general_ci NOT NULL,
  `content` text COLLATE utf8mb4_general_ci,
  `created_by` int DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`board_id`),
  KEY `created_by` (`created_by`),
  CONSTRAINT `Boards_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `Users` (`uqid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Boards`
--

LOCK TABLES `Boards` WRITE;
/*!40000 ALTER TABLE `Boards` DISABLE KEYS */;
/*!40000 ALTER TABLE `Boards` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `CareerHistory`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `CareerHistory` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `artist_id` bigint NOT NULL,
  `type` enum('드라마','영화','방송','공익','광고','공연','홍보','기타') COLLATE utf8mb4_general_ci NOT NULL,
  `year` year DEFAULT NULL,
  `title` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `memo` text COLLATE utf8mb4_general_ci,
  PRIMARY KEY (`id`),
  KEY `artist_id` (`artist_id`),
  CONSTRAINT `CareerHistory_ibfk_1` FOREIGN KEY (`artist_id`) REFERENCES `Artists` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CareerHistory`
--

LOCK TABLES `CareerHistory` WRITE;
/*!40000 ALTER TABLE `CareerHistory` DISABLE KEYS */;
INSERT INTO `CareerHistory` VALUES (1,1,'드라마',2024,'경성크리처 시즌2',NULL),(2,1,'드라마',2023,'경성크리처',NULL),(3,1,'영화',2023,'더 마블스',NULL),(4,1,'방송',2024,'서진이네2',NULL),(5,11,'광고',2024,'알레르망 비건 라인','비건/친환경 메시지'),(6,25,'드라마',2024,'애기씨 부군간택뎐',NULL),(7,25,'공연',2022,'다락방',NULL),(8,26,'드라마',2025,'모범택시3','촬영예정'),(9,26,'드라마',2025,'빌런의 나라',NULL);
/*!40000 ALTER TABLE `CareerHistory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ContractInfo`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ContractInfo` (
  `artist_id` bigint NOT NULL,
  `fee_type` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `fee_amount` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `validity_year` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`artist_id`),
  CONSTRAINT `ContractInfo_ibfk_1` FOREIGN KEY (`artist_id`) REFERENCES `Artists` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ContractInfo`
--

LOCK TABLES `ContractInfo` WRITE;
/*!40000 ALTER TABLE `ContractInfo` DISABLE KEYS */;
INSERT INTO `ContractInfo` VALUES (10,'1년','10억','2024~');
/*!40000 ALTER TABLE `ContractInfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Recommendation`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Recommendation` (
  `artist_id` bigint NOT NULL,
  `reason_type` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `description` text COLLATE utf8mb4_general_ci,
  `source` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`artist_id`),
  CONSTRAINT `Recommendation_ibfk_1` FOREIGN KEY (`artist_id`) REFERENCES `Artists` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Recommendation`
--

LOCK TABLES `Recommendation` WRITE;
/*!40000 ALTER TABLE `Recommendation` DISABLE KEYS */;
INSERT INTO `Recommendation` VALUES (1,'환경보호','국제자연보전기관인 WWF(세계자연기금) 홍보대사로 꾸준히 활동 중이며, 리텍스타일 캠페인에 참여함.','WWF 홍보대사/리텍스타일 캠페인'),(13,'친환경/비건','알레르망 비건 라인의 자연 친화적 메시지를 담아내며, 환경 보호 기부 활동을 이어감.','알레르망 비건 라인');
/*!40000 ALTER TABLE `Recommendation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `model_categories`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `model_categories` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `category_name` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `category_index` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `category_name` (`category_name`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `model_categories`
--

LOCK TABLES `model_categories` WRITE;
/*!40000 ALTER TABLE `model_categories` DISABLE KEYS */;
INSERT INTO `model_categories` VALUES (1,'일반모델(성인)',1),(2,'일반모델(아동)',2),(3,'패션모델',3),(4,'연예인',4),(5,'아동모델',5),(6,'전문 외국인 모델',6),(7,'B 외국인 모델',7);
/*!40000 ALTER TABLE `model_categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts` (
  `account_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(64) COLLATE utf8mb4_general_ci NOT NULL,
  `password_hash` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(128) COLLATE utf8mb4_general_ci NOT NULL,
  `role` enum('admin','user') COLLATE utf8mb4_general_ci DEFAULT 'user',
  `last_login` datetime DEFAULT NULL,
  PRIMARY KEY (`account_id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts`
--

LOCK TABLES `accounts` WRITE;
/*!40000 ALTER TABLE `accounts` DISABLE KEYS */;
INSERT INTO `accounts` VALUES (1,'first_admin','$2b$12$8QK6qeXKyGJLIMBOP8Dwle7Cx/rg3wgdXQyXwicozruDRnHXieQqi','zankke@gmail.com','admin','2025-10-19 22:21:36'),(12,'itsme','$2b$12$iJD4TxfvxMFrw1QW8WD0w.1nB9PD509vcCSy07DeW/3RuYdDSryd.','cubleinc@gmail.com','user',NULL);
/*!40000 ALTER TABLE `accounts` ENABLE KEYS */;
UNLOCK TABLES;



/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-22  8:11:23

-- Grant root user access from any host for development
ALTER USER 'root'@'%' IDENTIFIED BY 'qpflxktm(*)!#%';
FLUSH PRIVILEGES;