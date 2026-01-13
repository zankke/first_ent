mysqldump: [Warning] Using a password on the command line interface can be insecure.
-- MySQL dump 10.13  Distrib 8.0.43, for Linux (aarch64)
--
-- Host: localhost    Database: first_ent
-- ------------------------------------------------------
-- Server version	8.0.43

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
-- Table structure for table `Activities`
--

DROP TABLE IF EXISTS `Activities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Activities` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `activity_name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `activity_type` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `start_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  `location` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `manager_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `manager_id` (`manager_id`),
  CONSTRAINT `Activities_ibfk_1` FOREIGN KEY (`manager_id`) REFERENCES `Staff` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Activities`
--

LOCK TABLES `Activities` WRITE;
/*!40000 ALTER TABLE `Activities` DISABLE KEYS */;
INSERT INTO `Activities` VALUES (5,'박서준 - 볼뉴머','광고',NULL,NULL,NULL,1),(6,'박서준 - 룰루레몬','광고',NULL,NULL,NULL,1),(7,'박서준 - 에싸소파','광고',NULL,NULL,NULL,1),(8,'박서준 - 락토핏 솔루션','광고',NULL,NULL,NULL,1),(9,'이정재 - 더미식 라면','광고',NULL,NULL,NULL,NULL),(10,'이정재 - 하이퍼스','광고',NULL,NULL,NULL,NULL),(11,'이정재 - 퍼플렉시티','광고',NULL,NULL,NULL,NULL),(12,'이정재 - 수','광고',NULL,NULL,NULL,NULL),(13,'유지태 - 비피오','광고',NULL,NULL,NULL,NULL),(14,'유지태 - 베이지북','광고',NULL,NULL,NULL,NULL),(15,'유지태 - 스케쳐스','광고',NULL,NULL,NULL,NULL),(16,'유지태 - 제누','광고',NULL,NULL,NULL,NULL),(17,'유지태 - 비피오','광고',NULL,NULL,NULL,NULL),(18,'유지태 - 베이지북','광고',NULL,NULL,NULL,NULL),(19,'유지태 - 스케쳐스','광고',NULL,NULL,NULL,NULL),(20,'유지태 - 제누','광고',NULL,NULL,NULL,NULL),(21,'류준열 - 나이키 러닝','광고',NULL,NULL,NULL,NULL),(22,'류준열 - 그린피스','광고',NULL,NULL,NULL,NULL),(23,'이효리 - 부디무드라','광고',NULL,NULL,NULL,NULL),(24,'이효리 - 컬리','광고',NULL,NULL,NULL,NULL),(25,'류준열 - 나이키 러닝','광고',NULL,NULL,NULL,NULL),(26,'류준열 - 그린피스','광고',NULL,NULL,NULL,NULL),(27,'유지태 - 비피오','광고',NULL,NULL,NULL,NULL),(28,'유지태 - 베이지북','광고',NULL,NULL,NULL,NULL),(29,'유지태 - 스케쳐스','광고',NULL,NULL,NULL,NULL),(30,'유지태 - 제누','광고',NULL,NULL,NULL,NULL),(31,'김혜수 - 씨드비','광고',NULL,NULL,NULL,NULL),(32,'김혜수 - 악사','광고',NULL,NULL,NULL,NULL),(33,'김고은 - 알럭스','광고',NULL,NULL,NULL,NULL),(34,'김고은 - 네스프레소','광고',NULL,NULL,NULL,NULL),(35,'김고은 - 발베니 메이커스','광고',NULL,NULL,NULL,NULL),(36,'공효진 - 드파운드','광고',NULL,NULL,NULL,NULL),(37,'공효진 - 프로쉬','광고',NULL,NULL,NULL,NULL),(38,'신민아 - 랑콤','광고',NULL,NULL,NULL,NULL),(39,'신민아 - 루이비통 주얼리','광고',NULL,NULL,NULL,NULL),(40,'신민아 - 휴그린','광고',NULL,NULL,NULL,NULL),(41,'신민아 - 라이필','광고',NULL,NULL,NULL,NULL),(42,'신민아 - 글램팜','광고',NULL,NULL,NULL,NULL),(43,'신민아 - 로레알','광고',NULL,NULL,NULL,NULL),(44,'장윤주 - 강남언니','광고',NULL,NULL,NULL,NULL),(45,'장윤주 - 다우니','광고',NULL,NULL,NULL,NULL),(46,'장윤주 - 글렌피딕','광고',NULL,NULL,NULL,NULL),(47,'소지섭 - 한국여행엑스포 홍보대사','홍보',NULL,NULL,NULL,NULL),(48,'소지섭 - 랑방블랑','광고',NULL,NULL,NULL,NULL),(49,'차승원 - 케어네이션','광고',NULL,NULL,NULL,NULL),(50,'차승원 - 귀한족발','광고',NULL,NULL,NULL,NULL),(51,'차승원 - 엘리스랩','광고',NULL,NULL,NULL,NULL),(52,'차승원 - GSK 호흡기백신','광고',NULL,NULL,NULL,NULL),(53,'차승원 - JDX','광고',NULL,NULL,NULL,NULL),(54,'김석훈 - 환경포럼 참여','공익',NULL,NULL,NULL,NULL),(55,'김석훈 - 쓰레기 아저씨 유튜브','방송',NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `Activities` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Agencies`
--

DROP TABLE IF EXISTS `Agencies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Agencies` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `founded_date` date DEFAULT NULL,
  `location` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
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
-- Table structure for table `Albums`
--

DROP TABLE IF EXISTS `Albums`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Albums` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
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

DROP TABLE IF EXISTS `Artist_Assets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Artist_Assets` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `artist_id` bigint DEFAULT NULL,
  `asset_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `file_path` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
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
-- Table structure for table `Artist_Schedules`
--

DROP TABLE IF EXISTS `Artist_Schedules`;
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
-- Table structure for table `Artists`
--

DROP TABLE IF EXISTS `Artists`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Artists` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `birth_date` date NOT NULL,
  `height_cm` int DEFAULT NULL,
  `debut_date` date DEFAULT NULL,
  `genre` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `agency_id` bigint DEFAULT NULL,
  `nationality` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `is_korean` tinyint(1) DEFAULT '1',
  `gender` enum('WOMAN','MEN','EXTRA','FOREIGN') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `status` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `category_id` bigint DEFAULT NULL,
  `platform` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `social_media_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `profile_photo` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `guarantee_krw` bigint DEFAULT NULL COMMENT '모델료 또는 개런티 금액 (단위: 원)',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Artists`
--

LOCK TABLES `Artists` WRITE;
/*!40000 ALTER TABLE `Artists` DISABLE KEYS */;
INSERT INTO `Artists` VALUES (1,'박서준','1988-01-01',185,'2018-01-01','배우',NULL,'대한민국',1,'MEN','ACTIVE',NULL,'Instagram','https://www.instagram.com/bn_sj2013','/images/artists/profile/park_seo_joon_2025.png',1000000000),(2,'이정재','1972-01-01',180,'2020-01-01','배우',NULL,'대한민국',0,'MEN','OTHER',NULL,'Instagram','https://www.instagram.com/from_jjlee','/images/artists/profile/scene_01.png',1000000000),(3,'유지태','1976-01-01',188,'2018-01-01','배우',NULL,'대한민국',1,'MEN','RESTING',NULL,'Instagram','https://www.instagram.com/jt_db','/images/artists/profile/scene_02.png',100000000),(4,'류준열','1986-01-01',183,'2022-01-01','배우',NULL,'대한민국',1,'MEN','ACTIVE',NULL,'Instagram','https://www.instagram.com/ryusdb','',NULL),(5,'류승룡','1970-01-01',175,'2020-01-01','배우',NULL,'대한민국',1,'MEN','ACTIVE',NULL,'Instagram','https://www.instagram.com/ryusdb','',NULL),(6,'김석훈','1972-01-01',178,'2015-01-01','배우/방송인',NULL,'대한민국',1,'MEN','ACTIVE',NULL,'Youtube','https://www.youtube.com/@mr_kimyoutube','',NULL),(7,'이기우','1981-01-01',190,'2022-01-01','배우',NULL,'대한민국',1,'MEN','ACTIVE',NULL,'Instagram','https://www.instagram.com/lee_kiwoo',NULL,NULL),(8,'션','1972-01-01',180,'2021-01-01','가수/방송인',NULL,'대한민국',1,'MEN','OTHER',NULL,'Instagram','https://www.instagram.com/jinusean3000',NULL,NULL),(9,'소지섭','1977-01-01',182,'2018-01-01','배우',NULL,'대한민국',1,'MEN','ACTIVE',NULL,'Instagram','https://www.instagram.com/soganzi_51',NULL,NULL),(10,'차승원','1970-01-01',188,'2021-01-01','배우',NULL,'대한민국',1,'MEN','RESTING',NULL,'Instagram','https://www.instagram.com/70csw',NULL,NULL),(11,'이효리','1979-01-01',167,'2022-01-01','가수/방송인',NULL,'대한민국',1,'WOMAN','ACTIVE',NULL,'Instagram','https://www.instagram.com/lee_hyolee','',NULL),(12,'김혜수','1970-01-01',170,'2018-01-01','배우',NULL,'대한민국',1,'WOMAN','ACTIVE',NULL,'Instagram','https://www.instagram.com/hs_kim_95',NULL,NULL),(13,'김고은','1991-01-01',167,'2022-01-01','배우',NULL,'대한민국',1,'WOMAN','ACTIVE',NULL,'Instagram','https://www.instagram.com/ggonekim','/images/artists/profile/scene_04.png',NULL),(14,'공효진','1980-01-01',172,'2021-01-01','배우',NULL,'대한민국',1,'WOMAN','RESTING',NULL,'Instagram','https://www.instagram.com/rovvxhyo','/images/artists/profile/scene_05.png',NULL),(15,'수지','1994-01-01',168,'2022-01-01','가수/배우',NULL,'대한민국',1,'WOMAN','ACTIVE',NULL,'Instagram','https://www.instagram.com/skuukzky','/images/artists/profile/scene_06.png',NULL),(16,'아이유','1993-01-01',162,'2020-01-01','가수/배우',NULL,'대한민국',1,'WOMAN','ACTIVE',NULL,'Instagram','https://www.instagram.com/dlwlrma',NULL,NULL),(17,'박보영','1990-01-01',158,'2018-01-01','배우',NULL,'대한민국',1,'WOMAN','ACTIVE',NULL,'Instagram','https://www.instagram.com/boyoung0212_official',NULL,NULL),(18,'김유정','1999-01-01',164,'2022-01-01','배우',NULL,'대한민국',1,'WOMAN','ACTIVE',NULL,'Instagram','https://www.instagram.com/you_r_love',NULL,NULL),(19,'한효주','1987-01-01',172,'2021-01-01','배우',NULL,'대한민국',1,'WOMAN','ACTIVE',NULL,'Instagram','https://www.instagram.com/hanhyojoo222',NULL,NULL),(20,'신민아','1984-01-01',168,'2018-01-01','배우',NULL,'대한민국',1,'WOMAN','RESTING',NULL,'Instagram','https://www.instagram.com/illusomina',NULL,NULL),(21,'제니','1996-01-01',163,'2022-01-01','가수',NULL,'대한민국',1,'WOMAN',NULL,NULL,'Instagram','https://www.instagram.com/jennierubyjane',NULL,NULL),(22,'리사','1997-01-01',167,'2022-01-01','가수',NULL,'대한민국',1,'WOMAN',NULL,NULL,'Instagram','https://www.instagram.com/lalalalisa_m','https://cdn.firstent.com/profiles/lee_hyo_ri.jpg',NULL),(23,'로제','1997-01-01',168,'2022-01-01','가수',NULL,'대한민국',1,'WOMAN',NULL,NULL,'Instagram','https://www.instagram.com/roses_are_rosie',NULL,NULL),(24,'지수','1995-01-01',162,'2022-01-01','가수/배우',NULL,'대한민국',1,'WOMAN',NULL,NULL,'Instagram','https://www.instagram.com/sooyaaa__',NULL,NULL),(25,'김지원','1992-01-01',164,'2020-01-01','배우',NULL,'대한민국',1,'WOMAN','ACTIVE',NULL,'Instagram','https://www.instagram.com/geewonii','/images/artists/profile/scene_06.png',NULL),(26,'표예진','1992-01-01',163,'2022-01-01','배우',NULL,'대한민국',1,'WOMAN',NULL,NULL,'Instagram','https://www.instagram.com/pyo_ye_jin',NULL,NULL),(27,'고윤정','1996-01-01',167,'2021-01-01','배우',NULL,'대한민국',1,'WOMAN',NULL,NULL,'Instagram','https://www.instagram.com/goyounjung',NULL,NULL),(28,'노윤서','2000-01-01',165,'2022-01-01','배우',NULL,'대한민국',1,'WOMAN',NULL,NULL,'Instagram','https://www.instagram.com/rohyoonseo',NULL,NULL),(29,'박은빈','1992-01-01',163,'2018-01-01','배우',NULL,'대한민국',1,'WOMAN',NULL,NULL,'Instagram','https://www.instagram.com/eunbining0904','/images/artists/profile/scene_03.png',NULL),(30,'이성경','1990-01-01',175,'2020-01-01','배우/모델',NULL,'대한민국',1,'WOMAN',NULL,NULL,'Instagram','https://www.instagram.com/heybiblee',NULL,NULL),(43,'장윤주','1980-03-20',171,'1997-01-01','배우/모델',NULL,'대한민국',1,'WOMAN','ACTIVE',NULL,NULL,NULL,NULL,400000000),(65,'frederika 프레데리카','1996-10-28',174,'2014-10-28','모델',NULL,'슬로바키아',0,'FOREIGN','ACTIVE',NULL,NULL,NULL,NULL,NULL),(66,'kamila m 카밀라 m','2004-10-28',174,'2022-10-28','모델',NULL,'러시아',0,'FOREIGN','ACTIVE',NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `Artists` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `CareerHistory`
--

DROP TABLE IF EXISTS `CareerHistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `CareerHistory` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `artist_id` bigint NOT NULL,
  `type` enum('드라마','영화','방송','공익','광고','공연','홍보','기타') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `year` year DEFAULT NULL,
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `memo` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  PRIMARY KEY (`id`),
  KEY `artist_id` (`artist_id`),
  CONSTRAINT `CareerHistory_ibfk_1` FOREIGN KEY (`artist_id`) REFERENCES `Artists` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CareerHistory`
--

LOCK TABLES `CareerHistory` WRITE;
/*!40000 ALTER TABLE `CareerHistory` DISABLE KEYS */;
INSERT INTO `CareerHistory` VALUES (1,1,'드라마',2024,'경성크리처 시즌2',NULL),(2,1,'드라마',2023,'경성크리처',NULL),(3,1,'영화',2023,'더 마블스',NULL),(4,1,'방송',2024,'서진이네2',NULL),(5,11,'광고',2024,'알레르망 비건 라인','비건/친환경 메시지'),(6,25,'드라마',2024,'애기씨 부군간택뎐',NULL),(7,25,'공연',2022,'다락방',NULL),(8,26,'드라마',2025,'모범택시3','촬영예정'),(9,26,'드라마',2025,'빌런의 나라',NULL),(10,4,'광고',2024,'나이키 러닝',NULL),(11,4,'공익',2024,'그린피스',NULL),(12,3,'광고',2024,'비피오',NULL),(13,3,'광고',2024,'베이지북',NULL),(14,3,'광고',2024,'스케쳐스',NULL),(15,3,'광고',2024,'제누',NULL),(16,12,'광고',2024,'씨드비',NULL),(17,12,'광고',2024,'악사',NULL),(18,13,'광고',2024,'알럭스',NULL),(19,13,'광고',2024,'네스프레소',NULL),(20,13,'광고',2024,'발베니 메이커스',NULL),(21,14,'광고',2024,'드파운드',NULL),(22,14,'광고',2024,'프로쉬',NULL),(23,20,'광고',2024,'랑콤',NULL),(24,20,'광고',2024,'루이비통 주얼리',NULL),(25,20,'광고',2024,'휴그린',NULL),(26,20,'광고',2024,'라이필',NULL),(27,20,'광고',2024,'글램팜',NULL),(28,20,'광고',2024,'로레알',NULL),(29,43,'광고',2024,'강남언니',NULL),(30,43,'광고',2024,'다우니',NULL),(31,43,'광고',2024,'글렌피딕',NULL),(32,9,'홍보',2024,'한국여행엑스포 홍보대사',NULL),(33,9,'광고',2024,'랑방블랑',NULL),(34,10,'광고',2024,'케어네이션',NULL),(35,10,'광고',2024,'귀한족발',NULL),(36,10,'광고',2024,'엘리스랩',NULL),(37,10,'광고',2024,'GSK 호흡기백신',NULL),(38,10,'광고',2024,'JDX',NULL),(39,6,'공익',2024,'환경포럼 참여',NULL),(40,6,'방송',2024,'쓰레기 아저씨 유튜브',NULL);
/*!40000 ALTER TABLE `CareerHistory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ContractInfo`
--

DROP TABLE IF EXISTS `ContractInfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ContractInfo` (
  `artist_id` bigint NOT NULL,
  `fee_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `fee_amount` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `validity_year` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
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

DROP TABLE IF EXISTS `Recommendation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Recommendation` (
  `artist_id` bigint NOT NULL,
  `reason_type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `source` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
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
-- Table structure for table `Role_Types`
--

DROP TABLE IF EXISTS `Role_Types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Role_Types` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `role_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
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
-- Table structure for table `Staff`
--

DROP TABLE IF EXISTS `Staff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Staff` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `position` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `contact_phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `email` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `agency_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `agency_id` (`agency_id`),
  CONSTRAINT `Staff_ibfk_1` FOREIGN KEY (`agency_id`) REFERENCES `Agencies` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Staff`
--

LOCK TABLES `Staff` WRITE;
/*!40000 ALTER TABLE `Staff` DISABLE KEYS */;
INSERT INTO `Staff` VALUES (1,'홍길동 매니저','팀장',NULL,NULL,NULL);
/*!40000 ALTER TABLE `Staff` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Users`
--

DROP TABLE IF EXISTS `Users`;
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
-- Table structure for table `accounts`
--

DROP TABLE IF EXISTS `accounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts` (
  `account_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `password_hash` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `role` enum('admin','user') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT 'user',
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
INSERT INTO `alembic_version` VALUES ('548dcaa57192');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_keys`
--

DROP TABLE IF EXISTS `api_keys`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_keys` (
  `id` int NOT NULL AUTO_INCREMENT,
  `platform` enum('instagram','youtube','tiktok','twitter') NOT NULL,
  `api_name` varchar(100) NOT NULL,
  `api_key` text NOT NULL,
  `api_secret` text,
  `is_active` tinyint(1) DEFAULT NULL,
  `last_used_at` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_keys`
--

LOCK TABLES `api_keys` WRITE;
/*!40000 ALTER TABLE `api_keys` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_keys` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `database_configs`
--

DROP TABLE IF EXISTS `database_configs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `database_configs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `config_name` varchar(100) NOT NULL,
  `host` varchar(100) NOT NULL,
  `port` int NOT NULL,
  `database_name` varchar(100) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password_encrypted` text NOT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `config_name` (`config_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `database_configs`
--

LOCK TABLES `database_configs` WRITE;
/*!40000 ALTER TABLE `database_configs` DISABLE KEYS */;
/*!40000 ALTER TABLE `database_configs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `model_categories`
--

DROP TABLE IF EXISTS `model_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `model_categories` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `category_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `category_index` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `category_name` (`category_name`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `model_categories`
--

LOCK TABLES `model_categories` WRITE;
/*!40000 ALTER TABLE `model_categories` DISABLE KEYS */;
INSERT INTO `model_categories` VALUES (1,'일반모델(성인)',1),(2,'일반모델(아동)',2),(3,'패션모델',3),(4,'연예인',4),(5,'아동모델',5),(6,'전문 외국인 모델',6),(7,'B 외국인 모델',7),(8,'Influencer',8),(9,'Celebrity',9);
/*!40000 ALTER TABLE `model_categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `news`
--

DROP TABLE IF EXISTS `news`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `news` (
  `id` int NOT NULL AUTO_INCREMENT,
  `artist_id` bigint NOT NULL,
  `title` varchar(500) NOT NULL,
  `content` text,
  `url` text NOT NULL,
  `source` varchar(200) DEFAULT NULL,
  `published_at` timestamp NULL DEFAULT NULL,
  `crawled_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `sentiment` enum('positive','negative','neutral') DEFAULT 'neutral',
  `relevance_score` float DEFAULT '0',
  `keywords` json DEFAULT NULL,
  `is_processed` tinyint(1) DEFAULT '0',
  `thumbnail` varchar(255) DEFAULT NULL,
  `media_name` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_news_url` (`url`(255)),
  KEY `artist_id` (`artist_id`),
  CONSTRAINT `news_ibfk_1` FOREIGN KEY (`artist_id`) REFERENCES `Artists` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `news`
--

LOCK TABLES `news` WRITE;
/*!40000 ALTER TABLE `news` DISABLE KEYS */;
/*!40000 ALTER TABLE `news` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-28  9:22:16
